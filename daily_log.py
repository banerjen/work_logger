import json
import os


class DailyLog:
    def __init__(self):
        self.daily_log = dict() # Key : datetime.date, Val : Text
        self.filename = 'daily_log.json'

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

    def load_daily_log_from_file(self):
        # Load from a JSON file
        if os.path.exists(self.filename):
            with open(self.filename) as input_file:
                self.daily_log = json.load(input_file)