""" Инициализация сервера gRPC для стримнга """
import grpc
from concurrent import futures
from apps.grpc.streaming_pb2 import FileChunk
from apps.grpc.streaming_pb2_grpc import add_StreamingServiceServicer_to_server, StreamingServiceServicer
from apps.core.config import settings
from apps.core.logging import logger
from botocore.exceptions import ClientError, NoCredentialsError


class StreamingService(StreamingServiceServicer):
    def __init__(self):
        self.s3_client = settings.create_minio_client()
        self.bucket_name = settings.minio_bucket_name
        settings.create_bucket_if_not_exists()


    async def StreamFileMp3(self, request, context):
        """ Метод для стриминга треков """
        file_key = request.file_key
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            stream = response['Body']

            while chunk := stream.read(1024 * 64):  # читаем по 64 KB
                logger.debug(f"Sending chunk of size {len(chunk)} bytes")
                yield FileChunk(data=chunk)

        except self.s3_client.exceptions.NoSuchKey as e:
            logger.error(f"File not found in s3: {file_key}: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File {file_key} not found")
            return
        except self.s3_client.exceptions.NoSuchBucket:
            logger.error(f"Bucket {self.bucket_name} not found in s3")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Bucket not found")
            return
        except ClientError as e:
            logger.error(f"S3 error while accessing file {file_key}: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Problem accessing to storage")
            return
        except Exception as e:
            error_msg = f"Unexpected error while streaming file {file_key}: {e}"
            logger.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
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
