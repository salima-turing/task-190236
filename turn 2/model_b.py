import unittest
import logging
import io
import re
from datetime import datetime
from typing import Callable


def archive_data(data: str, logger: Callable[[str], None] = None) -> str:
    """
    Simulates data archiving function.
    If a logger is provided, it will be used to log audit messages.
    """
    if logger:
        logger("Archiving data: %s", data)
    archived_data = f"Archived: {data}"
    return archived_data


LOG_FORMAT = '%(asctime)s %(levelname)s:%(name)s:%(message)s'


class TestDataArchivingLogging(unittest.TestCase):
    def setUp(self):
        self.log_capture_string = io.StringIO()
        self.handler = logging.StreamHandler(self.log_capture_string)
        self.handler.setFormatter(logging.Formatter(LOG_FORMAT))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.handler.close()
        self.logger.removeHandler(self.handler)

    def test_archive_data_logging(self):
        data_to_archive = "sensitive information"
        archive_data(data_to_archive, logger=self.logger.info)
        self.log_capture_string.seek(0)
        log_output = self.log_capture_string.getvalue().strip()

        # Regular expression to match the log format
        log_regex = re.compile(
            r'^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (?P<level>INFO):(?P<name>\w+):Archiving data: (?P<data>.+)$')

        match = log_regex.match(log_output)
        self.assertIsNotNone(match, "Log output does not match the expected format")

        log_dict = match.groupdict()
        self.assertEqual(log_dict['level'], 'INFO')
        self.assertEqual(log_dict['name'], __name__)
        self.assertEqual(log_dict['data'], data_to_archive)

        # Validate the timestamp format
        timestamp = datetime.strptime(log_dict['timestamp'], '%Y-%m-%d %H:%M:%S,%f')


if __name__ == "__main__":
    unittest.main()
