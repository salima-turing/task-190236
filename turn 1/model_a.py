import unittest
import logging
import io
from typing import Callable


def archive_data(data: str, logger: Callable[[str], None] = None) -> str:
    """
    Simulates data archiving function.
    If a logger is provided, it will be used to log audit messages.
    """
    if logger:
        logger("Archiving data: {}".format(data))
    archived_data = "Archived: {}".format(data)
    return archived_data


class TestDataArchivingLogging(unittest.TestCase):
    def setUp(self):
        self.log_capture_string = io.StringIO()
        self.handler = logging.StreamHandler(self.log_capture_string)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def tearDown(self):
        self.handler.close()
        self.logger.removeHandler(self.handler)

    def test_archive_data_logging(self):
        data_to_archive = "important data"
        archived_data = archive_data(data_to_archive, logger=self.logger.info)

        self.assertEqual(archived_data, f"Archived: {data_to_archive}")
        self.log_capture_string.seek(0)
        log_output = self.log_capture_string.getvalue().strip()
        self.assertEqual(log_output, f"INFO:{__name__}:Archiving data: {data_to_archive}")


if __name__ == "__main__":
    unittest.main()
