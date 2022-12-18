import boto3
from botocore.exceptions import ClientError

import os
import csv

CLOUD_DISABLE = False


class AWS_S3_CloudStorage:
    def __init__(self, credentials_filename='credentials/credentials.csv'):
        self.aws_credentials_filename = credentials_filename
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.bucket = None

        self.read_credentials()

    def read_credentials(self):
        '''
        Credentials should be in the 2nd row of a csv file, where the first row
        would ideally contain the column names in the following order:
        [access_key_id, secret_access_key, bucket] and the second row would contain
        the values.
        '''
        with open(self.aws_credentials_filename, newline='') as csvfile:
            cred_reader = csv.reader(csvfile)
            for row in cred_reader:
                if row[0] == 'access_key_id':
                    continue
                self.aws_access_key_id = row[0]
                self.aws_secret_access_key = row[1]
                self.bucket = row[2]

    def create_session(self):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key)
        return session

    def file_exists_in_s3(self, s3_client, filename):
        try:
            s3_client.head_object(Bucket=self.bucket, Key=filename)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True

    def file_exists_locally(self, filename):
        return os.path.isfile(filename)

    def upload_file_to_cloud(self, filename):
        '''
        @param filename : Filename include local filepath
        '''
        global CLOUD_DISABLE
        if CLOUD_DISABLE:
            return True

        cur_session = self.create_session()
        s3_client = cur_session.client('s3')
        if self.file_exists_locally(filename):
            s3_client.upload_file(
                Bucket=self.bucket,
                Key=os.path.basename(filename),
                Filename=filename
            )
        else:
            print('File does not exist. Could not upload.')
            return False

        return True

    def download_file_from_cloud(self, filename):
        '''
        @param filename : Filename including local filepath where the file will be stored
        '''
        global CLOUD_DISABLE
        if CLOUD_DISABLE:
            return True

        cur_session = self.create_session()
        s3_client = cur_session.client('s3')
        if self.file_exists_in_s3(s3_client, os.path.basename(filename)):
            s3_client.download_file(
                Bucket=self.bucket,
                Key=os.path.basename(filename),
                Filename=filename
            )
        else:
            print('File does not exist in the S3 bucket. Could not download.')
            return False

        return True


# Alias
CloudStorage = AWS_S3_CloudStorage