import timeit
from urllib.request import urlretrieve
from downloaders.download import DownloadableFile
from hashlib import sha256
def downloadTest():
    DownloadableFile("http://speedtest.belwue.net/100M", "temp/bmf.dab").download()


def downloadTest2():
    urlretrieve("http://speedtest.belwue.net/100M", "temp/bmf.dab")

expected_sum = "20492a4d0d84f8beb1767f6616229f85d44c2827b64bdbfb260ee12fa1109e0e"
filename = "temp/bmf.dab"
time_dl1 = timeit.Timer("downloadTest()", globals=locals()).timeit(10) / 10
print("DownloadableFile method took " + str(time_dl1) + " seconds per iteration, which is " + str(100 / time_dl1) + "MB/s")
sha256_hash = sha256()
with open(filename,"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    if sha256_hash.hexdigest() == expected_sum:
        print("DownloadableFile DID download the file correctly.")
    else:
        print("DownloadableFile DID NOT download the file correctly.")


time_dl2 = timeit.Timer("downloadTest2()", globals=locals()).timeit(10) / 10
print("urlretrieve method took " + str(time_dl2) + " seconds per iteration, which is " + str(100 / time_dl2) + "MB/s")
sha256_hash = sha256()
with open(filename,"rb") as f:
    # Read and update hash string value in blocks of 4K
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    if sha256_hash.hexdigest() == expected_sum:
        print("urlretrieve DID download the file correctly.")
    else:
        print("urlretrieve DID NOT download the file correctly.")