import os.path

from urllib.parse import urlparse

def fake_apicall(url):
    """
    A stub urlopen() implementation that load json responses from
    the filesystem.
    """
    # Map path from url to a file
    parsed_url = urlparse(request.get_full_url())
    resource_file = os.path.normpath('tests/resources%s' % parsed_url.path)
    # Must return a file-like object
    try:
        return open(resource_file, mode='rb')
    except IOError:
        raise HTTPError(request.get_full_url, 404,
                        "HTTP Error 404: Not Found", {}, None)


