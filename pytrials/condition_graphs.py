#!/usr/bin/env python
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
if not os.path.exists(dir_conditions):
    os.makedirs(dir_conditions)


def get_conditions(client):
    """ Query all available conditions.

    :return:
    """
    pass
    results = ot.query(client, endpoint='condition')
    return results


def get_trials_for_condition(client, condition):
    """ Gets the data for the given conditions.

    :param client:
    :param condition:
    :return:
    """
    print('*** Query: {} ***'.format(condition))
    results = ot.query(client, q='conditions.name:{}'.format(condition), endpoint='trials')
    print(results['total_count'], len(results['items']))

    # Save the data in files
    f_pkl = os.path.join(dir_conditions, '{}.pkl'.format(condition))
    ot.save_results(filename=f_pkl, results=results)


def create_graph_for_condition(condition):
    """ Use networkx to create the graphs.
    :return:
    """
    print('*** Graph: {} ***'.format(condition))
    # read the results for condition
    f_pkl = os.path.join(dir_conditions, '{}.pkl'.format(condition))
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
    f_gml = os.path.join(dir_conditions, '{}.gml'.format(condition))
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
    condition = 'depression'
    client = ot.get_client()

    # results = ot.query(client, q=condition, endpoint='trials')
    # query_str = 'conditions:{{name:{}}}'.format(condition)
    query_str = 'conditions.name:{}'.format(condition)
    print('query_str:', query_str)
    results = ot.query(client, q=query_str, endpoint='trials')

    print(results['total_count'], len(results['items']))
    # pprint(results['items'][:5])

    # Save the data in files
    f_pkl = os.path.join(dir_conditions, '{}.pkl'.format(condition))
    ot.save_results(filename=f_pkl, results=results)

    # Load the data from files
    results = ot.load_results(filename=f_pkl)
    pprint(results['items'][:5])

#####################################################################################

if __name__ == "__main__":
    do_query = False

    conditions = ['depression', 'diabetes AND type AND 2', 'NAFLD']

    # get trial data
    if do_query:
        client = ot.get_client()
        for condition in conditions:
            get_trials_for_condition(client, condition)

    # create graphs

    # create_graph_for_condition('NAFLD')

    for condition in conditions:
        create_graph_for_condition(condition)


