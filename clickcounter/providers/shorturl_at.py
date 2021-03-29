from clickcounter.providers._base import BaseProvider


REGISTER_URL = "https://www.shorturl.at/shortener.php"
ANALYTICS_URL_TEMPLATE = "https://www.shorturl.at/url-total-clicks.php?u={}"
TRACK_URL_TEMPLATE = "https://shorturl.at/{}"


class ShortUrlAt(BaseProvider):
    def register_url(self, url):
        self.session.get("https://www.shorturl.at/")
        response = self.session.post(
            REGISTER_URL,
            data={"u": url},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )

        url_id = response.text.split(
            "url-total-clicks.php?u=shorturl.at/")[1].split('">')[0]
        return TRACK_URL_TEMPLATE.format(url_id)

    def get_visits(self, track_url):
        analytics_url = ANALYTICS_URL_TEMPLATE.format(
            track_url.split("https://")[-1])
        response = self.session.get(analytics_url).text
        return int(response.split('<div class="squarebox"><b>')[1].split("<")[0])
