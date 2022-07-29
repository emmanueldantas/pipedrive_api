import json
import asyncio
import time
import os
from app_utils import pipe_api
from app_utils.fetch_data import retreive_tables
from app_utils.file_manager import save_to
from app_utils import process_data


def all_deals(max_range=100000, start=0, limit=500, save_as=None):
    loop = asyncio.get_event_loop()
    all_deals = []
    while start < max_range:
        deals = loop.run_until_complete(
            retreive_tables(
                urls_batch = pipe_api.get_deals_by_start_and_limit(start, limit),
            )
        )

        if deals: all_deals += deals; start += limit
        else: break

    if save_as:
        save_to(
            file_data=json.dumps(all_deals, indent=4),
            file_path=os.path.join(os.getenv('ROOT_DIR') ,f'files\\{save_as}')
        )
    
    return all_deals




def pipe_log(pipelines, columns, save_as=None):
    '''Retorna um JSON de movimentações de todos os ids dentro de 
    uma lista de pipelines, filtrando-se as colunas solicitadas'''
    loop = asyncio.get_event_loop()

    deals = deals_id_in_pipelines(pipelines, save_as=None)

    #A API do pipe limita o número de requests em 60 por 2s
    deals_log = []
    for mini_batch in process_data.chop_list(deals, 40):
        batch_log = loop.run_until_complete(
            retreive_tables(
                urls_batch =  pipe_api.get_deals_updates(mini_batch)
            )
        )
        deals_log += batch_log
        time.sleep(4) #Tempo entre requests


    filtered_data = [process_data.extract_values_json(log['data'], columns) for log in deals_log if log['data']['field_key'] == 'stage_id']

    if save_as:
        save_to(
            file_data=json.dumps(filtered_data, indent=4),
            file_path=os.path.join(os.getenv('ROOT_DIR'), f'files\\{save_as}')
        )
    
    return filtered_data



def deals_id_in_pipelines(pipelines, filter_id=1295, save_as=None):
    loop = asyncio.get_event_loop()
    deals_in_pipeline = loop.run_until_complete(
        retreive_tables(
            urls_batch = pipe_api.get_deals_in_pipelines(pipelines=pipelines, filter_id=filter_id)
        )
    )

    deals_ids = [deal['id'] for deal in deals_in_pipeline]

    if save_as:
        save_to(
            file_data=json.dumps(deals_ids, indent=4),
            file_path=os.path.join(os.getenv('ROOT_DIR'), f'files\\{save_as}')
        )
    
    return deals_ids
