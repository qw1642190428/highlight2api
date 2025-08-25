# Highlight2API

将 Highlight AI 转换为 OpenAI 兼容的 API 接口，支持流式响应、工具调用和图片处理。

## 🚀 一键部署

```bash
docker run -d -p 8080:8080 --name highlight2api ghcr.io/jhhgiyv/highlight2api:latest
```
自定义环境变量部署
```bash
docker run -d -p 8080:8080 \
  -e DEBUG=true \
  -e MAX_RETRIES=3 \
  -e TLS_VERIFY=false \
  --name highlight2api \
  ghcr.io/jhhgiyv/highlight2api:latest
```

## 📝 获取 API Key

部署完成后，打开 `http://你的服务器IP:8080/highlight_login` 根据页面提示获取 API Key。

## 🎯 特性

- ✅ 完全兼容 OpenAI API 格式
- ✅ 支持流式和非流式响应
- ✅ 支持图片上传和分析
- ✅ 支持工具调用 (Function Calling)
- ✅ 自动处理认证和令牌刷新
- ✅ 内置文件缓存机制
- ✅ 支持多模态对话

## 环境变量配置

| 环境变量          | 默认值     | 说明          |
|---------------|---------|-------------|
| `TLS_VERIFY`  | `True`  | 是否验证 TLS 证书 |
| `DEBUG`       | `False` | 是否开启调试模式    |
| `MAX_RETRIES` | `1`     | 最大重试次数      |


