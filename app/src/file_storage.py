import json
from .models import Event  

class EventFileManager:
    FILE_PATH = "event.json"

    @classmethod
    def read_events_from_file(cls):
        try:
            with open(cls.FILE_PATH, 'r') as file:
                data = json.load(file)
                events = [Event(**event_data) for event_data in data]
        except FileNotFoundError:
            events = []
        except Exception as e:
            print(f"An error occurred while reading events from file: {e}")
            events = []
        return events

    @classmethod
    def write_events_to_file(cls, events):
        try:
            event_dicts = [event.dict() for event in events]

            with open(cls.FILE_PATH, 'w') as file:
                json.dump(event_dicts, file, indent=4)
        except Exception as e:
            print(f"An error occurred while writing events to file: {e}")

