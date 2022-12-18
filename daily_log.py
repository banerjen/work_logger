import json
import os

from cloud_storage import CloudStorage


class DailyLog:
    def __init__(self):
        self.daily_log = dict() # Key : datetime.date, Val : Text
        self.filename = 'daily_log.json'
        self.cloud_storage = CloudStorage()

    def get_log(self, date_):
        if date_ in self.daily_log:
            return self.daily_log[date_]
        else:
            return ''

    def set_log(self, date_, data):
        if type(date_) == str:
            self.daily_log[date_] = data

    def save_daily_log_to_file(self):
        # Save as a JSON file
        with open(self.filename, 'w') as output_file:
            json.dump(self.daily_log, output_file)

        # Upload file to S3
        self.cloud_storage.upload_file_to_cloud(self.filename)

    def load_daily_log_from_file(self):
        # Download file from S3
        self.cloud_storage.download_file_from_cloud(self.filename)

        # Load from a JSON file
        if os.path.exists(self.filename):
            with open(self.filename) as input_file:
                self.daily_log = json.load(input_file)