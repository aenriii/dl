from . import DownloaderOptions
from typing import List, Dict
from .internal import Job, JobOptions, Logger
from dataclasses import field
from requests import Session
from queue import Queue
# abstract
class DefaultDownloader:
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }

    l: Logger = Logger("DEBUG")
    def __init__(this, tags_str: str, options: DownloaderOptions):
        this.l.log("Entering DefaultDownloader.__init__ ")
        this.options = options
        this.tags = this.processTags(tags_str)

        this.l.log("NumPosts = " + str(this.options.numPosts))
    def setJobs(this):
        return # Defined by inherited classes, abstract.
    def runJobs(this):
        this.l.log("Starting jobs...")
        this.discoveryJob.start()
        this.retrieveJob.start()
    def processTags(self, tags_str: str) -> List[str]:
        return [""] # Defined by inherited classes, abstract.
    def get(this, uri):
        this.l.log("Getting " + uri)
        return this.http_client.get(uri, headers=this.base_headers)