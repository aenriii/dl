from dataclasses import dataclass

@dataclass
class DownloaderOptions:
    safe: bool
    questionable: bool
    explicit: bool
    numPosts: int
    outputDirectory: str
    simulate: bool