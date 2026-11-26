# from __future__ import annotations
import logging
import os
import sqlite3
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)



class BaseDAO(ABC):
        
    def __init__(self, filepath: str):
        full_database_filepath: str = os.path.abspath(filepath)
        if not os.path.exists(full_database_filepath):
            pass
        try:
            self.open(full_database_filepath)
            
            logger.info('Connected to sqlite database at: %s', full_database_filepath)
        except FileNotFoundError as e:
            logger.error('Could not open database: %s', e)
    
    @abstractmethod
    def _restrict_instantiation(self):
        pass
    
    def open(self, db: str):
        self.connection: sqlite3.Connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
    
    @abstractmethod
    def create_table(self):
        pass
    
    @abstractmethod
    def truncate_table(self):
        pass

    @abstractmethod
    def create_triggers(self):
        pass
    