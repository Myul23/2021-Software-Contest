# 더 자세히 selenium에 대해 알고 싶다면, google, Selenium with Python

import os
import time

from selenium import webdriver
from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

# from msedge.selenium_tools import Edge, EdgeOptions

# kewords = [
#     "칠성사이다",
#     "생수병",
#     "손소독제",
#     "볼펜",
#     "마우스",
#     "테이크아웃 커피잔",
#     "잼",
#     "와인잔",
#     "유리",
#     "카스",
#     "참치캔",
#     "스위트콘",
#     "신문지",
#     "책",
#     "과자 박스",
#     "색종이",
#     "뽁뽁이",
#     "검은비닐",
#     "비닐",
# ]

kewords = ["피자박스", "치킨박스", "음료수캔"]

# ? browser option set
# 굳이 web으로의 작동을 볼 필요가 없다면 headless를 사용한다.
# Edge가 Chrome이랑 호환되는 건 알고 있었지만, 그렇다고 EdgeOptions을 안 만들었을 줄이야.
# options = EdgeOptions()
# options.use_chromium = True
# options.add_argument("--headless")
# options.add_argument("window-size=1920x1080")
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68"
# )
# browser = webdriver.Edge(options=options)
# browser = webdriver.Chrome("msedgedriver.exe", options=options)
browser = webdriver.Chrome("chromedriver.exe")
browser.maximize_window()

name = "yahoo"
# * Naver url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query="
# * Daum url = "https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q="
# * Yahoo
url = "https://images.search.yahoo.com/search/images;_ylt=Awr9Dtid09Zge2oASTpXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZANDMjAxMl8xBHNlYwNwaXZz?p="
behind = "&fr2=piv-web&fr=yfp-t"

for keword in kewords:
    # _url = url + keword
    # Yahoo
    _url = url + quote_plus(keword) + behind
    browser.get(_url)

    # ? 강제로 js 실행시키기, 지정한 위치로 스크롤 내리기
    # browser.execute_script("window.scrollTo(0, 1080)")

    interval = 2
    prev_height = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(interval)
        curr_height = browser.execute_script("return document.body.scrollHeight")

        if curr_height == prev_height:
            try:
                browser.find_element_by_name("more-res").click()
                time.sleep(interval)
            except:
                break
        prev_height = curr_height

    # screenshot
    # browser.get_screenshot_as_file("google_movie.jpg")

    soup = BeautifulSoup(browser.page_source, "lxml")
    # images = soup.find_all("img", attrs={"class": "_image"})
    # images = soup.find_all("img", attrs={"class": "thumb_img"})
    images = soup.find_all("img", attrs={"class": ""})

    # Yahoo용
    img = []
    for image in images:
        link = image["src"]
        img.append(link.split("&pid")[0])
        img = list(set(img))
    # print(img)

    if not os.path.exists("./downloads"):
        os.mkdir("./downloads")
    if not os.path.exists("./downloads/" + keword):
        os.mkdir("./downloads/" + keword)

    # for idx, image in enumerate(images):
    # Yahoo용
    for idx, imgUrl in enumerate(img):
        # - Yahoo
        # imgUrl = image["src"]
        # print(imgUrl)

        # Naver data source에 gif가 붙어있는 것들은 손을 쓸 수가 없었다.
        # if "gif" not in imgUrl:
        with urlopen(imgUrl) as f:
            with open("./downloads/" + keword + "/" + name + "_" + str(idx) + ".jpg", "wb") as h:
                img = f.read()
                h.write(img)

    print(keword + " finish")

browser.quit()
