from dataclasses import dataclass, field

@dataclass()
class JobOptions():
    doRunDownload: bool = field(init=True)
    doShowsProgress: bool = field(init=True)
    doProgressMax: bool = field(init=True)
    progressCurr: int = field(init=0)
    progressMax: int
