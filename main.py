from downloaders import SafeBooruDownloader, DownloaderOptions
from dataclasses import dataclass
@dataclass
class App:
    options: DownloaderOptions
    def safebooru(this, tagstr):
        SafeBooruDownloader(tagstr, this.options).runJobs()
    s, sb, safe = safebooru, safebooru, safebooru 

SafeBooruDownloader("skirt", DownloaderOptions(True, True, False, 1, "./out", True)).runJobs()