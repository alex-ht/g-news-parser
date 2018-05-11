import six
from google.cloud import storage

def _get_storage_client():
    return storage.Client(project='asr-corpora-203714')

def upload_file(file_stream, fpath, content_type):
    client = _get_storage_client()
    bucket = client.bucket('asr-corpora-203714.appspot.com')
    blob = bucket.blob(fpath)
    blob.upload_from_string(
        file_stream,
        content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

def read_file(fpath, output_path):
    client = _get_storage_client()
    bucket = client.bucket('asr-corpora-203714.appspot.com')
    blob = bucket.get_blob(fpath)
    if not blob:
        return None
    with open(output_path, 'wb') as file_obj:
        blob.download_to_file(file_obj)
    return blob
