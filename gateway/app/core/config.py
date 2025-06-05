from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra='ignore')
    project_name: str = Field("Сервис api gateway", alias="PROJECT_NAME")
    description: str = Field(
        "Маршрутизация запросов пользователей", alias="DESCRIPTION"
    )
    version: str = Field("1.0.0", alias="VERSION")
    cache_host: str = Field("127.0.0.1", alias="CACHE_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT")
    base_dir: str = str(Path(__file__).parent.parent)

    # Данные для работы с Minio
    minio_endpoint: str = Field("storage:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field("storage", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field("qwerty1234", alias="MINIO_SECRET_KEY")
    minio_bucket_name: str = Field("storage-artists", alias="MINIO_BUCKET_NAME")


    def create_minio_client(self):
        """ Функция для создания клиента s3 """
        try:
            s3_client = boto3.client(
                "s3",
                endpoint_url=f"http://{self.minio_endpoint}",
                aws_access_key_id=self.minio_access_key,
                aws_secret_access_key=self.minio_secret_key,
                region_name=None,
            )
            return s3_client
        except NoCredentialsError:
            raise Exception("MinIO credentials not found.")


    def create_bucket_if_not_exists(self, client=None):
        """ Функция для создания бакета, если он не существует """
        bucket_name = self.minio_bucket_name
        s3_client = client or self.create_minio_client()

        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' created.")
            else:
                raise

    def upload_file_to_s3(self, file_obj, bucket_name, object_name, s3_client):
        try:
            s3_client.upload_fileobj(file_obj, bucket_name, object_name)
            file_status = f"Файл {object_name} загружен в хранилище"
            return file_status
        except NoCredentialsError:
            raise Exception("AWS Credentials not found")
        except ClientError as e:
            raise Exception(f"Failed to upload file: {e}")


settings = Settings()
