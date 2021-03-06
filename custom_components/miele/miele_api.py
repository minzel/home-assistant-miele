from typing import Tuple, List, Optional, Union, Callable, Dict, Any

from requests import Response
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

from .model import Device

BASE_URL = "https://api.mcs3.miele.com/v1"

MIELE_OAUTH = "https://api.mcs3.miele.com/thirdparty/login"
MIELE_TOKEN = "https://api.mcs3.miele.com/thirdparty/token"
MIELE_REFRESH = "https://api.mcs3.miele.com/thirdparty/token"


class MieleApi:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: Optional[str] = None,
        token: Optional[Dict[str, str]] = None,
        token_updater: Optional[Callable[[str], None]] = None,
    ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.token_updater = token_updater

        extra = {"client_id": self.client_id, "client_secret": self.client_secret}

        self._oauth = OAuth2Session(
            client_id=client_id,
            token=token,
            redirect_uri=redirect_uri,
            auto_refresh_kwargs=extra,
            token_updater=token_updater,
        )

    def get_devices(self, language) -> List[Device]:
        r = self.get("/devices/?language=" + language)
        r.raise_for_status()
        return [Device(k, **d) for k, d in r.json().items()]

    def get(self, path: str) -> Response:
        return self._request("get", path)

    def post(self, path: str, *, json: Dict[str, Any]) -> Response:
        return self._request("post", path, json=json)

    def get_authorization_url(self, state: Optional[str] = None) -> Tuple[str, str]:
        return self._oauth.authorization_url(MIELE_OAUTH, state)

    def request_token(
        self, authorization_response: Optional[str] = None, code: Optional[str] = None
    ) -> Dict[str, str]:
        return self._oauth.fetch_token(
            MIELE_TOKEN,
            authorization_response=authorization_response,
            code=code,
            client_secret=self.client_secret,
        )

    def refresh_tokens(self) -> Dict[str, Union[str, int]]:
        token = self._oauth.refresh_token(MIELE_REFRESH)

        if self.token_updater is not None:
            self.token_updater(token)

        return token

    def _request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Make a request.
        We don't use the built-in token refresh mechanism of OAuth2 session because
        we want to allow overriding the token refresh logic.
        """
        url = BASE_URL + path
        try:
            return getattr(self._oauth, method)(url, **kwargs)
        except TokenExpiredError:
            self._oauth.token = self.refresh_tokens()

            return getattr(self._oauth, method)(url, **kwargs)
