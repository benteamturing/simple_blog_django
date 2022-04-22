import uuid

import boto3

from django.conf import settings

AWS_REGION = settings.AWS_REGION


class FileUpload:
    """
    CustomS3Client의 wrapping class
    생성된 S3 client 클래스가 아닌 인스턴스를 import 하는 경우 구조의 명확성을 위해 추가

    사용 예:
    from storages.s3_file_upload import base_client, FileUpload

    s3_client = FileUpload(base_client)
    s3_client.upload(file)
    """
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        return self.client.upload(file)


class CustomS3Client:
    """
    boto3 s3 client 생성 로직
    access_key, secret_key, bucket_name을 이용해 인스턴스를 생성한다.
    (*get_s3_env_vars())를 input으로 생성하면된다.
    self.upload(file)을 이용해 파일을 S3로 업로드하고 URL을 받는다.
    """
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        """
        request의 file을 받아 S3의 URL로 return한다.
        """
        try:
            file_id = get_file_id()
            file_content_type = {'ContentType': file.content_type}

            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                file_id,
                ExtraArgs=file_content_type
            )
            return f'https://{self.bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file_id}'

        # TODO: more specific exception error check
        except:
            return None

def get_s3_env_vars():
    """
    return S3 ACCESS_KEY_ID, SECRET_ACCESS_KEY, BUCKET_NAME as tuple
    """
    env_vars = (
        settings.AWS_S3_ACCESS_KEY_ID,
        settings.AWS_S3_SECRET_ACCESS_KEY,
        settings.AWS_STORAGE_BUCKET_NAME
    )
    return env_vars


def get_file_id():
    """
    return random uuid
    """
    return str(uuid.uuid4())


base_client = CustomS3Client(*get_s3_env_vars())

