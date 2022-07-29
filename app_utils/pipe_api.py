import os
from app_utils.fetch_data import UrlGenerator


def get_all_filters():
    return UrlGenerator(
        endpoint='filters',
        query_params={'api_token': os.getenv('API_TOKEN')}, 
        main_url=os.getenv('MAIN_URL')
    ).generate_urls()


def get_deals_by_start_and_limit(start, limit):
    return UrlGenerator(
        endpoint='deals',
        query_params={
            'api_token': os.getenv('API_TOKEN'), 
            'start': start,
            'limit': limit
        }, 
        main_url=os.getenv('MAIN_URL')
    ).generate_urls()


def get_deals_in_pipelines(pipelines, filter_id):
    return UrlGenerator(
        endpoint='pipelines/{}/deals',
        query_params={'api_token': os.getenv('API_TOKEN'), 'filter_id':filter_id},
        path_params=pipelines,
        main_url=os.getenv('MAIN_URL')
    ).generate_urls()


def get_deals_updates(deals):
    return UrlGenerator(
        endpoint='deals/{}/flow',
        query_params={'api_token': os.getenv('API_TOKEN'), 'items': 'change'}, 
        main_url=os.getenv('MAIN_URL'),
        path_params=deals
    ).generate_urls()