import grpc
from typing import Union

AUTH_HEADER = 'rpc-auth-header'


class AuthInterceptor(grpc.ServerInterceptor):
    def __int__(self, key: Union[str, int]):
        self._valid_metadata = (AUTH_HEADER, key)

        def deny(_, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'invalid key')

        self._deny = grpc.unary_unary_rpc_method_handler(deny)

    def intercept_service(self, continuation, handler_call_details):
        meta = handler_call_details.invocation_metadata

        if meta and meta[0] == self._valid_metadata:
            return continuation(handler_call_details)
        else:
            return self._deny
