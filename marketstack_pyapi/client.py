import logging
import os

import requests
from attrs import Factory, define, field
from requests.exceptions import HTTPError

from .exceptions import MissingAPIKeyException, RestClientException
from .utils import load_env_variables


@define
class BaseRestClient:
    base_url: str = ""
    config: dict = Factory(dict)
    headers: dict = Factory(dict)
    session: requests.Session = Factory(requests.Session)

    def __repr__(self):
        return f"{self.__class__.__name__}(base_url='{self.base_url}'"

    __str__ = __repr__

    def _request(self, method: str, url: str, **kwargs):
        response = self.session.request(method, f"{self.base_url}/{url}", headers=self.headers, **kwargs)

        try:
            response.raise_for_status()
        except HTTPError as e:
            logging.error(response.content)
            raise RestClientException(e) from e
        return response


@define
class MarketStackRestClient(BaseRestClient):
    base_url: str = "https://api.marketstack.com/v1"
    access_key: str = ""
    params: dict = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.params = {"access_key": get_access_key(self.access_key)}


def get_access_key(self, api_key: str = None) -> str:
    # if api_key is a passed argument to MarketStackRestClient class
    # return it
    if api_key:
        return api_key

    # if api_key is not passed, check environment
    env_vars = load_env_variables()
    access_key = env_vars.get("ACCESS_KEY", None) or os.getenv("ACCESS_KEY")

    # if not access_key found, return Exception
    if not access_key:
        raise MissingAPIKeyException

    return access_key
