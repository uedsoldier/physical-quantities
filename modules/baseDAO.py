# from __future__ import annotations
import sqlite3
import os
from abc import ABC, abstractmethod



class BaseDAO(ABC):
    
    COMPONENTS_TABLE_NAME: str = 'Components'
    POWER_SUPPLIES_TABLE_NAME: str = 'PowerSupplies'
    
    def __init__(self, filepath: str):
        full_database_filepath: str = os.path.abspath(filepath)
        if not os.path.exists(full_database_filepath):
            pass
        try:
            self.open(full_database_filepath)
            
            print(f'Connected to sqlite database at: {full_database_filepath}')
        except FileNotFoundError as e:
            print(e)
    
    @abstractmethod
    def _restrict_instantiation(self):
        pass
    
    def open(self, db: str):
        self.connection: sqlite3.Connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
    
    def create_table(self):
        raise NotImplementedError('Direct DAO instantiation is not allowed')
    
    def truncate_table(self):
        raise NotImplementedError('Direct DAO instantiation is not allowed')
    