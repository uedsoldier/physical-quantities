from .power_budget import *
from .baseDAO import BaseDAO



class ComponentDAO(BaseDAO):
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
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
    
    
    def truncate_table(self):
        with self.connection:
            self.cursor.execute(
            f"""
            DELETE FROM {self.COMPONENTS_TABLE_NAME} WHERE 1=1
            """,
            ()
            )

    def add_component(self, component: Component):   
        name: str = component.name
        voltage: Voltage = component.voltage.to_json_string()
        current: Current = component.current.to_json_string()
        power: Power = component.power.to_json_string()
        power_supply_id: int = None
        with self.connection:
            self.cursor.execute(
                f"""
                INSERT INTO {self.COMPONENTS_TABLE_NAME} ("name","voltage","current","power","power_supply_id")
                VALUES (?,?,?,?,?);
                """,
                (name,voltage,current,power,power_supply_id)
            )
    
    def assign_power_supply(self, component_id: int,power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                UPDATE {self.COMPONENTS_TABLE_NAME}
                SET power_supply_id = ? 
                WHERE component_id = ?
                """
                ,(power_supply_id,component_id)
                
            )
        
    
    def get_components_by_power_supply(self, power_supply_id):
        with self.connection:
            self.cursor.execute(
                f"""SELECT * FROM {self.COMPONENTS_TABLE_NAME} WHERE power_supply_id = ?"""
                , (power_supply_id,)
            )
            return self.cursor.fetchall()