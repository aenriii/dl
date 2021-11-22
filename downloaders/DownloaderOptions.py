from dataclasses import dataclass

@dataclass
class DownloaderOptions:
    safe: bool
    questionable: bool
    explicit: bool
    imageCount: int
    outputDirectory: str
    simulate: bool