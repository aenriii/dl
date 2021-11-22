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