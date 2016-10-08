# -*- coding: utf-8 -*-
"""
Helper functions to query the OpenTrials database.

The client is based on the swagger definitions and uses bravado
to create the python interface
http://api.opentrials.net/v1/docs/#!/trials/searchTrials

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
MAX_PAGE = 100  # maximal pages on OpenTrials
MAX_PER_PAGE = 100  # maximal results per page on OpenTrials
MAX_RESULT = MAX_PAGE * MAX_PER_PAGE  # maximal results one can get via query
ENDPOINTS = ['conditions',
             'interventions',
             'organisations',
             'persons',
             'publications',
             'search',
             'sources',
             'trials']
SLEEP_TIME = 0.1  # time to sleep between queries
# ------------------------------------------------------------------------


def get_client():
    """ Create OpenTrials client using swagger.

    The client is used to query OpenTrials. We only create
    the client once and reuse it for subsequent queries.
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

    This combines the paginated results into a single result by
    performing multiple queries for every single page.

    Don't use the 'per_page' or 'page' in the query.
    This method will collect the full set of results.

    :param client: OpenTrials client.
    :param endpoint:
    :param kwargs:
    :return: Returns the results
    """

    # check page & per_page keywords
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

    # Combines results of all pages (query as many pages as necessary with max entries per page)
    kwargs['per_page'] = MAX_PER_PAGE
    pages = int(math.ceil(total_count/MAX_PER_PAGE))
    all_results = []
    for k in xrange(pages):
        page = k+1
        print('page: {}'.format(page))
        kwargs['page'] = page

        if endpoint is 'trials':
            qres = client.trials.searchTrials(**kwargs).result()
        # FIXME: fix & test other endpoints than 'trials', currently only trials tested
        elif endpoint is 'conditions':
            qres = client.conditions.searchConditions(**kwargs).result()
        elif endpoint is 'interventions':
            qres = client.interventions.searchInterventions(**kwargs).result()
        elif endpoint is 'organisations':
            qres = client.organisations.searchOrganisations(**kwargs).result()
        elif endpoint is 'persons':
            qres = client.persons.searchPersons(**kwargs).result()
        elif endpoint is 'publications':
            qres = client.publications.searchPublications(**kwargs).result()
        elif endpoint is 'sources':
            qres = client.sources.searchSources(**kwargs).result()
        elif endpoint is 'search':
            qres = client.sources.searchSources(**kwargs).result()

        # add page results to all results
        all_results.extend(qres['items'])
        print("Cummulative results: {:2f} [{}/{}]".format(len(all_results)/total_count, len(all_results), total_count))

        # waiting between queries to not stress the server too much
        time.sleep(SLEEP)

    # put all_results into latest results
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

