from types import EllipsisType
import pyodbc
import pandas as pd

from sql_interface import SqlConnectorInterface


class SqlConnector(SqlConnectorInterface):
    def __init__(self):
        self.username = "" # Add your username here
        self.password = "" # Add your password here
        self.url = "" # Add your DB url here

    def get_dbhost(self):
        url = self.url
        def host_address(s): return s.split("//")[1].split(";")[0]
        def database_name(s): return s.split("=")[1].split(";")[0]
        host = host_address(url)
        database = database_name(url)
        return database, host

    def execute_Sql(self, sqlQuery, parameters: EllipsisType = None):
        database, host = self.get_dbhost()
        df: pd.DataFrame = None
        try:
            connect = pyodbc.connect(Driver='SQL Server', host=host,
                                        database=database, user=self.username,
                                        password=self.password)
            if (parameters != None):
                df = pd.read_sql(sqlQuery, connect, params=parameters)
            else:
                df = pd.read_sql(sqlQuery, connect)
            connect.close()
            return df
        except pyodbc.Error as e:
            raise e
