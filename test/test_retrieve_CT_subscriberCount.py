import unittest
import os

import pandas as pd
from datetime import datetime

class TestSubscriberCount(unittest.TestCase):
    """
    Check for extracted content from CrowdTangle
    """

    @classmethod
    def setUpClass(cls):
        cls.current_date_filename = "Facebook/data/" + datetime.now().strftime("%Y-%m-%d") + ".csv"

    def test_a_file_exists(self):
        """
        Test if there is a retrieved file for the current date
        """

        self.assertTrue(os.path.isfile(self.current_date_filename), "File %s not found" % self.current_date_filename)


    def test_b_file_contains_data(self):
        """
        Test if the CSV file contains actual stuff
        """

        df = pd.read_csv(self.current_date_filename)

        self.assertGreaterEqual(len(df), 10000)
