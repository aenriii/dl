from dataclasses import dataclass, field

@dataclass()
class JobOptions():
    doRunDownload: bool = field(True)
    doShowsProgress: bool = field(True)
    doProgressMax: bool = field(True)
    progressCurr: int
    progressMax: int
