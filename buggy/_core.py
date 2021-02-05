# built-in
from typing import Dict, Optional
from urllib.parse import urlparse

# external
import requests


URL = 'https://pypi.org/pypi/{}/json'
KNOWN = frozenset({'github.com', 'gitlab.com', 'bitbucket.org'})


def get_links(name: str) -> Dict[str, str]:
    response = requests.get(URL.format(name))
    response.raise_for_status()
    response.json()
    return response.json()['info']['project_urls']


def get_tracker_url(links: Dict[str, str]) -> Optional[str]:
    # try to find github or gitlab url and use it as a bug tracker
    for url in links.values():
        if not url.startswith('http'):
            url = 'https://' + url
        parsed = urlparse(url)
        if parsed.hostname not in KNOWN:
            continue

        # build URL
        parts = parsed.path.strip('/').split('/')
        if len(parts) < 2:
            continue
        url = 'https://{}/{}/{}/issues/new'.format(parsed.hostname, *parts)

        # check that issues aren't disabled for the project
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 404:
            continue
        return url

    # try to find custom bug tracker by name
    for name, url in links.items():
        if 'tracker' not in name.lower():
            continue
        if not url.startswith('http'):
            url = 'https://' + url
        return url

    return None
