from .DefaultDownloader import DefaultDownloader
from .DownloaderOptions import DownloaderOptions
from typing import List, Dict
from urllib.parse import quote
from requests import Session
from bs4 import BeautifulSoup as bs
from pathlib import Path
from os import getcwd
from .internal import Job
class SafeBooruDownloader(DefaultDownloader):
    base_uri: str = "https://safebooru.org/"
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }
    def __init__(this, tags_str: str, options: DownloaderOptions):
        this.l.log("Entering SafeBooruDownloader.__init__")
        DefaultDownloader.__init__(this, tags_str, options)
        

        
    def processTags(this, tags_str: str) -> List[str]:
        this.l.log("Processing tags '" + tags_str + "'")
        tags = tags_str.split(" ")
        for i in range(len(tags)):
            
            try:
                this.l.log("Testing tag " + tags[i])
                if this.getPosts(1, [tags[i]]) is []:
                    this.l.log("Bad Tag: " + tags[i])
                    tags.remove(i)
                    i -= 1
            except:
                break
    def setJobs(this):
        this.l.log("Setting Jobs...")
        this.retrieveJob = Job(target=this.retrieveJobDelegate, args=(this,))
        this.discoveryJob = Job(target=this.discoveryJobDelegate, args=(this,))
    def getPosts(this, num: int = None, tags: List[str] = None):
        this.l.log("Getting", num, "posts for tags", str(tags))
        if (num is None or tags is None):
            this.l.log("None Value in getPosts")
            return this.getPosts(this.options.numPosts, this.tags)
        posts: List[Dict[str,str]] = []
        postsIterated = 0
        iterable = this.iterLinks(tags)
        while (len(posts) < num):
            this.l.log("iterating to new URL")
            currUrl = next(iterable)
            cPostsIterated = postsIterated
            for post in this.getPostInformationByUri(currUrl):
                postsIterated += 1
                this.l.log("Iterating to new post, post number", postsIterated)
                if(this.isAllowed(this.parseRating(post["title"]))):
                    this.l.log("Post", postsIterated, "is allowed; pushing to internal queue")
                    posts.append({"uri": this.getImageUriFromPostUri(this.base_uri + post["href"]), "title": post["id"]})
            if cPostsIterated == postsIterated:
                break
        return posts
    def postGenerator(this, tags: List[str] = None):
        if (tags is None and tags != this.tags):
            this.l.log("postGenerator called with None tags!")
            return this.postGenerator(this.tags)
        postsIterated = 0
        iterable = this.iterLinks(tags)
        while (True):
            currUrl = next(iterable)
            cPostsIterated = postsIterated
            for post in this.getPostInformationByUri(currUrl):
                postsIterated += 1
                if(this.isAllowed(this.parseRating(post["title"]))):
                    this.l.log("Yielding image uri.")
                    yield {"uri": this.getImageUriFromPostUri(this.base_uri + post["href"]), "title": post["id"]}
            if cPostsIterated == postsIterated:
                break
                
            

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

    # SECTION: Job definitons
    def discoveryJobDelegate(this, *args):
        this.retrieveJobOptions.doRunDownload = True
        for each in this.postGenerator(this.tags):
            this.imageQueue.put(each)
            this.discoveryJobOptions.progressCurr += 1
            
    def retrieveJobDelegate(this, *args):
        
        while (True):
            this.l.log("Awaiting post. - retrieveJob")
            post = this.imageQueue.get()
            this.l.log("Retrieved post - retrieveJob")
            # Write binary data of image to outputDirectory/title[1:].(uri.split(".")[-1])
            with open(Path(getcwd()).joinpath(this.options.outputDirectory, post.title[1:] + "." + post.uri.split(".")[-1]), "wb") as f:
                this.l.log("Saving post - retrieveJob")
                f.write(this.get(post.uri).raw)
                this.retrieveJobOptions.progressCurr += 1
            if not this.retrieveJobOptions.doRunDownload:
                break
                

            

        