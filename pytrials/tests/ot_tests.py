import unittest
import pytrials.ot_helpers as ot


class OpenTrialsTestCase(unittest.TestCase):

    def test_client(self):
        """ Test the OpenTrials client.
        :return:
        """
        client = ot.get_client()
        self.assertIsNotNone(client, "Client must exist.")

    def test_query_trials(self):
        self.assertEqual(True, False)


    def test_save_results(self):
        self.assertEqual(True, False)


    def test_load_results(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
