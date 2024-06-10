# Libraries
from urllib.request import urlopen


class Browser:
    # Attributes
    _url = ''

    # Constructors
    def __init__(self, url):
        self._url = url

    # Methods
    def get_html_from_url(self):
        page = urlopen(self._url)
        html = page.read().decode("utf-8")

        return html
