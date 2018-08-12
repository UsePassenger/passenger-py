import os


class FileReader(object):
    files = [
        "agency.txt",
        "calendar.txt",
        "calendar_dates.txt",
        "frequencies.txt",
        "routes.txt",
        "shapes.txt",
        "stop_times.txt",
        "stops.txt",
        "trips.txt",
    ]

    def __init__(self, directory_path):
        self.directory_path = directory_path

    def read(self):
        directory_path = self.directory_path
        files = self.files

        results = {}

        for basename in files:
            key = os.path.splitext(basename)[0]
            filepath = os.path.join(directory_path, basename)

            if os.path.isfile(filepath):
                results[key] = filepath

        return results
