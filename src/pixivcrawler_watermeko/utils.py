from concurrent.futures import ThreadPoolExecutor
import requests
from urllib3 import disable_warnings, exceptions
import re
from typing import TypedDict,List

class Artwork(TypedDict):
    title: str
    user_name: str
    p_id: str
    referer: str

HEADERS = {
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}

disable_warnings(exceptions.InsecureRequestWarning)


def set_cookie(cookie):
    HEADERS["Cookie"] = cookie

def get_title(p_id):
    """
    Get artwork title from p_id
    """
    res = requests.get(
        f"https://www.pixiv.net/artworks/{p_id}", verify=False, headers=HEADERS)
    title_match = re.search(r'<title>(.*?)</title>', res.text)
    return title_match.group(1)

# An artwork has one or more than one pictures


def get_image_urls(artwork:Artwork):
    res_artwork = requests.get(
        f"https://www.pixiv.net/ajax/illust/{artwork['p_id']}/pages?lang=zh", headers=HEADERS, verify=False)
    artwork_datas = res_artwork.json()["body"]
    image_urls = []
    for image in artwork_datas:
        image_urls.append(image["urls"]["original"])
    return image_urls


retry_list = {}
# download pictures from an artwork


def download_image(artwork:Artwork, savepath="output/", max_retry=3):
    global retry_list
    # if there's no referer in headers, the pixiv won't return the picture
    download_headers = HEADERS
    download_headers["referer"] = artwork["referer"]
    image_urls = get_image_urls(artwork)
    for image_url in image_urls:
        if not image_url in retry_list:
            retry_list[image_url] = 0
        try:
            resp_image = requests.get(
                image_url, headers=download_headers, verify=False)
        except Exception as e:
            if retry_list[image_url] < max_retry:
                print(
                    f"Failed to download {artwork['title']}.Begin to retry.Retry times:{retry_list[image_url]}")
                retry_list[image_url] += 1
                download_image(artwork, savepath, max_retry)
            else:
                print(f"Failed to download {artwork['title']}.Stop retrying.")
                del retry_list[image_url]
                return False
        file_name = image_url.split("/")[-1]
        with open(savepath+file_name, "wb") as file:
            file.write(resp_image.content)
        del retry_list[image_url]
        return True


def download_images(artworks:List[Artwork], savepath):
    with ThreadPoolExecutor(max_workers=16) as pool:
        for artwork in artworks:
            pool.submit(download_image, artwork, savepath)
