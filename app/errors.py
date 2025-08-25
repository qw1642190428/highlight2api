from loguru import logger


class HighlightError(Exception):
    def __init__(self, status_code: int, message: str, response_status_code: int = 500):
        self.status_code = status_code
        self.message = message
        self.response_status_code = response_status_code
        logger.error(self.__str__())

    def __str__(self) -> str:
        return f"HighlightError: {self.status_code}, {self.message}"

    def to_openai_error(self) -> dict[str, dict[str, str]]:
        return {
            "error": {
                "message": self.__str__(),
                "type": "highlight_error",
                "code": "highlight_error"
            }
        }
