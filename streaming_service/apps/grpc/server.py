import grpc
from concurrent import futures
from apps.grpc.streaming_pb2 import FileChunk
from apps.grpc.streaming_pb2_grpc import add_StreamingServiceServicer_to_server
from apps.core.config import settings
from apps.core.logging import logger
import boto3


class StreamingService:
    def __init__(self):
        self.s3_client = settings.create_minio_client()
        self.bucket_name = settings.minio_bucket_name
        settings.create_bucket_if_not_exists()


    async def StreamFileMp3(self, request, context):
        file_key = request.file_key
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            stream = response['Body']

            while chunk := stream.read(1024 * 64):  # Читаем по 64 KB
                yield FileChunk(data=chunk)

        except Exception as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File {file_key} not found")
            return


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    add_StreamingServiceServicer_to_server(StreamingService(), server)
    server.add_insecure_port('[::]:50051')
    logger.info("GRPC server started on port 50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    serve()