"""
Example interaction with OpenTrials.

The queries are generated using Elastic Search.
https://www.elastic.co/guide/en/elasticsearch/reference/2.3/query-dsl-query-string-query.html#query-string-syntax

"""
from __future__ import print_function, division
from bravado.client import SwaggerClient
from pprint import pprint

# The spec that will be used to generate the methods of the API client.
OPENTRIALS_API_SPEC = 'http://api.opentrials.net/v1/swagger.yaml'


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


#######################################################################################

if __name__ == "__main__":
    client = get_client()

    # Passing in a very simple query, we will paginate results by 10
    # The query response is then saved in the `result` variable
    result = client.trials.searchTrials(q='depression', per_page=10).result()

    pprint(result)
    




