#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取服务器IP地址的跨平台脚本
"""

import subprocess
import socket
import platform

def get_server_ip():
    """获取服务器主要IP地址"""
    try:
        # 方法1: 获取连接外网时使用的IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        pass
    
    try:
        # 方法2: Linux系统使用hostname命令
        if platform.system() == "Linux":
            result = subprocess.check_output(['hostname', '-I'], timeout=5)
            return result.decode().strip().split()[0]
    except:
        pass
    
    try:
        # 方法3: 获取本机IP
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        pass
    
    # 默认返回localhost
    return "localhost"

if __name__ == "__main__":
    print(get_server_ip())
