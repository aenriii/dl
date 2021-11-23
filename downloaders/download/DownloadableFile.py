from pathlib import Path
from requests import get, head
from threading import Thread
from typing import List
from queue import Queue
from io import FileIO


class DownloadableFile:
    uri: str
    downloadTo: str
    overwrite: bool
    stop: bool
    headThread: Thread
    parts: List[str]
    binparts: List[Queue]
    latestCompleted: int
    openFile: FileIO

    def __init__(self, uri: str, downloadTo: str, overwrite: bool = True):
        self.uri = uri
        self.downloadTo = downloadTo
        self.overwrite = overwrite
        self.stop = False
        self.headThread = Thread(target=self.head)
        self.headThread.run()
        self.binparts = []
        self.latestCompleted = 0

    def assertPathExists(self):
        f = Path(self.downloadTo)
        if not f.parent.exists():
            f.parent.mkdir(parents=True)
        if f.exists() and not self.overwrite:
            raise FileExistsError(
                "DownloadableFile with position set to " + self.downloadTo + " encountered an error: File exists and self.overwrite set to False.")

    def head(self):
        res = head(self.uri)
        if int(res.headers["Content-Length"]) > 5 * 1024 * 1024 and "Accept-Ranges" in res.headers and res.headers[
            "Accept-Ranges"] == "bytes":
            parts = self.iterParts(int(res.headers["Content-Length"]))
        else:
            parts = ["0-" + res.headers["Content-Length"]]
        self.parts = parts
        print(str(len(parts)) + " parts...")

    def _downloadRange(self, range: str, id: int):
        print(range)
        x = 0
        mem = get(self.uri, headers={"Range": "bytes=" + range})
        if id:
            self.binparts[id - 1].join()
        print("filling file part " + str(id))
        for chunk in mem.iter_content(chunk_size=4 * 1024):
            self.openFile.write(chunk)

        self.latestCompleted = id
        print("download part " + str(id) + " completed")

    def iterParts(self, length):
        partnum = int(length / 5 * 1024 * 1024)
        if partnum > 8:
            partnum = 8
        partsize = int(length / partnum)
        return [str(i - partsize) + "-" + str(i - 1) for i in range(partsize, length + 1 - partsize, partsize)] + [
            str(length - partsize) + "-" + str(length)]

    def download(self):
        if self.headThread.is_alive():
            self.headThread.join()
        self.assertPathExists()
        self.openFile = open(self.downloadTo, "wb", buffering=0)
        for i in range(len(self.parts)):
            t = Thread(target=self._downloadRange, args=(self.parts[i], i))
            self.binparts.append(t)
            t.start()
        for t in self.binparts:
            if t.is_alive():
                t.join()
        self.openFile.close()

    def downloadThreaded(self):
        Thread(target=self.download).start()