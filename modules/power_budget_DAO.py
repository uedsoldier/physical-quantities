from .power_budget import *
from .baseDAO import BaseDAO

class PowerBudgetDAO(BaseDAO):
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
    def __init__(self, filepath):
        super().__init__(filepath)
        self.create_table()
    
    def create_table(self):
        with self.connection:
            self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.COMPONENTS_TABLE_NAME} (
                "component_id" INTEGER NOT NULL,
                "name" TEXT NOT NULL,
                "voltage" TEXT,
                "current" TEXT,
                "power" TEXT,
                "power_supply_id" INTEGER,
                PRIMARY KEY("component_id" AUTOINCREMENT)
                FOREIGN KEY("power_supply_id") REFERENCES "{self.POWER_SUPPLIES_TABLE_NAME}"("power_supply_id")
            )
            """,
            ()
            )