# -*- coding: utf-8 -*-

"""
Create the graphs for the different conditions.
"""
from __future__ import print_function, division
import os
from pprint import pprint
import ot_helpers as ot
import networkx as nx

dir_script = os.path.dirname(os.path.realpath(__file__))
dir_conditions = os.path.join(dir_script, 'results/conditions')
dir_queries = os.path.join(dir_script, 'results/queries')
if not os.path.exists(dir_conditions):
    os.makedirs(dir_conditions)


def get_conditions(client):
    """ Query all available conditions.

    :return:
    """
    pass
    results = ot.query(client, endpoint='condition')
    return results


def get_trials_for_query(client, query):
    """ Gets the data for the given conditions.

    :param client:
    :param query:
    :return:
    """
    print('*** Query: {} ***'.format(query))
    results = ot.query(client, q=query, endpoint='trials')
    print(results['total_count'], len(results['items']))

    # Save the data in files
    f_pkl = os.path.join(dir_queries, '{}.pkl'.format(query))
    ot.save_results(filename=f_pkl, results=results)


def create_graph_for_query(query):
    """ Use networkx to create the graphs.
    :return:
    """
    print('*** Graph: {} ***'.format(query))
    # read the results for condition
    f_pkl = os.path.join(dir_queries, '{}.pkl'.format(query))
    results = ot.load_results(filename=f_pkl)
    # pprint(results['items'][:1])

    # create the graph
    G = nx.Graph()

    for item in results['items']:
        # trial nodes
        trial_id = item['id']
        trial_dict = key_dict(item)
        trial_dict['type'] = 'trial'
        G.add_node(trial_id, attr_dict=trial_dict)

        # conditions
        for c in item['conditions']:
            cond_id = c['id']
            cond_dict = key_dict(c)
            cond_dict['type'] = 'condition'
            G.add_node(cond_id, attr_dict=cond_dict)
            G.add_edge(trial_id, cond_id)

        # interventions
        for inter in item['interventions']:
            inter_id = inter['id']
            inter_dict = key_dict(inter)
            inter_dict['type'] = 'intervention'
            G.add_node(inter_id, attr_dict=inter_dict)
            G.add_edge(trial_id, inter_id)

    # write the graph
    f_gml = os.path.join(dir_queries, '{}.gml'.format(query))
    nx.write_gml(G, f_gml)


def key_dict(item):
    """ Creates the keyword dict from the given object

    :return:
    """
    d = {}
    for key, value in item.iteritems():
        if type(value) is unicode:
            key = key.replace('_', '')  # not supported underscore
            d[key] = value.encode('utf-8')
    if 'name' in d:
        d['otlabel'] = d['name']
    return d


def test():
    """ Testing

    :return:
    """
    condition = 'breast AND cancer'
    client = ot.get_client()

    # results = ot.query(client, q=condition, endpoint='trials')
    # query_str = 'conditions:{{name:{}}}'.format(condition)
    # query_str = 'conditions.name:{}'.format(condition)

    query_str = 'breast AND cancer AND tamoxifen'
    print('query_str:', query_str)
    results = ot.query(client, q=query_str, endpoint='trials')

    print(results['total_count'], len(results['items']))
    pprint(results['items'][:1])

#####################################################################################

if __name__ == "__main__":

    test()
    exit()

    do_query = True

    # conditions = ['depression', 'diabetes AND type AND 2', 'NAFLD']
    conditions = []
    queries = ['breast AND cancer AND tamoxifen']

    queries = queries + ['conditions.name:{}'.format(c) for c in conditions]
    pprint(queries)

    # get trial data
    if do_query:
        client = ot.get_client()
        for q in queries:
            get_trials_for_query(client, q)

    # create graphs

    # create_graph_for_condition('NAFLD')

    for q in queries:
        create_graph_for_query(q)


