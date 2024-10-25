import unittest
import logging
import io
import re
from typing import Callable
import time

def archive_data(data: str, logger: Callable[[str], None] = None) -> str:
	"""
	Simulates data archiving function.
	If a logger is provided, it will be used to log audit messages.
	"""
	if logger:
		logger("Archiving data: %s", data)
	archived_data = f"Archived: {data}"
	return archived_data

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

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
		archived_data = archive_data(data_to_archive, logger=self.logger.info)

		self.assertEqual(archived_data, f"Archived: {data_to_archive}")
		self.log_capture_string.seek(0)
		log_output = self.log_capture_string.getvalue().strip()

		# Regular expression to match the log entry format
		log_regex = re.compile(
			r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (?P<loglevel>INFO) - Archiving data: sensitive information$"
		)

		match = log_regex.match(log_output)
		self.assertIsNotNone(match, "Log output does not match the expected format")

		log_dict = match.groupdict()
		self.assertIsNotNone(log_dict['timestamp'])
		# Verify that the timestamp is in the correct format
		time.strptime(log_dict['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
		self.assertEqual(log_dict['loglevel'], 'INFO')

if __name__ == "__main__":
	unittest.main()
