import requests
from time import sleep
import re
from settings import *

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ",
    "Cookie": COOKIE
}


def get_weekly(page=1, num=0,savepath="output/"):
    res = requests.get(
        f"https://www.pixiv.net/ranking.php?mode=weekly&p={page}&format=json")
    datas = res.json()["contents"]
    artwork_list = []
    if (not num) or num > len(datas):
        num = len(datas)
    for data in datas[0:num]:
        artwork = {
            "title": data["title"],
            "user_name": data["user_name"],
            "p_id": data["illust_id"],
            "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"
        }
        artwork_list.append(artwork)
    for artwork in artwork_list:
        urls = get_image_urls(artwork)
        for url in urls:
            download_image(url, artwork,savepath)

# An artwork has one or more than one pictures


def get_image_urls(artwork: {}):
    res_artwork = requests.get(
        f"https://www.pixiv.net/ajax/illust/{artwork['p_id']}/pages?lang=zh", headers=headers,)
    artwork_datas = res_artwork.json()["body"]
    image_urls = []
    for image in artwork_datas:
        image_urls.append(image["urls"]["original"])
    return image_urls


# download one picture
def download_image(download_url, artwork: {},savepath="output/"):
    global i
    sleep(1)
    download_headers = headers
    download_headers["referer"] = artwork["referer"]
    try:
        resp_image = requests.get(download_url, headers=download_headers)
    except Exception as e:
        print(e)
        return
    file_name = download_url.split("/")[-1]
    with open(savepath+file_name, "wb") as file:
        file.write(resp_image.content)

get_weekly(1, 10,savepath="output/weekly/")
