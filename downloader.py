import os
import requests
from clint.textui import progress

DOWNLOADS_DIR = '/Users/alvinlee/Downloads/python-downloader/'
DOWNLOAD_URL_LIST = 'cs50_result.txt'


def getOutputFilePath(dir, name):
    return os.path.join(dir, name)

def downloadFile(downloadOutputPath, url):
    r = requests.get(url, stream=True)
    with open(downloadOutputPath, "wb") as downloadStream:
        print('Downloading from url: %s' % url)
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size = 2391975), expected_size=(total_length/1024) + 1):
            if ch:
                downloadStream.write(ch)

# For every line in the file
for url in open(DOWNLOAD_URL_LIST):
    # Split on the rightmost / and take everything on the right side of that
    name = url.rsplit('/', 1)[-1]
    # Combine the name and the downloads directory to get the local filename
    filename = getOutputFilePath(DOWNLOADS_DIR, name)
    if not os.path.isfile(filename):
        downloadFile(filename, url)
    # # Download the file if it does not exist
    #     urllib3.urlretrieve(url, filename)


