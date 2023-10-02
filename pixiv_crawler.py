import requests
from time import sleep
from settings import *

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ",
    "Cookie": LOGIN_COOKIE
}

# artwork = {
#     "title": "",
#     "user_name": "",
#     "p_id": "",
#     "referer": ""
# }


def get_weekly_artworks(page=1, num=0):
    res = requests.get(
        f"https://www.pixiv.net/ranking.php?mode=weekly&p={page}&format=json")
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


# An artwork has one or more than one pictures
def get_image_urls(artwork):
    res_artwork = requests.get(
        f"https://www.pixiv.net/ajax/illust/{artwork['p_id']}/pages?lang=zh", headers=headers,)
    artwork_datas = res_artwork.json()["body"]
    image_urls = []
    for image in artwork_datas:
        image_urls.append(image["urls"]["original"])
    return image_urls


# download one picture
def download_image(artwork, savepath="output/"):
    sleep(1)
    # if there's no referer in headers, the pixiv won't return the picture
    download_headers = headers
    download_headers["referer"] = artwork["referer"]
    image_urls = get_image_urls(artwork)
    for image_url in image_urls:
        try:
            resp_image = requests.get(image_url, headers=download_headers)
        except Exception as e:
            print(e)
            return
        file_name = image_url.split("/")[-1]
        with open(savepath+file_name, "wb") as file:
            file.write(resp_image.content)
    print(f"Download {artwork['title']} successfully!")


if __name__ == "__main__":
    artworks = get_weekly_artworks(1, 10)
    urls = []
    for artwork in artworks:
        download_image(artwork, "output/weekly/")
