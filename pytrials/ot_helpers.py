"""
Example interaction with OpenTrials.

The queries are generated using Elastic Search.
https://www.elastic.co/guide/en/elasticsearch/reference/2.3/query-dsl-query-string-query.html#query-string-syntax

"""
from __future__ import print_function, division
from bravado.client import SwaggerClient
from pprint import pprint
import warnings
import math
import time
import pickle

# ------------------------------------------------------------------------
# The spec that will be used to generate the methods of the API client.
OPENTRIALS_API_SPEC = 'http://api.opentrials.net/v1/swagger.yaml'
MAX_PAGE = 100
MAX_PER_PAGE = 100
MAX_RESULT = MAX_PAGE * MAX_PER_PAGE
ENDPOINTS = ['conditions',
             'interventions',
             'organisations',
             'persons',
             'publications',
             'search',
             'sources',
             'trials']
SLEEP = 0.1
# ------------------------------------------------------------------------


def get_client():
    """ Create OpenTrials client using swagger.
    :return: OpenTrials client.
    """

    # we want our data returned as an array of dicts, and not as class instances.
    config = {'use_models': False}

    # instantiate our API client
    client = SwaggerClient.from_url(OPENTRIALS_API_SPEC, config=config)

    # inspect the client properties
    print('-'*80)
    print('OpenTrials Client')
    print('\t', OPENTRIALS_API_SPEC)
    print('\t', dir(client))
    print('-' * 80)

    return client


def query(client, endpoint='trials', **kwargs):
    """ Query OpenTrials with the given client and search keywords.
    Returns the results.
    Don't use the 'per_page' or 'page' in the query.
    This method will collect the full set of results.

    :param client:
    :param kwargs:
    :return:
    """
    # check page
    for key in ['per_page', 'page']:
        if key in kwargs:
            warnings.warn('{} not supported in query, handled automatically'.format(key))
            del kwargs[key]

    # check endpoint
    if endpoint not in ENDPOINTS:
        raise ValueError, "endpoint not supported"

    # check the max results
    qres = client.trials.searchTrials(per_page=20, **kwargs).result()
    total_count = qres['total_count']
    if total_count > MAX_RESULT:
        warnings.warn('Query larger than maximum number of supported results: {} > {}'.format(
            total_count,
            MAX_RESULT
        ))

    # Combines the per_page and page arguments with sleep
    kwargs['per_page'] = MAX_PER_PAGE
    pages = int(math.ceil(total_count/MAX_PER_PAGE))
    all_results = []
    for k in xrange(pages):
        page = k+1
        print('page: {}'.format(page))
        kwargs['page'] = page

        if endpoint is 'conditions':
            qres = client.conditions.searchTrials(**kwargs).result()
        elif endpoint is 'interventions':
            qres = client.interventions.searchInterventions(**kwargs).result()
        elif endpoint is 'organisations':
            qres = client.organisations.searchT(**kwargs).result()
        elif endpoint is 'persons':
            qres = client.persons.searchTrials(**kwargs).result()
        elif endpoint is 'publications':
            qres = client.publications.searchTrials(**kwargs).result()
        elif endpoint is 'search':
            qres = client.search.searchTrials(**kwargs).result()
        elif endpoint is 'sources':
            qres = client.sources.searchTrials(**kwargs).result()
        elif endpoint is 'trials':
            qres = client.trials.searchTrials(**kwargs).result()

        all_results.extend(qres['items'])
        print("Cummulative results: {:2f} [{}/{}]".format(len(all_results)/total_count, len(all_results), total_count))
        time.sleep(0.1)

    # put back into latests results
    qres['items'] = all_results

    return qres


def save_results(filename, results):
    """ Pickles results in file.

    :param filename:
    :param results:
    :return:
    """
    with open(filename, 'wb') as output:
        pickle.dump(results, output, pickle.HIGHEST_PROTOCOL)


def load_results(filename):
    """ Load pickled data.

    :param filename:
    :return:
    """
    with open(filename, 'rb') as input:
        results = pickle.load(input)

    return results


#######################################################################################

if __name__ == "__main__":
    client = get_client()

    # Passing in a very simple query, we will paginate results by 10
    # The query response is then saved in the `result` variable
    # Enough words, let's get some data. The searchTrials method is the key to out Elasticsearch kingdom.

    # result = client.trials.searchTrials(q='depression', per_page=10).result()
    result = query(client, q='depression')

    pprint(result)

    # Basic metadata of results
    print('OpenTrials knows about {} trials related to depression.'.format(result['total_count']))

    # Available fields in the trial items
    r0 = result['items'][0]
    print('-'*80)
    print('Available keys')
    print('-' * 80)
    pprint(r0.keys())
    print('-' * 80)

    # [obj['public_title'] for obj in result['items']]


    # The major API endpoint for exploration is the search endpoint.
    # But as you saw at the start of the notebook, we have several other endpoints available.

    # the total number of trials
    result = client.trials.searchTrials(per_page=100).result()
    trial_count = result['total_count']

    print('Total number of trials: {}'.format(trial_count))


    print("\n\n")
    print("#"*80)


    trials_depression = client.trials.searchTrials(q="depression").result()
    print(trials_depression['total_count'])
    print(len(trials_depression['items']))
    # pprint(trials_depression)

