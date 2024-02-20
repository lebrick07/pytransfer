import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import boto3
from tqdm import tqdm

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account credentials file

# AWS S3 setup
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'
S3_BUCKET_NAME = 'iby-file-transfer-bucket'

# Initialize Google Drive API
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

# Initialize AWS S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def download_file_from_google_drive(file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    with open(file_name, 'wb') as fh:
        downloader = tqdm(desc="Downloading", unit="B", unit_scale=True)
        response = request.execute()
        for chunk in response:
            if isinstance(chunk, int):
                chunk = chunk.to_bytes((chunk.bit_length() + 7) // 8, 'big')
            if chunk:
                fh.write(chunk)
                downloader.update(len(chunk))


def upload_file_to_s3(file_name):
    file_size = os.path.getsize(file_name)
    with open(file_name, 'rb') as fh:
        s3.upload_fileobj(fh, S3_BUCKET_NAME, os.path.basename(file_name), Callback=ProgressPercentage(file_size))

class ProgressPercentage(object):
    def __init__(self, file_size):
        self._file_size = file_size
        self._seen_so_far = 0
        self._lock = tqdm.get_lock()
        self._pbar = tqdm(total=file_size, desc="Uploading", unit="B", unit_scale=True)

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self._pbar.update(bytes_amount)

def main():
    file_id = input("Enter the Google Drive file ID: ")
    file_name = input("Enter the desired file name to save: ")

    download_file_from_google_drive(file_id, file_name)
    print("File downloaded successfully from Google Drive.")

    upload_file_to_s3(file_name)
    print("File uploaded successfully to AWS S3.")

    os.remove(file_name)  # Remove the file from local storage after uploading

if __name__ == "__main__":
    main()
