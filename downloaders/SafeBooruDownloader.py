from . import DefaultDownloader
from typing import List, Dict
from urllib import quote
from requests import Session
class SafeBooruDownloader(DefaultDownloader):
    base_uri: str = "https://safebooru.org/"
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }
    def __init__(this, tags_str: str, options: DownloaderOptions):
        super.__init__(this, tags_str, options)
        
    def processTags(this, tags_str: str) -> List[str]:
        tags = tags_str.split(" ")
        for i in range(len(tags)):
            try:
                if this.getPosts(1, [tags[i]]) is None:
                    tags.remove(i)
                    i -= 1
            except:
                break
    def getPosts(this, num: int = None, tags: List[str] = None):
        if (num is None or tags is None):
            return this.getPosts(this.options.numPosts, this.tags)
        posts: List[str] = []
        iterable = this.iterLinks(tags)
        while (len(posts) < num):
            currUrl = next(iterable)
            for post in this.getPostInformationByUri(currUrl):
                pass
    def iterLinks(this, tags: List[str] = []):
        index = 0
        uri_tags_piece = "+".join([quote(i) for i in tags])
        while True:
            currUri = this.base_uri + "index.php?page=post&s=list&tags=" + uri_tags_piece
            if index == 0:
                yield currUri
            else:
                yield currUri + "&pid=" + str(index)
            index += 40
    def getPostInformationByUri(this, uri: str):
        