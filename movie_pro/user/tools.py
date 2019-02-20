import json
import random
from io import StringIO

import requests



def get_ip_address(request):
    """获得请求的IP地址"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ip or request.META['REMOTE_ADDR']


def send_mobile_code(code:str, mobile:str):
    """调用手机短信三方接口-山东墨白"""
    templateId = 'TP1801025'
    headers = {"Host":"mobai.market.alicloudapi.com", "Authorization":"APPCODE b9c8d60cf919439dab918dc1cb3c1638"}
    url = f'http://mobai.market.alicloudapi.com/mobai_sms?param=code:{code}&phone={mobile}&templateId={templateId}'
    response = requests.post(url=url, headers=headers, timeout=5)
    if response.status_code == 200:
        return json.loads(response.text)


def gen_mobile_code(length=6):
    """生成指定长度的手机验证码"""
    code = StringIO()
    for _ in range(length):
        code.write(str(random.randint(0, 9)))
    return code.getvalue()



ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def gen_captcha_text(length=4):
    """生成指定长度的图片验证码文字"""
    code = StringIO()
    chars_len = len(ALL_CHARS)
    for _ in range(length):
        index = random.randrange(chars_len)
        code.write(ALL_CHARS[index])
    return code.getvalue()