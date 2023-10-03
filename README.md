# PixivCrawler

## 实现功能

- [x] 下载周榜、日榜、月榜的图片

- [x] 下载搜索的图片

- [ ] 下载某画师的图片

- [ ] 图形界面

- [x] 显示下载进度（暂且使用rich.progress库）

- [ ] 多线程下载

## 关于HERADERS

只需要两行

```json
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ",
    "Cookie": LOGIN_COOKIE
}
```

但在下载图片时需要referer，让pixiv以为我们是通过pixiv官网访问图片的

```json
DOWNLOAD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ",
    "Cookie": LOGIN_COOKIE
    "referer": "referer of artworks"
}
```

# 关于LOGIN_COOKIE

登录www.pixiv.net，并打开开发者模式。

在网络（network）中搜索www.pixiv.net，打开后标头-Cookie的内容便是LOGIN_COOKIE


