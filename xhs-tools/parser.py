import requests
from bs4 import BeautifulSoup

def parse_article_from_url(url):
    resp = requests.get(url, timeout=10)
    resp.encoding = resp.apparent_encoding
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    # 简单适配主流平台
    if 'csdn.net' in url:
        title = soup.find('h1').get_text(strip=True)
        content = '\n'.join([p.get_text() for p in soup.select('.blog-content-box p')])
    elif 'jianshu.com' in url:
        title = soup.find('h1').get_text(strip=True)
        content = '\n'.join([p.get_text() for p in soup.select('article p')])
    elif 'zhihu.com' in url:
        title = soup.find('h1').get_text(strip=True)
        content = '\n'.join([p.get_text() for p in soup.select('div.RichContent-inner p')])
    else:
        # 通用提取
        title = soup.title.get_text(strip=True) if soup.title else '未识别标题'
        content = '\n'.join([p.get_text() for p in soup.find_all('p')])
    return title, content 