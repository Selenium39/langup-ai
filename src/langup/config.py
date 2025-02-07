"""
全局配置，基本可以作为Uploader参数传入
"""
import os
from typing import Union

from bilibili_api import Credential


credential: Union['Credential', None] = None
work_dir = './'

tts = {
    "voice": "zh-CN-XiaoyiNeural",
    "rate": "+0%",
    "volume": "+0%",
    "voice_path": 'voice/'
}

log = {
    "handlers": ["console"],  # console打印日志到控制台, file文件存储
    "file_path": "logs/"
}

convert = {
    "audio_path": "audio/"
}

root = os.path.dirname(__file__)
openai_api_key = None  # sk-...
openai_api_base = None  # https://{your_domain}/v1
proxy = None  # 代理
debug = True

test_net = True
welcome_tip = True
