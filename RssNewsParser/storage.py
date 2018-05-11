import six
from google.cloud import storage

def _get_storage_client():
    return storage.Client(project='asr-corpora-203714')

def upload_file(file_stream, filename):
    client = _get_storage_client()
    bucket = client.bucket('asr-corpora-203714.appspot.com')
    blob = bucket.blob(filename)
    blob.upload_from_string(
        file_stream,
        content_type='audio/mp4')

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url
