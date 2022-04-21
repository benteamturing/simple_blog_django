import uuid

import boto3

from django.conf import settings

AWS_REGION = settings.AWS_REGION


class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, file):
        return self.client.upload(file)


class CustomS3Client:
    """
    attributes::
    s3_client (boto3 client)
    bucket_name

    Methods::
    initialization - access_key, secret_key, bucket_name (get_s3_env_vars()를 unpacking해서 사용)
    upload - file을 input으로 가지며 s3에 업로드 후 s3 url을 return 한다.
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
            return f'http://{self.bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file_id}'

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


# Question : class가 아닌 인스턴스를 선언 후 import 해도 괜찮을까?
# 만약 매번 class를 호출해서 인스턴스를 생성한다면 client객체가 그만큼 생기는건데 이에 대한 aws의 제한사항이 있는가
s3_client = CustomS3Client(*get_s3_env_vars())

