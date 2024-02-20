# pytransfer
Transferring files from gdrive to AWS S3

## Pre-Reqs
1. Make sure you have Python3 and pip installed.
2. Install the following Python packages: `googleapiclient`, `google`, `boto3`, `tqdm`, `pydrive`

## GCP setup
### Create Service Account
1. Go to the Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing one.
3. In the left sidebar, click on `IAM & Admin` > `Service accounts`.
4. Click on `Create service account` at the top.
5. Enter a name and description for your service account, then click `Create`. Under `Role`,
6. select `Project` > `Owner` (or grant appropriate permissions based on your requirements).
7. Click `Continue` and then `Done`.
8. Once the service account is created, find it in the service accounts list and click on the three dots on the right side, then select `Manage keys`.
9. Click on `Add key` > `Create new key`.
10. Select the key type as JSON and click `Create`. This will download the JSON file containing your credentials. This file is your credentials.json.

Make sure to keep this credentials.json file secure and don't expose it publicly. You'll need to place this file in the same directory as your Python script for authentication to work.

## AWS setup
1. Go to S3 and create S3 bucket, for example `lebrick-file-transfer`
2. Get AWS access keys (access and secret keys) from an AWS service account. Use these credentials in the code here (in transfer.py):
```
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'
S3_BUCKET_NAME = 'bucket'
```

# Google Drive
## Share Google Drive file with GCP Service Account
1. Share the CSV file that exists in your Google Drive with the GCP Service Account.1. Go to your Google Drive in a web browser.
2. Right-click on the folder or file you want to share and select `Share`.
3. In the `Share with people and groups` dialog, enter the email address of your service account. You can find the email address in the Google Cloud Console under `IAM & Admin` > `Service accounts`. It will be in the format [SERVICE_ACCOUNT_NAME]@[PROJECT_ID].iam.gserviceaccount.com.
4. Set the access permissions for the service account (e.g., `Viewer`, `Editor`, or `Owner`) depending on what level of access you want to grant.
5. Click `Send` to share the folder or file with the service account.

# Execute code
Run the following command to initiate file transfer
```
python3 transfer.py
```
You will need to indicate if you're uploading a file from your local machine or from Google Drive.
```
Enter '1' to upload from Google Drive or '2' to upload from local machine: 2
```
1. If you've selected option 1 you will need to input the Google Drive file ID and the name of the file.
```
Enter the Google Drive file ID: 5Agbgdorkpa3TuxoZOd0DtIqN6qn-B_xD
Enter the desired file name to save: vid.mp4
Downloading: 646MB [08:01, 1.34MB/s]
File downloaded successfully from Google Drive.
Uploading: 100%|█████████████████████████████| 646M/646M [00:19<00:00, 32.3MB/s]
File uploaded successfully to AWS S3.
```
2. If you've chosen to upload a local file, pass the file name. And the name you would like the file to be saved as at rest in S3.
```
Enter '1' to upload from Google Drive or '2' to upload from local machine: 2
Enter the path of the file to upload: vid.mp4
Enter the desired file name to save: vid.mp4
File renamed successfully.
Uploading: 100%|█████████████████████████████| 651M/651M [00:20<00:00, 31.7MB/s]
File uploaded successfully to AWS S3.
```