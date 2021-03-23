import time
from clickcounter.providers._base import BaseProvider
from clickcounter import _utils


REGISTER_URL = 'https://www.linkclickcounter.com/createShortURL.php'

LOGIN_URL = 'https://www.linkclickcounter.com/userAccount.php'
ANALYTICS_URL_TEMPLATE = 'https://www.linkclickcounter.com/monitoring.php'


class LinkClickCounterCom(BaseProvider):
    def login(self, email, password):
        response = self.session.post(LOGIN_URL, data={
            "email": email,
            "password": password,
            "rememberMe": 1,
            "loginSubmit": "Sign In"
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()

    def register_url(self, url):
        self.session.get(ANALYTICS_URL_TEMPLATE)
        self.session.post(REGISTER_URL, data={
            "inner_url": url,
            "url_tag_name": None,
            "shortened_domain": 19,
            "innerURLSubmit": "START MONITORING !"
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'}).text

        rows = self._get_raw_rows()
        selected_row = [r for r in rows if r['Monitored URL'] == url]
        if not selected_row:
            raise RuntimeError("error creating monitoring url")
        return selected_row[0]['Shorten URL']

    def get_visits(self, track_url):
        all_visits = self.get_all_visits()
        track_url_count = all_visits.get(track_url)
        if track_url_count is None:
            raise KeyError(f"{track_url} not found amongst rows: {all_visits}")
        return track_url_count

    def get_all_visits(self):
        rows = self._get_raw_rows()
        return {r['Shorten URL']: int(r['Clicks Counter']) for r in rows}

    def _get_raw_rows(self, max_tries=5):
        response = None
        for try_number in range(1, max_tries+1):
            try:
                response = self.session.get(ANALYTICS_URL_TEMPLATE)
                return _utils.extract_table_rows_from_html_string(response.content)
            except:
                if try_number >= max_tries:
                    raise Exception(
                        f"Error during fetch of monitoring rows, last response: {response}")
            time.sleep(try_number)
