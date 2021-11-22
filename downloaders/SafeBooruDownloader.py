from . import DefaultDownloader
from typing import List
class SafeBooruDownloader(DefaultDownloader):
    base_uri: str = "https://safebooru.org/"
    def processTags(this, tags_str: str) -> List[str]:
        tags = tags_str.split(" ")
        for tag in tags:
            if this.getPosts(1, [tag]) is None:
                tags.re