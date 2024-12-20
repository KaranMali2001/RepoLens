from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
import requests
import os


class ClerkTokenVerifier:
    def __init__(self):
        self.clerk_issuer_url = os.environ.get("clerk_issuer_url")
        self.clerk_jwks_url = os.environ.get("clerk_jwks_url")
        self.clerk_app_id = os.environ.get("clerk_app_id")
        self.security_scheme = HTTPBearer()

        self._jwks = None

    def _get_signing_key(self, token_headers):

        if self._jwks is None:

            response = requests.get(self.clerk_jwks_url)
            response.raise_for_status()

            jwks = response.json()

        for key in jwks.get("keys", []):

            jwks_key: str = key.get("kid")
            token_headers_key: str = token_headers.get("kid")
            print("jwks_key", jwks_key)
            if jwks_key == token_headers_key:

                return key
        raise HTTPException(
            status_code=401, detail="Unable to find matching signing key"
        )

    def verify_token(
        self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ):
        token = credentials.credentials
        print("verifying token .....")

        try:
            unverified_headers = jwt.get_unverified_header(token)
            signing_key = self._get_signing_key(unverified_headers)

            payload = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                options={"verify_aud": True, "verify_iss": True},
                audience=self.clerk_app_id,
                issuer=self.clerk_issuer_url,
            )
            print("token verifed successfully")
            return payload
        except JWTError as e:
            raise HTTPException(status_code=404, detail=f"Invalid token: {str(e)}")
