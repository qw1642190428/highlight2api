import base64
import json
from typing import List, Dict, Any, Optional, Union, Callable

from curl_cffi.requests.exceptions import RequestException
from sse_starlette import EventSourceResponse
from starlette.responses import JSONResponse

from .errors import HighlightError
from .models import Message, OpenAITool


def format_messages_to_prompt(messages: List[Message]) -> str:
    """将OpenAI格式的消息转换为单个提示字符串"""
    formatted_messages = []
    for message in messages:
        if message.role:
            if message.content:
                if isinstance(message.content, list):
                    for item in message.content:
                        formatted_messages.append(f"{message.role}: {item.text}")
                else:
                    formatted_messages.append(f"{message.role}: {message.content}")
            if message.tool_calls:
                formatted_messages.append(
                    f"{message.role}: {json.dumps(message.tool_calls)}"
                )
            if message.tool_call_id:
                formatted_messages.append(
                    f"{message.role}: tool_call_id: {message.tool_call_id} {message.content}"
                )
    return "\n\n".join(formatted_messages)


def format_openai_tools(tools: Optional[List[OpenAITool]]) -> List[Dict[str, Any]]:
    """将OpenAI格式的工具转换为Highlight格式"""
    if not tools:
        return []

    highlight_tools = []
    for tool in tools:
        if tool.type == "function":
            highlight_tool = {
                "name": tool.function.name,
                "description": tool.function.description or "",
                "parameters": tool.function.parameters or {}
            }
            highlight_tools.append(highlight_tool)

    return highlight_tools


async def safe_stream_wrapper(
        generator_func, *args, **kwargs
) -> Union[EventSourceResponse, JSONResponse]:
    """
    安全的流响应包装器
    先执行生成器获取第一个值，如果成功才创建流响应
    """
    # 创建生成器实例
    generator = generator_func(*args, **kwargs)

    # 尝试获取第一个值
    first_item = await generator.__anext__()

    # 如果成功获取第一个值，创建新的生成器包装原生成器
    async def wrapped_generator():
        # 先yield第一个值
        yield first_item
        # 然后yield剩余的值
        async for item in generator:
            yield item

    # 创建流响应
    return EventSourceResponse(
        wrapped_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def error_wrapper(func: Callable, *args, **kwargs) -> Any:
    from .config import MAX_RETRIES
    for attempt in range(MAX_RETRIES + 1):  # 包含初始尝试，所以是 MAX_RETRIES + 1
        try:
            return await func(*args, **kwargs)
        except (HighlightError, RequestException) as e:
            # 如果已经达到最大重试次数，返回错误响应
            if attempt == MAX_RETRIES:
                if isinstance(e, HighlightError):
                    return JSONResponse(
                        e.to_openai_error(),
                        status_code=e.response_status_code
                    )
                elif isinstance(e, RequestException):
                    return JSONResponse(
                        {
                            'error': {
                                'message': str(e),
                                "type": "http_error",
                                "code": "http_error"
                            }
                        },
                        status_code=500
                    )

            if attempt < MAX_RETRIES:
                continue
    return None


def decode_base64url_safe(data):
    """使用安全的base64url解码"""
    # 添加必要的填充
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)

    return base64.urlsafe_b64decode(data)


def check_ban_content(content: str) -> bool:
    ban_strs = [
        'Your account has been secured',
        'To protect our community',
        "Your account status has been updated to 'restricted'",
        'support@highlight.ing',
        'We’ve detected unusual',
        'support@highlightai.com',
        "We've temporarily restricted access",
        "due to suspicious activity.",
        "Highlight support",
        'Your account access is limited'
    ]
    for ban_str in ban_strs:
        if ban_str in content:
            return True
    return False
