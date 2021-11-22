from . import DownloaderOptions
from typing import List
from .internal import Job, JobOptions, Logger
from dataclasses import field
# abstract
class DefaultDownloader:
    discoveryJobOptions: JobOptions
    retrieveJobOptions: JobOptions
    discoveryJob: Job
    retrieveJob: Job
    http_client: Session = Session()
    base_headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko), Chrome/91.0.4472.124 Safari/537.36"
    }

    l: Logger = field(Logger())
    def __init__(this, tags_str: str, options: DownloaderOptions):
        this.options = options
        this.tags = this.processTags(tags_str)
        this.setJobs()
    def setJobs(this):
        return # Defined by inherited classes, abstract.
    def runJobs(this):
        this.discoveryJob.start()
        this.retrieveJob.start()
    def processTags(self, tags_str: str) -> List[str]:
        return [""] # Defined by inherited classes, abstract.
    def get(this, uri):
        return this.http_client.get(uri, headers=this.base_headers)