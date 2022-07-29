import clr
import pandas as pd
import os
clr.AddReference('System.Data')
from System.Data import SqlClient


def exec_increment_pipedrive_log(records):
    df = pd.DataFrame(records)   
    df.columns = [
        'key_id_log',
        'key_id_cliente',
        'key_id_user_pipe',
        'key_data_registro',
        'key_valor_antigo',
        'key_valor_novo'
    ]

    return exec_sql_command(
        sqlCommandString = command_increment_pipedrive_log(df.to_json(orient='records')), 
        sqlConnectionString = os.getenv('ENG_CONN_STRING')
    )


def command_increment_pipedrive_log(records):
    return f"exec dbo.sp_increment_pipedrive_log @pipe_logs='{records}'"

def exec_sql_command(sqlCommandString, sqlConnectionString):
    output_string = ''
    transactionName = 'pipe_sync'    
    sqlDbConnection = SqlClient.SqlConnection(sqlConnectionString)
    sqlDbConnection.Open()

    transaction = sqlDbConnection.BeginTransaction(transactionName)

    command = sqlDbConnection.CreateCommand()
    command.Connection = sqlDbConnection
    command.Transaction = transaction
    command.CommandText = sqlCommandString

    try:
        output_string += str(command.ExecuteNonQuery())
        transaction.Commit()
    
    except Exception as e:
        output_string += transactionName + '\n'
        output_string += e.Message + '\n' * 2
    
        try:
            transaction.Rollback()
      
        except Exception as e:
            output_string += f'{transactionName} Rollback' + '\n'
            output_string += e.Message + '\n' * 2
  
    sqlDbConnection.Close()
    return output_string
