from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from typing import Optional
from datetime import datetime
import requests


class ZohoInventoryAuthenticator(APIAuthenticatorBase):
    """API Authenticator for OAuth 2.0 flows."""

    def __init__(
        self,
        stream: RESTStreamBase,
        config_file: Optional[str] = None,
        auth_endpoint: Optional[str] = "https://accounts.zoho.com/oauth/v2/token",
    ) -> None:
        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._config_file = config_file
        self._tap = stream._tap

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.logger.info("Token is invalid. Refreshing...")
            self.update_access_token()
        result = super().auth_headers
        result[
            "Authorization"
        ] = f"Zoho-oauthtoken {self._tap._config.get('access_token')}"
        self.logger.info("Token is valid.")

        return result

    @property
    def auth_endpoint(self) -> str:
        """Get the authorization endpoint.

        Returns:
            The API authorization endpoint if it is set.

        Raises:
            ValueError: If the endpoint is not set.
        """
        if not self._auth_endpoint:
            raise ValueError("Authorization endpoint not set.")
        return self._auth_endpoint

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the API."""
        return {
            "client_id": self._tap._config["client_id"],
            "client_secret": self._tap._config["client_secret"],
            "redirect_uri": self._tap._config["redirect_uri"],
            "refresh_token": self._tap._config["refresh_token"],
            "grant_type": "refresh_token"
        }

    def is_token_valid(self) -> bool:
        now = round(datetime.utcnow().timestamp())
        expires_in = 3600
        created_at = self._tap._config.get(
            "created_at", 0
        )  # make sure it returns invalid if created_at is not there, so it can be generated

        return now < (created_at + expires_in - 60)

    @property
    def oauth_request_payload(self) -> dict:
        """Get request body.

        Returns:
            A plain (OAuth) or encrypted (JWT) request body.
        """
        return self.oauth_request_body

    # Authentication and refresh
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        auth_request_payload = self.oauth_request_payload
        self.logger.info(f"OAuth Payload: {auth_request_payload}")
        
        token_response = requests.post(self.auth_endpoint, data=auth_request_payload)
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
            self.logger.info(f"OAuth response: {token_response.json()}")
            token_last_refreshed = round(datetime.utcnow().timestamp())
        except Exception as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            )
        token_json = token_response.json()

        self._tap._config["created_at"] = token_last_refreshed
        self._tap._config["access_token"] = token_json["access_token"]