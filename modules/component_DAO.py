from .power_budget import *
from .baseDAO import BaseDAO



class ComponentDAO(BaseDAO):
    
    def __init__(self, filepath):
        super().__init__(filepath)
        self.create_table()
        self.create_triggers()
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
    def create_triggers(self):
        # Create triggers to automatically update component counts in PowerSupply table.
        with self.connection:
            
            # Trigger to increment component count on insert
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS increment_component_count_on_insert
                AFTER INSERT ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count + 1
                    WHERE power_supply_id = NEW.power_supply_id;
                END;
            """,()
            )
            
            # Trigger to decrement component count on delete
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS decrement_component_count_on_delete
                AFTER DELETE ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count - 1
                    WHERE power_supply_id = OLD.power_supply_id;
                END;
            """,()
            )
            
            # Trigger to decrement component count on power_supply_id update (old power supply)
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS decrement_component_count_on_update
                AFTER UPDATE OF power_supply_id ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count - 1
                    WHERE power_supply_id = OLD.power_supply_id;
                END;
            """,()
            )
            
            # Trigger to increment component count on power_supply_id update (new power supply)
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS increment_component_count_on_update
                AFTER UPDATE OF power_supply_id ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count + 1
                    WHERE power_supply_id = NEW.power_supply_id;
                END;
            """,()
            )
            
    
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
        voltage: VoltageQuantity = component.voltage.to_json_string()
        current: ElectricCurrentQuantity = component.current.to_json_string()
        power: PowerQuantity = component.power.to_json_string()
        power_supply_id: int = None
        with self.connection:
            self.cursor.execute(
                f"""
                INSERT INTO {self.COMPONENTS_TABLE_NAME} ("name","voltage","current","power","power_supply_id")
                VALUES (?,?,?,?,?);
                """,
                (name,voltage,current,power,power_supply_id)
            )
            
    def is_component_assigned_to_power_supply(self,component_id: int, power_supply_id: int):
        # Check if a component is already assigned to a specific power supply.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT COUNT(*) FROM {self.COMPONENTS_TABLE_NAME}
                WHERE component_id = ? AND power_supply_id = ?
                """,(component_id,power_supply_id)
                )
            count = self.cursor.fetchone()[0]
            return count > 0        # Returns True if assigned, False otherwise
    
    def assign_power_supply(self, component_id: int,power_supply_id: int):
        if(self.is_component_assigned_to_power_supply(component_id,power_supply_id)):
            print(f'Component {component_id} is already assigned to Power Supply {power_supply_id}.')
            return
        with self.connection:
            self.cursor.execute(
                f"""
                UPDATE {self.COMPONENTS_TABLE_NAME}
                SET power_supply_id = ? 
                WHERE component_id = ?
                """
                ,(power_supply_id,component_id)
            )
        
    def get_components_by_power_supply(self, power_supply_id: int) -> list:
        with self.connection:
            self.cursor.execute(
                f"""SELECT * FROM {self.COMPONENTS_TABLE_NAME} WHERE power_supply_id = ?"""
                , (power_supply_id,)
            )
            return self.cursor.fetchall()
    
    def count_components_per_power_supply(self, power_supply_id: int) -> int:
        with self.connection:
            self.cursor.execute(
                f"""SELECT COUNT(*) FROM {self.COMPONENTS_TABLE_NAME} WHERE power_supply_id = ?"""
                , (power_supply_id,)
            )
            return self.cursor.fetchone()[0]