
"""
Create the graphs for the different conditions.
"""
from __future__ import print_function, division
import os
from pprint import pprint
import ot_helpers as ot

dir_script = os.path.dirname(os.path.realpath(__file__))
dir_conditions = os.path.join(dir_script, 'results/conditions')


def get_conditions(client):
    """ Query all available conditions.

    :return:
    """
    results = ot.query(client, endpoint='condition')
    return results


def get_data_for_conditions(client, conditions):
    """ Gets the data for the given conditions.

    :param client:
    :param conditions:
    :return:
    """
    for condition in conditions:
        print('*** {} ***'.format(condition))
        results = ot.query(client, q=condition, endpoint='trials')
        print(results['total_count'], len(results['items']))

        # Save the data in files
        f_pkl = os.path.join(dir_conditions, '{}.pkl'.format(condition))
        ot.save_results(filename=f_pkl, results=results)


def test():
    """ Testing

    :return:
    """
    condition = 'depression'
    client = ot.get_client()

    results = ot.query(client, q=condition, endpoint='trials')
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

    """
    conditions = ['depression', 'diabetes']
    client = ot.get_client()
    get_data_for_conditions(client, conditions)
    """

