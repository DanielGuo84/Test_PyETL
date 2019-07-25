# https://2.python-requests.org/en/master/
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
url = "https://www.ptt.cc/bbs/Beauty/M.1561307799.A.4EB.html"
response = requests.get(url)
# 如果requests記得要拿.text
html = BeautifulSoup(response.text)
content = html.find("div", id="main-content")

metas = content.find_all("span", class_="article-meta-value")
print("ID:", metas[0].text)
print("看板:", metas[1].text)
category = re.match(r"\[.+\]", metas[2].text).group(0)
print("類別:", category)
print("標題:", metas[2].text)
post_time = datetime.strptime(metas[3].text, "%a %b %d %H:%M:%S %Y")
print("時間:", str(post_time))

# 你必須在刪掉前先把圖片萃取
anchors = content.find_all("a")
for a in anchors:
    img_url = a["href"]
    last = img_url.split("/")[-1]
    if "." in last and ".html" not in last:
        dir = "ptt/" + metas[2].text.replace("/", "") + "/"
        if not os.path.exists(dir):
            os.makedirs(dir)
        fp = dir + last
        img_response = requests.get(img_url, stream=True)
        # 純文字: "r", "w" + encoding
        # 非純文字: "rb", "wb"
        f = open(fp, "wb")
        # 這裡你要注意: 如果你非純文字  .raw
        f.write(img_response.raw.read())
        f.close()

# 丟掉; 盒子.extract()
metas = content.find_all("div", class_="article-metaline")
for m in metas:
    m.extract()
metas = content.find_all("div", class_="article-metaline-right")
for m in metas:
    m.extract()

score = 0
pushes = content.find_all("div", class_="push")
for p in pushes:
    tag = p.find("span", class_="push-tag").text
    if "推" in tag:
        score = score + 1
    elif "噓" in tag:
        score = score - 1
    p.extract()
print("推文分數:", score)

spans = content.find_all("span")
delete_span = ["發信站:", "編輯:", "的推文:"]
for s in spans:
    if "來自:" in s.text:
        ip = s.text.split("來自:")[-1].split(" ")[1]
    for d in delete_span:
       if d in s.text:
           s.extract()
print("IP:", ip)
print("內容:", content.text)
f = open(dir + "post.txt", "w", encoding="utf-8")
f.write(content.text)
f.close()
