import unittest
import os
import shutil
import tempfile
import pytrials.ot_helpers as ot
import pytrials.query_graphs as qg


class OpenTrialsTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)


    #######################
    # ot_helpers
    #######################
    def test_client(self):
        """ Test the OpenTrials client.
        :return:
        """
        client = ot.get_client()
        self.assertIsNotNone(client, "Client must exist.")

    def test_query_trials(self):
        client = ot.get_client()

        results = ot.query(client, q='conditions.name:NAFLD')
        self.assertIsNotNone(results)
        self.assertTrue('items' in results)
        self.assertTrue('total_count' in results)
        self.assertTrue(results['items'] > 0)

    def test_save_results(self):
        client = ot.get_client()
        results = ot.query(client, q='conditions.name:NAFLD')
        tmp_f = os.path.join(self.test_dir, 'test.pkl')
        ot.save_results(filename=tmp_f, results=results)
        self.assertTrue(os.path.exists(tmp_f))

    def test_load_results(self):
        client = ot.get_client()
        results = ot.query(client, q='conditions.name:NAFLD')
        tmp_f = os.path.join(self.test_dir, 'test.pkl')
        ot.save_results(filename=tmp_f, results=results)
        results2 = ot.load_results(tmp_f)
        self.assertEqual(results['total_count'], results2['total_count'])
        self.assertEqual(len(results['items']), len(results2['items']))

    #######################
    # query_graphs
    #######################
    def test_get_trials_for_query(self):
        query = 'conditions.name:NAFLD'
        client = ot.get_client()
        qg.get_trials_for_query(client, query=query, directory=self.test_dir)
        qg.create_graph_for_query(query=query, directory=self.test_dir)

    def test_create_graph_for_query(self):
        query = 'conditions.name:NAFLD'
        client = ot.get_client()
        qg.get_trials_for_query(client, query=query, directory=self.test_dir)
        qg.create_graph_for_query(query=query, directory=self.test_dir)


if __name__ == '__main__':
    unittest.main()
