from setuptools import setup, find_packages

setup(
    name='pixiv-crawler',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='watermeko',
    description='Crawl pixiv pictures',
    url='https://github.com/watermeko/PixivCrawler',
)
