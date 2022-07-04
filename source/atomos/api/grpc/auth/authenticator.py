import grpc
from typing import Union

from atomos.api.grpc.auth.auth_interceptor import AUTH_HEADER


class Authenticator(grpc.AuthMetadataContext):
    def __int__(self, key: Union[str, int]):
        self._key = key

    def __call__(self, context, callback):
        callback(((AUTH_HEADER, self._key),), None)
