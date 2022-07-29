import os
from dotenv import load_dotenv
from ext import get_view
from ext import eng_db
from config import app_config


if __name__ == "__main__":
    app_config()
    load_dotenv(os.path.join(os.getenv('ROOT_DIR') ,r'.\pipe_api.env'))
    
    #Outras funções já disponíveis
    # get_view.deals_id_in_pipelines([18], save_as='deals_in_pipeline')
    # get_view.all_deals(save_as='deals')

    records = get_view.pipe_log(
        pipelines=[8, 9, 17, 18, 21, 23, 28, 35],
        columns = ['id','item_id', 'user_id', 'log_time', 'old_value', 'new_value'],
        save_as='all_deals_history'
    )

    response = eng_db.exec_increment_pipedrive_log(records)
    print(response)