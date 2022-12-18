from datetime import date
import json
import os

from cloud_storage import CloudStorage

class TodoAndMisc:
    def __init__(self):
        self.todo_text = ''
        self.misc_text = ''
        self.todo_filename = 'todo.txt'
        self.misc_filename = 'misc.txt'
        self.cloud_storage = CloudStorage()

    def get_todo(self):
        return self.todo_text

    def get_misc(self):
        return self.misc_text

    def set_todo(self, new_todo_text):
        self.todo_text = new_todo_text

    def set_misc(self, new_misc_text):
        self.misc_text = new_misc_text

    def save_todo_to_file(self):
        # Save as a txt file
        with open(self.todo_filename, 'w') as f:
            f.write(self.todo_text)

        self.cloud_storage.upload_file_to_cloud(self.todo_filename)

    def save_misc_to_file(self):
        # Save as a txt file
        with open(self.misc_filename, 'w') as f:
            f.write(self.misc_text)

        self.cloud_storage.upload_file_to_cloud(self.misc_filename)

    def load_todo_from_file(self):
        self.cloud_storage.download_file_from_cloud(self.todo_filename)

        # Load from a txt file
        if os.path.exists(self.todo_filename):
            with open(self.todo_filename) as f:
                self.todo_text = f.read()

    def load_misc_from_file(self):
        self.cloud_storage.download_file_from_cloud(self.misc_filename)

        # Load from a txt file
        if os.path.exists(self.misc_filename):
            with open(self.misc_filename) as f:
                self.misc_text = f.read()
