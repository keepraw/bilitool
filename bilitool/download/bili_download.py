# Copyright (c) 2025 bilitool

import requests
import time
import sys
from tqdm import tqdm
from ..model.model import Model


class BiliDownloader:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.config = {
            "download": {
                "video": True,
                "cover": True,
            }
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_cid(self, bvid):
        url = "https://api.bilibili.com/x/player/pagelist?bvid=" + bvid
        response = requests.get(url, headers=self.headers)
        return response.json()["data"]

    def get_bvid_video(self, bvid, cid, name_raw="video"):
        url = (
            "https://api.bilibili.com/x/player/playurl?cid="
            + str(cid)
            + "&bvid="
            + bvid
            + "&qn="
            + str(self.config["download"]["quality"])
        )
        name = name_raw + ".mp4"
        response = None
        response = requests.get(url, headers=self.headers)
        video_url = response.json()["data"]["durl"][0]["url"]
        self.download_video(video_url, name)

    def download_video(self, cid, name_raw="video"):
        if self.config["download"]["video"]:
            self.logger.info(f"Begin download video")
            video_url = "https://api.bilibili.com/x/player/playurl"
            params = {
                "cid": cid,
                "qn": 80,
                "fnval": 16,
                "fnver": 0,
                "fourk": 1,
            }
            response = requests.get(video_url, params=params, headers=self.headers)
            data = response.json()
            if data["code"] == 0:
                video_url = data["data"]["durl"][0]["url"]
                response = requests.get(video_url, headers=self.headers)
                with open(name_raw + ".flv", "wb") as file:
                    file.write(response.content)
                self.logger.info(f"Successfully downloaded video")
            else:
                self.logger.error(f"Failed to download video: {data['message']}")

    def download_cover(self, cid, name_raw="video"):
        if self.config["download"]["cover"]:
            self.logger.info(f"Begin download cover")
            cover_url = "https://api.bilibili.com/x/web-interface/view"
            params = {"cid": cid}
            response = requests.get(cover_url, params=params, headers=self.headers)
            data = response.json()
            if data["code"] == 0:
                cover_url = data["data"]["pic"]
                response = requests.get(cover_url, headers=self.headers)
                with open(name_raw + ".jpg", "wb") as file:
                    file.write(response.content)
                self.logger.info(f"Successfully downloaded cover")
            else:
                self.logger.error(f"Failed to download cover: {data['message']}")
