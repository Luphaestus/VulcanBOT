import json
import os
import json
import pickle
import os

class DictStorage:
    def __init__(self, filename, format='json'):
        """
        Initialize the storage with a filename and a format.
        Supported formats are 'json' and 'pickle'.
        """
        self.filename = filename
        self.format = format.lower()
        self.supported_formats = ['json', 'pickle']

        if self.format not in self.supported_formats:
            raise ValueError(f"Unsupported format: {self.format}. Use 'json' or 'pickle'.")
    def _ensure_directory_exists(self):
        """
        Ensure that the directory for the specified file exists.
        """

        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist

    def save(self, data):
        """
        Save the given dictionary to the specified file.
        """
        self._ensure_directory_exists()

        if self.format == 'json':
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=2)
        elif self.format == 'pickle':
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)

    def load(self):
        """
        Load a dictionary from the specified file.
        Returns an empty dictionary if the file doesn't exist.
        """
        if not os.path.exists(self.filename):
            # File doesn't exist, return an empty dictionary
            return {}

        if self.format == 'json':
            with open(self.filename, 'r') as file:
                return json.load(file)
        elif self.format == 'pickle':
            with open(self.filename, 'rb') as file:
                return pickle.load(file)

class PersistentCounter:
    def __init__(self, filename):
        self.filename = filename
        self.counter = self._load_counter()

    def _load_counter(self):
        # Check if the file exists and read the current count from it
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                try:
                    return int(f.read().strip())
                except ValueError:
                    pass
        # If the file doesn't exist or is invalid, start from 0
        return 0

    def increment(self):
        # Increment the counter and save it to the file
        self.counter += 1
        with open(self.filename, 'w') as f:
            f.write(str(self.counter))

    def get_value(self):
        return self.counter
# Class for managing attachment-only threads
class json_manager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.only_attachments = self.load()

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []  # Return empty list if not found

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.only_attachments, f)

    def add(self, thread_id):
        if thread_id not in self.only_attachments:
            self.only_attachments.append(thread_id)
            self.save()

    def remove(self, thread_id):
        if thread_id in self.only_attachments:
            self.only_attachments.remove(thread_id)
            self.save()

