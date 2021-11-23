from downloaders import SafeBooruDownloader, DownloaderOptions, GelbooruDownloader
from dataclasses import dataclass
from downloaders.download import DownloadableFile


@dataclass
class App:
    options: DownloaderOptions

    def safebooru(this, tag_str):
        SafeBooruDownloader(tag_str, this.options).runJobs()

    s, sb, safe = safebooru, safebooru, safebooru


a = GelbooruDownloader("tail", DownloaderOptions(True, True, False, 5, "//barracks/tail", False))


