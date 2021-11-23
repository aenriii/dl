from .DefaultDownloader import DefaultDownloader
from .DownloaderOptions import DownloaderOptions
from typing import List, Dict
from urllib.parse import quote
from requests import Session
from bs4 import BeautifulSoup as bs
from pathlib import Path
from os import getcwd
from .download import DownloadableFile
from urllib.request import urlretrieve
from threading import Thread

class KonachanDownloader(DefaultDownloader):
    base_uri: str = "https://konachan.com/"
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }

    def __init__(self, tags_str: str, options: DownloaderOptions):
        self.l.log("Entering KonachanDownloader.__init__")
        DefaultDownloader.__init__(self, tags_str, options)
        self.doDownload()

    def processTags(self, tags_str: str) -> List[str]:
        self.l.log("Processing tags '" + tags_str + "'")
        tags = tags_str.split(" ")
        for i in range(len(tags)):

            try:
                self.l.log("Testing tag " + tags[i])
                if not self.getPosts(1, [tags[i]]):
                    self.l.log("Bad Tag: " + tags[i])
                    tags.remove(i)
                    i -= 1
            except Exception as e:
                self.l.log(e.__str__() + " ERROR")
                break
        return tags

    def getPosts(self, num: int = None, tags: List[str] = None):
        self.l.log("Getting", num, "posts for tags", str(tags))
        if num is None or tags is None:
            self.l.log("None Value in getPosts")
            return self.getPosts(self.options.numPosts, self.tags)
        posts: List[Dict[str, str]] = []
        iterable = self.postGenerator(tags)
        while len(posts) < num:
            posts.append(next(iterable))

        return posts

    def postGenerator(self, tags: List[str]):
        if tags is None and tags != self.tags:
            self.l.log("postGenerator called with None tags!")
            return self.postGenerator(self.tags)
        postsIterated = 0
        iterable = self.iterLinks(tags)
        if iterable is None:
            self.l.log("Iterable is NONE!")
            raise UnboundLocalError("Iterable is NONE!")
        while True:
            currUrl = next(iterable)
            cPostsIterated = postsIterated
            for post in self.getPostInformationByUri(currUrl):
                postsIterated += 1
                if self.isAllowed(self.parseRating(post["alt"])):
                    self.l.log("Yielding image uri: " + post["href"])
                    yield {"uri": post["href"], "title": post["href"].split("/")[-2]}
            if cPostsIterated == postsIterated:
                break

    def iterLinks(self, tags: List[str] = []):
        index = 1
        uri_tags_piece = "+".join([quote(i) for i in tags])
        while True:
            currUri = self.base_uri + "post?tags=" + uri_tags_piece
            if index == 1:
                yield currUri
            else:
                yield currUri + "&page=" + str(index)
            index += 1

    def getPostInformationByUri(self, uri: str):
        html = bs(self.get(uri).text, features="html5lib")
        self.l.log("Parsing information from post")
        if len(html.select("#content div h1")) != 0:
            self.l.log("Tag claims invalid, " + html.select("#content div h1")[0].text)
            return []
        for post in html.select("li[id^=p]"):
            self.l.log("Yielding attributes.")
            postattrs:dict= post.select(".inner a.thumb img")[0].attrs
            postattrs.pop("class")
            yield dict({"alt": postattrs["alt"]}, **post.select("a.directlink")[0].attrs)


    def parseRating(self, containingString: str):
        x = containingString.split(" ")
        return x[x.index("Rating:")+1]


    def isAllowed(self, ratingString: str):
        return (ratingString == "Safe" and self.options.safe) or (
                    ratingString == "Questionable" and self.options.questionable) or (
                           ratingString == "Explicit" and self.options.explicit)


    def doDownload(self):
        i = 0
        for post in self.postGenerator(self.tags):
            if not i < self.options.numPosts:
                break
            i+=1
            self.l.log("Downloading", post["title"])
            p = Path(getcwd()).joinpath(self.options.outputDirectory, post["title"][1:] + '.' + post["uri"].split(".")[-1].split("?")[0])
            if not p.parent.exists():
                p.parent.mkdir(parents=True)
            Thread(target=urlretrieve, args=(post["uri"], p)).start()
