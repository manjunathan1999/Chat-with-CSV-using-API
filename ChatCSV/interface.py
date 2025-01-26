from abc import ABC, abstractmethod


# class SqlConnectorInterface(ABC):

#     @abstractmethod
#     def get_config_values(self, sql_category, keyname):
#         pass

#     @abstractmethod
#     def get_dbhost(self):
#         pass

#     @abstractmethod
#     def sql_main(self, sql_query):
#         pass


class ChatQueryInterface(ABC):
    @abstractmethod
    def load_llm(self):
        pass

    @abstractmethod
    def query_chat(self, query: str):
        pass


class ChatIngestInterface(ABC):
    @abstractmethod
    def get_vectorstores(self):
        pass

