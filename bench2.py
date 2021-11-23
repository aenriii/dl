from downloaders.download import DownloadableFile
from time import time
from urllib.request import urlretrieve

def downloadTest():
    ctime = time()
    DownloadableFile("http://speedtest.belwue.net/100M", "temp/downloadablefile").download()
    print("1 iteration of DownloadableFile method costs " + str((time() - ctime)) + " secs")
def downloadTest2():
    ctime = time()
    urlretrieve("http://speedtest.belwue.net/100M", "temp/urlretrieve")
    print("1 iteration of urlretrieve method costs " + str((time() - ctime)) + " secs")
downloadTest()
downloadTest2()