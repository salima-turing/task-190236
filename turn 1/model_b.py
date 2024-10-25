import logging
import unittest
from io import StringIO

# Function to be tested
def archive_data(data_to_archive, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)

    logger.info("Starting data archiving process...")

    try:
        # Simulate archiving data
        logger.info(f"Archiving data: {data_to_archive}")
        archived_data = data_to_archive
        logger.info("Data archiving completed successfully.")
        return archived_data
    except Exception as e:
        logger.error(f"Data archiving failed: {e}")
        raise

# Test class using unittest
class TestDataArchiving(unittest.TestCase):
    def setUp(self):
        # Set up a logger for testing
        self.log_capture_string = StringIO()
        self.test_logger = logging.getLogger("test_logger")
        self.test_logger.setLevel(logging.INFO)
        ch = logging.StreamHandler(self.log_capture_string)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        self.test_logger.addHandler(ch)

    def tearDown(self):
        # Reset logger after each test
        self.test_logger.handlers = []

    def test_archive_data_success(self):
        data_to_archive = "Sample Data"
        archived_data = archive_data(data_to_archive, logger=self.test_logger)

        # Assert that the data was archived successfully
        self.assertEqual(archived_data, data_to_archive)

        # Check the log output
        log_output = self.log_capture_string.getvalue().strip()
        expected_log_output = (
            f"{logging.getLogger(__name__).handlers[0].formatter.formatTime('now', '%Y-%m-%d %H:%M:%S')} - INFO - Starting data archiving process..."
            f"\n{logging.getLogger(__name__).handlers[0].formatter.formatTime('now', '%Y-%m-%d %H:%M:%S')} - INFO - Archiving data: {data_to_archive}"
            f"\n{logging.getLogger(__name__).handlers[0].formatter.formatTime('now', '%Y-%m-%d %H:%M:%S')} - INFO - Data archiving completed successfully."
        )
        self.assertEqual(log_output, expected_log_output)

    def test_archive_data_failure(self):
        data_to_archive = "Invalid Data"

        with self.assertRaises(Exception) as context:
            archive_data(data_to_archive, logger=self.test_logger)

        # Check the log output for error message
        log_output = self.log_capture_string.getvalue().strip()
        self.assertIn("Data archiving failed: Invalid Data", log_output)

if __name__ == "__main__":
    unittest.main()
