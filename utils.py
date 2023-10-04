from time import sleep
import requests
from settings import HEADERS

# Structure of artwork
# artwork = {
#     "title": "",
#     "user_name": "",
#     "p_id": "",
#     "referer": ""
# }

# An artwork has one or more than one pictures
def get_image_urls(artwork):
    res_artwork = requests.get(
        f"https://www.pixiv.net/ajax/illust/{artwork['p_id']}/pages?lang=zh", headers=HEADERS,)
    artwork_datas = res_artwork.json()["body"]
    image_urls = []
    for image in artwork_datas:
        image_urls.append(image["urls"]["original"])
    return image_urls


# download pictures from an artwork
def download_image(artwork, savepath="output/"):
    sleep(1)
    # if there's no referer in headers, the pixiv won't return the picture
    download_headers = HEADERS
    download_headers["referer"] = artwork["referer"]
    image_urls = get_image_urls(artwork)
    for image_url in image_urls:
        try:
            resp_image = requests.get(image_url, headers=download_headers)
        except Exception as e:
            print(f"Failed to download {artwork['title']} due to {e}")
            return
        file_name = image_url.split("/")[-1]
        with open(savepath+file_name, "wb") as file:
            file.write(resp_image.content)


