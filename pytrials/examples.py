# -*- coding: utf-8 -*-
"""
Examples querying OpenTrials and creating result graphs in GML.


"""
from __future__ import print_function, division
import os
import ot_helpers as ot
import query_graphs
from pprint import pprint

dir_script = os.path.dirname(os.path.realpath(__file__))
dir_queries = os.path.join(dir_script, '../results/queries')
if not os.path.exists(dir_queries):
    os.makedirs(dir_queries)


def examples(do_query=True):
    """ Example queries.

    :param do_query: switch if web queries or use of files.
    :return:
    """
    queries = [
        # trials with condition field match
        'conditions.name:depression',
        'conditions.name:NAFLD',
        'conditions.name:diabetes AND type AND 2',
        # trials with match in any field
        'breast AND cancer AND tamoxifen'
    ]
    pprint(queries)

    # get trial data
    if do_query:
        client = ot.get_client()
        for q in queries:
            # get results
            query_graphs.get_trials_for_query(client, query=q, directory=dir_queries)

    # create graphs
    for q in queries:
        query_graphs.create_graph_for_query(query=q, directory=dir_queries)


def example(query):
    """ Performs query and creates network.

    :param query:
    :return:
    """
    client = ot.get_client()
    query_graphs.get_trials_for_query(client, query=query, directory=dir_queries)
    query_graphs.create_graph_for_query(query=query, directory=dir_queries)


def test():
    """ Simple test.

    :return:
    """
    client = ot.get_client()
    query_str = 'breast AND cancer AND tamoxifen'
    print('query_str:', query_str)
    results = ot.query(client, q=query_str, endpoint='trials')
    print(results['total_count'], len(results['items']))
    pprint(results['items'][:1])

if __name__ == "__main__":
    # run examples
    examples(do_query=True)
