import grpc
from app.grpc_clients.streaming_pb2 import FileRequest
from app.grpc_clients.streaming_pb2_grpc import StreamingServiceStub
from app.domain_exceptions.streaming_exceptions import StreamingException
from app.core.logging import logger


class StreamingClient:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('streaming_web:50051')
        self.stub = StreamingServiceStub(self.channel)


    async def stream_file(self, file_key):
        request = FileRequest(file_key=file_key)
        try:
            async for response in self.stub.StreamFileMp3(request):
                yield response.data
        except grpc.aio.AioRpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
                logger.error(f"gRPC error caught: {rpc_error.details()}")
                raise FileNotFoundError(rpc_error.details())
            elif rpc_error.code() == grpc.StatusCode.INTERNAL:
                raise StreamingException(rpc_error.details())
            raise
        except Exception as e:
            logger.error(e)
            raise
