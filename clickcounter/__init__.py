from clickcounter.providers.shorturl_at import ShortUrlAt
from clickcounter.providers.linkclickcounter_com import LinkClickCounterCom

providers = {
    "shorturl.at": ShortUrlAt,
    "linkclickcounter.com": LinkClickCounterCom
}

_default_provider_singleton = ShortUrlAt()

register_url = _default_provider_singleton.register_url

get_visits = _default_provider_singleton.get_visits

make_visit = _default_provider_singleton.make_visit
