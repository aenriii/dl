from .DefaultDownloader import DefaultDownloader
from .DownloaderOptions import DownloaderOptions
from typing import List, Dict
from urllib.parse import quote
from requests import Session
from bs4 import BeautifulSoup as bs
class SafeBooruDownloader(DefaultDownloader):
    base_uri: str = "https://safebooru.org/"
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }
    def __init__(this, tags_str: str, options: DownloaderOptions):
        DefaultDownloader.__init__(this, tags_str, options)
        
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
        posts: List[Dict[str,str]] = []
        postsIterated = 0
        iterable = this.iterLinks(tags)
        while (len(posts) < num):
            currUrl = next(iterable)
            cPostsIterated = postsIterated
            for post in this.getPostInformationByUri(currUrl):
                postsIterated += 1
                if(this.isAllowed(this.parseRating(post["title"]))):
                    posts.append({"uri": this.getImageUriFromPostUri(this.base_uri + post["href"]), "title": post["id"]})
            if cPostsIterated == postsIterated:
                break
        print(posts[0])
        return posts
                
            

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
        html = bs(this.get(uri).text, features="html5lib")
        if len(html.select("#content div h1")) != 0:
            return []
        for post in html.select("span.thumb[id] a[id][href*=\"s=view\"]"):
            yield dict(**post.attrs, **post.select("img")[0].attrs)
    def getImageUriFromPostUri(this, postUri: str):
        html = bs(this.get(postUri).text, features="html5lib")
        # Check if is sample image.
        if "sample" in html.select("#image")[0].attrs["src"]:
            return html.select("[href*=\"image\"]")[0].attrs["href"]
        return html.select("#image")[0].attrs["src"]
    def parseRating(this, containingString: str):
        return "" # Unneeded, this is safebooru.
    def isAllowed(this, ratingString: str):
        return True # Unneeded, this is safebooru.