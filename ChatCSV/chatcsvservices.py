# --------- Interface Export -----------#
import json
from .interface import ChatIngestInterface, ChatQueryInterface

# --------- CSV Export -----------#
from sql.sqlconnector import SqlConnector
from sql.sql_interface import SqlConnectorInterface

#------------- CHAT-CSV -------------------#
from ChatCSV.main import ChatCSV
from ChatCSV.csv_ingest import CSV_ingest


def import_csv(table: str) -> SqlConnectorInterface:
    sql = SqlConnector()
    with open("chatcsvcorpus.json", "r") as f:
        data = json.load(f)
    for entry in data:
        for key, sql_query in entry.items():
            if key == table:
                df = sql.execute_Sql(sql_query)
                match table:
                    case "table1":
                        csv_file = df.to_csv("ChatCSV/source_documents/table1.csv",index=False)
                    case "table2":
                        csv_file = df.to_csv("ChatCSV/source_documents/table2.csv",index=False)
                    ## Add more cases for other tables ## 
                return csv_file


def ingest_csv(type: str) -> ChatIngestInterface:
    csv_ingest = CSV_ingest()
    match type:
        case "table1":
            return csv_ingest.get_vectorstores()
        case "table2":
            return csv_ingest.get_vectorstores()
        ## Add more cases for other tables ##



def get_chatcsv_query(type: str) -> ChatQueryInterface:
    match type:
        case "table1":
            return ChatCSV()
        case "table2":
            return ChatCSV()
        ## Add more cases for other tables ##