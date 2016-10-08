
"""
Create the graphs for the different conditions.
"""
from pprint import pprint
from ot_helpers import get_client, query


# TODO: query the available conditions & get the number of associated trials

def get_conditions():
    """ Query all available conditions.

    :return:
    """
    pass


if __name__ == "__main__":
    client = get_client()
    all_result = query(client, q='depression')
    print(all_result['total_count'], len(all_result['items']))

    pprint(all_result['items'][:5])

    # Save the data in files


