import grpc
import logging
import asyncio
from concurrent import futures

from atomos.core import config

from identity.api.proto import identity_pb2_grpc
from identity.api.grpc import identity_servicer

logger = logging.getLogger(__name__)


async def serve():
    logger.info(f'initializing gRPC server on address {config.API_HOST}:{config.API_PORT}')

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register identity service
    identity_pb2_grpc.add_IdentityServicer_to_server(identity_servicer.IdentityServicer(), server)

    server.add_insecure_port(f'{config.API_HOST}:{config.API_PORT}')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
