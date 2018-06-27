__author__ = "紫羽"
import urllib.request as ur
import requests
from bs4 import BeautifulSoup

# 构建请求头
def __web_headers():
    import random
    user_Agent = [
        'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 64.0.3282.186Safari / 537.36',
        'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 64.0.3282.140Safari / 537.36Edge / 17.17134'
    ]
    user_agent = random.choice(user_Agent)
    # 构建sesson对象
    sesso = requests.session()

    header = {
        'user-Agent': user_agent
    }
    return header

def __get_seeion(url):
    sees = requests.session()
    html = sees.get(url, headers=__web_headers()).text
    print(html)
    bs = BeautifulSoup(html, 'lxml')
    _xsrf = bs.find('title')
    return _xsrf

def loadpage(url):
    """
    加载页面
    返回对象
    :param url:
    :param code:
    :return:
    """

    header = __web_headers()
    __get_seeion(url)
    request = ur.Request(url, headers=header)
    response = ur.urlopen(request)
    html = response.read()
    return html

def savehtml(html):
    import re
    pattern = r'<title>(.*)</title>'
    try:
        filename = re.search(pattern, html).group(1)+'.html'
    except:
        filename = '1'
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(html.decode('utf-8'))

def json_text(html):
    import json
    import jsonpath
    unicodestr = json.loads(html)
    str_list = jsonpath.jsonpath(unicodestr,'$..name')
    for item in str_list:
        print(item)