"""应用配置"""
import os
import sys

from loguru import logger

from app.utils import decode_base64url_safe

# Highlight AI 配置
HIGHLIGHT_BASE_URL = "https://chat-backend.highlightai.com"
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Highlight/1.3.61 Chrome/132.0.6834.210 Electron/34.5.8 Safari/537.36"
USER_AGENT = decode_base64url_safe(os.environ.get("HIGHLIGHT_USER_AGENT",
                                                     "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgSGlnaGxpZ2h0LzEuMy42MSBDaHJvbWUvMTMyLjAuNjgzNC4yMTAgRWxlY3Ryb24vMzQuNS44IFNhZmFyaS81MzcuMzY")).decode("utf-8")

# 网络配置
TLS_VERIFY = os.environ.get("TLS_VERIFY", 'True').lower() == "true"

DEBUG = os.environ.get("DEBUG", 'False').lower() == "true"
if not DEBUG:
    logger.remove()
    logger.add(sys.stdout, level="INFO")

MAX_RETRIES = int(os.environ.get("MAX_RETRIES", '1'))
