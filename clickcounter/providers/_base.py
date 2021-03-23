import requests


class BaseProvider:
    headers = {}

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def login(self, *args, **kwargs):
        pass

    def register_url(self, *args, **kwargs):
        raise NotImplementedError()

    def get_visits(self, *args, **kwargs):
        raise NotImplementedError()

    def get_all_visits(self, *args, **kwargs):
        raise NotImplementedError()

    def make_visit(self, track_url):
        return self.session.get(track_url)
