# -*- coding: utf-8 -*-

"""
Create the graphs for the different conditions.
"""
from __future__ import print_function, division
import os
import ot_helpers as ot
import networkx as nx
from pprint import pprint


def get_trials_for_query(client, query, directory):
    """ Get results for given query and save in directory.

    Uses pickle to store file.

    :param client: OpenTrial client
    :param query: Query string.
    :param directory: Directory for output file.
    :return:
    """
    print('*** Query: {} ***'.format(query))
    results = ot.query(client, q=query, endpoint='trials')
    print(results['total_count'], len(results['items']))

    # Save the data in files
    f_pkl = os.path.join(directory, '{}.pkl'.format(query))
    ot.save_results(filename=f_pkl, results=results)


def create_graph_for_query(query, directory):
    """ Creates GML graph for given query in directory.

    Pickle file for the query must exist in the repository
    Uses networkx to create the graphs.
    Node attributes are created from the OpenTrials object attributes.

    :param query: OpenTrials query.
    :param directory: Directory for input file and output graph.
    :return:
    """
    # FIXME: reading of all attributes
    # FIXME: setting of labels for visual mapping

    print('*** Graph: {} ***'.format(query))
    # read results for condition
    f_pkl = os.path.join(directory, '{}.pkl'.format(query))
    results = ot.load_results(filename=f_pkl)
    # pprint(results['items'][:1])

    # create the graph
    G = nx.Graph()

    for item in results['items']:
        # trial nodes
        trial_id = item['id']
        trial_dict = _key_dict(item)
        trial_dict['type'] = 'trial'
        G.add_node(trial_id, attr_dict=trial_dict)

        # conditions
        for cond in item['conditions']:
            cond_id = cond['id']
            cond_dict = _key_dict(cond)
            cond_dict['type'] = 'condition'
            G.add_node(cond_id, attr_dict=cond_dict)
            G.add_edge(trial_id, cond_id)

        # interventions
        for inter in item['interventions']:
            inter_id = inter['id']
            inter_dict = _key_dict(inter)
            inter_dict['type'] = 'intervention'
            G.add_node(inter_id, attr_dict=inter_dict)
            G.add_edge(trial_id, inter_id)

    # write the graph
    f_gml = os.path.join(directory, '{}.gml'.format(query))
    nx.write_gml(G, f_gml)


def _key_dict(item):
    """ Creates the keyword dict from the given OpenTrial object.

    :param item: OpenTrial object like trial, condition, intervention, ...
    :return:
    """
    d = {}
    for key, value in item.iteritems():
        if type(value) is unicode:
            # FIXME: better encoding as strings, just a hack to get it working for now
            key = key.replace('_', '')  # not supported underscore
            d[key] = value.encode('utf-8')
    if 'name' in d:
        d['otlabel'] = d['name']
    return d
