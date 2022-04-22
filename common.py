import uuid
import os.path


def generate_random_filename(instance, filename):
    """
    랜덤한 파일 이름을 생성한다.(uuid4)
    ::param instance: file을 생성하고자 하는 모델
    ::param filename: 기존파일이름.확장자명
    ::return: 랜덤 파일 이름(URN format)
    ::rtype: str
    Note: model에 prefix를 명시하는 경우 그 경로로 저장된다.
    """

    # 파일 확장자를 받아온다
    ext = file_ext(filename)

    # 랜덤 uuid를 생성한다
    basename = get_random_id()

    try:
        prefix = instance.prefix
    except AttributeError:
        prefix = ''

    return f'{prefix}/{basename}{ext}'


def file_ext(filename):
    _, ext = os.path.splitext(filename)
    return ext


def get_random_id():
    return str(uuid.uuid4())
