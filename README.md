# Work Logger v1.0
A tool to keep track of daily work logs. Run the program using -
```python main.py```

## Requirements
+ Python 3.7 +
+ boto3
+ pyqt5

## Cloud storage
There is support only for S3 bucket storage. I created an S3 bucket using the following tutorial https://towardsdatascience.com/how-to-upload-and-download-files-from-aws-s3-using-python-2022-4c9b787b15f2. Using the boto3 package, data is downloaded / uploaded from the S3 bucket.

### AWS Credentials
The credentials are stored inside a credentials folder. Credentials should be in the 2nd row of a csv file, where the first row would ideally contain the column names in the following order: [access_key_id, secret_access_key, bucket] and the second row would contain the values.


