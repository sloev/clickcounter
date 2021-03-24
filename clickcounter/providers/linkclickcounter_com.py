import time
from clickcounter.providers._base import BaseProvider
from clickcounter import _utils


REGISTER_URL = "https://www.linkclickcounter.com/createShortURL.php"

LOGIN_URL = "https://www.linkclickcounter.com/login.php"
ACCOUNT_URL = "https://www.linkclickcounter.com/userAccount.php"
ANALYTICS_URL_TEMPLATE = "https://www.linkclickcounter.com/monitoring.php"


class LinkClickCounterCom(BaseProvider):
    def login(self, email, password):
        if None in [email, password]:
            raise AttributeError("email or password can't be None")
        self.session.get(LOGIN_URL)

        response = self.session.post(
            ACCOUNT_URL,
            data={
                "email": email,
                "password": password,
                "rememberMe": 1,
                "loginSubmit": "Sign In",
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
            allow_redirects=True,
        )
        response.raise_for_status()
        if "Logout" not in response.text:
            raise RuntimeError("error logging in")

    def register_url(self, url):
        self.session.get(ANALYTICS_URL_TEMPLATE)
        self.session.post(
            REGISTER_URL,
            data={
                "inner_url": url,
                "url_tag_name": None,
                "shortened_domain": 19,
                "innerURLSubmit": "START MONITORING !",
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
        ).text

        rows = self._get_raw_rows()
        selected_row = [r for r in rows if r["Monitored URL"] == url]
        if not selected_row:
            raise RuntimeError("error creating monitoring url")
        return selected_row[0]["Shorten URL"]

    def get_visits(self, track_url):
        all_visits = self.get_all_visits()
        track_url_count = all_visits.get(track_url)
        if track_url_count is None:
            raise KeyError(f"{track_url} not found amongst rows: {all_visits}")
        return track_url_count

    def get_all_visits(self):
        rows = self._get_raw_rows()
        return {r["Shorten URL"]: int(r["Clicks Counter"]) for r in rows}

    def _get_raw_rows(self, max_tries=2):
        response = None
        html = None
        for try_number in range(1, max_tries + 1):
            try:
                response = self.session.get(ANALYTICS_URL_TEMPLATE)
                html = response.content
                return _utils.extract_table_rows_from_html_string(html)
            except:
                if try_number >= max_tries:
                    raise Exception(
                        f"Error during fetch of monitoring rows, last response: {response}, html:{html}"
                    )
            time.sleep(try_number)
