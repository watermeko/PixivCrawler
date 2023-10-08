import requests
import time
from urllib.parse import quote
from urllib3 import disable_warnings, exceptions
from utils import *

disable_warnings(exceptions.InsecureRequestWarning)


def get_original_artworks(page=1, num=0):
    return get_rank_artworks("original", page, num)


def get_rookie_artworks(page=1, num=0):
    return get_rank_artworks("rookie", page, num)


def get_monthly_artworks(page=1, num=0):
    return get_rank_artworks("monthly", page, num)


def get_weekly_artworks(page=1, num=0, r18=False):
    return get_rank_artworks("weekly", page, num, r18)


def get_daily_artworks(page=1, num=0, r18=False):
    return get_rank_artworks("daily", page, num, r18)


def get_daily_ai_artworks(page=1, num=0, r18=False):
    return get_rank_artworks("daily_ai", page, num, r18)


def get_rank_artworks(keyword, page=1, num=0, r18=False):
    if r18:
        res = requests.get(
            f"https://www.pixiv.net/ranking.php?mode={keyword}_r18&p={page}&format=json", headers=HEADERS, verify=False)
    else:
        res = requests.get(
            f"https://www.pixiv.net/ranking.php?mode={keyword}&p={page}&format=json", headers=HEADERS, verify=False)

    datas = res.json()["contents"]

    if (not num) or num > len(datas):
        num = len(datas)

    artworks = []
    for data in datas[0:num]:
        artwork = {
            "title": data["title"],
            "user_name": data["user_name"],
            "p_id": data["illust_id"],
            "referer": f"https://www.pixiv.net/artworks/{data['illust_id']}"
        }
        artworks.append(artwork)
    return artworks


def get_search_artworks(keyword, page=1, num=0, order="date_d", r18=False):
    """
    Prameters: 
        order(str):
            - date_d: sort by newest
            - date: sort by oldest
            - popular_d: sort by popular
    """
    if r18:
        res = requests.get(
            f"https://www.pixiv.net/ajax/search/artworks/{quote(keyword)}?word={quote(keyword)}&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh&mode=r18", headers=HEADERS, verify=False)
    else:
        res = requests.get(
            f"https://www.pixiv.net/ajax/search/artworks/{quote(keyword)}?word={quote(keyword)}&order=date_d&mode=all&p=1&s_mode=s_tag&type=all&lang=zh&mode=safe", headers=HEADERS, verify=False)

    datas = res.json()["body"]["illustManga"]["data"]

    if (not num) or num > len(datas):
        num = len(datas)

    artworks = []
    for data in datas[0:num]:
        artwork = {
            "title": data["title"],
            "user_name": data["userName"],
            "p_id": data["id"],
            "referer": f"https://www.pixiv.net/artworks/{data['id']}"
        }
        artworks.append(artwork)
    return artworks


def get_user_artworks(user_id, num=0, getTitle=False):
    """
    Parameters:
        getTitle: get title is time consuming and unstable
    """
    res = requests.get(
        f"https://www.pixiv.net/ajax/user/{user_id}/profile/all?lang=zh", verify=False, headers=HEADERS
    )
    datas = res.json()["body"]
    illusts = datas["illusts"]
    p_ids = list(illusts.keys())
    if (not num) or num > len(p_ids):
        num = len(p_ids)
    artworks = []
    for p_id in p_ids[0:num]:
        if getTitle:
            artwork = {
                "title": get_title(p_id),
                "user_name": datas["pickup"][0]["userName"],
                "p_id": p_id,
                "referer": f"https://www.pixiv.net/artworks/{p_id}"
            }
        else:
            artwork = {
                "title": "",
                "user_name": datas["pickup"][0]["userName"],
                "p_id": p_id,
                "referer": f"https://www.pixiv.net/artworks/{p_id}"
            }
        artworks.append(artwork)
    return artworks


# Test
if __name__ == "__main__":
    artworks = get_user_artworks(19076791)
    t1 = time.time()
    download_images(artworks, "output/user/")
    t2 = time.time()
    print(f"Time cost: {t2-t1}\n")
