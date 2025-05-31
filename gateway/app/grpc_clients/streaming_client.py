import grpc
from app.grpc_clients.streaming_pb2 import FileRequest
from app.grpc_clients.streaming_pb2_grpc import StreamingServiceStub


class StreamingClient:
    def __init__(self):
        self.channel = grpc.aio.insecure_channel('streaming_web:50051')
        self.stub = StreamingServiceStub(self.channel)


    async def stream_file(self, file_key):

        request = FileRequest(file_key=file_key)
        responses = self.stub.StreamFileMp3(request)

        # with open(f"{file_key}.mp3", "wb") as f:
        #     for response in responses:
        #         f.write(response.data)

        return responses



