import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import boto3

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account credentials file
DRIVE_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID'  # ID of the Google Drive folder containing the file

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
    fh = open(file_name, 'wb')
    downloader = request.execute()
    fh.write(downloader)
    fh.close()

def upload_file_to_s3(file_name):
    s3.upload_file(file_name, S3_BUCKET_NAME, os.path.basename(file_name))

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
