from .downloaders import SafeBooruDownloader, DownloaderOptions
@dataclass
class App:
    options: DownloaderOptions
    def safebooru(this, tagstr):
        SafeBooruDownloader(tagstr, this.options).runJobs()
    s, sb, safe = safebooru, safebooru, safebooru 

