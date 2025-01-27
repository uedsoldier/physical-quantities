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
                CREATE TRIGGER IF NOT EXISTS trigger_component_insert
                AFTER INSERT ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                WHEN NEW.power_supply_id IS NOT NULL
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
                CREATE TRIGGER IF NOT EXISTS trigger_component_delete
                AFTER DELETE ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                WHEN OLD.power_supply_id IS NOT NULL
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count - 1
                    WHERE power_supply_id = OLD.power_supply_id;
                END;
            """,()
            )
            
            # Trigger to handle increment/decrement component count on power_supply_id update
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS trigger_component_update
                AFTER UPDATE ON {self.COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count - 1
                    WHERE power_supply_id = OLD.power_supply_id AND OLD.power_supply_id IS NOT NULL;

                    UPDATE {self.POWER_SUPPLIES_TABLE_NAME}
                    SET component_count = component_count + 1
                    WHERE power_supply_id = NEW.power_supply_id AND NEW.power_supply_id IS NOT NULL;
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

    def get_component_by_id(self,component_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT * FROM {self.COMPONENTS_TABLE_NAME} WHERE component_id = ?
                """
                ,(component_id,)
            )
            query = self.cursor.fetchone()
            if query is None:
                raise ValueError('Invalid id')
            return query
    
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
    
    def get_component_assigned_power_supply(self, component_id: int) -> (int | None):
        # Check if a component is assigned to a specific power supply. If true returns the power supply id.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT power_supply_id FROM {self.COMPONENTS_TABLE_NAME}
                WHERE component_id = ?
                """,(component_id,)
                )
            id = self.cursor.fetchone()[0]
            return id        # Returns id or None
    
    def is_component_assigned(self,component_id: int) -> bool:
        # Check if a component is already assigned to any power supply.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT power_supply_id FROM {self.COMPONENTS_TABLE_NAME}
                WHERE component_id = ?
                """,(component_id,)
                )
            ps_id = self.cursor.fetchone()[0]
            return ps_id is not None        # Returns True if assigned, False otherwise
            
    def is_component_assigned_to_power_supply(self,component_id: int, power_supply_id: int) -> bool:
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
    
    def assign_power_supply_to_component(self, component_id: int,power_supply_id: int):
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
        
    def get_components_list(self, power_supply_id: int) -> list:
        with self.connection:
            self.cursor.execute(
                f"""SELECT * FROM {self.COMPONENTS_TABLE_NAME} WHERE power_supply_id = ?"""
                , (power_supply_id,)
            )
            return self.cursor.fetchall()
    
    def get_components_count(self, power_supply_id: int) -> int:
        with self.connection:
            self.cursor.execute(
                f"""SELECT COUNT(*) FROM {self.COMPONENTS_TABLE_NAME} WHERE power_supply_id = ?"""
                , (power_supply_id,)
            )
            return self.cursor.fetchone()[0]
    
    def get_component_voltage(self, component_id: int) -> VoltageQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT voltage FROM {self.COMPONENTS_TABLE_NAME} WHERE component_id = ?
                """
                ,(component_id,)
            )
            query: str = self.cursor.fetchone()
            
            if query is None:
                raise ValueError('Invalid id')
            query = query[0]
            voltage = VoltageQuantity(0)
            return voltage.from_json_string(query)

    def get_component_current(self, component_id: int) -> ElectricCurrentQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT current FROM {self.COMPONENTS_TABLE_NAME} WHERE component_id = ?
                """
                ,(component_id,)
            )
            query: str = self.cursor.fetchone()
            
            if query is None:
                raise ValueError('Invalid id')
            query = query[0]
            current = ElectricCurrentQuantity(0)
            return current.from_json_string(query)
    
    def get_component_power(self, component_id: int) -> PowerQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT power FROM {self.COMPONENTS_TABLE_NAME} WHERE component_id = ?
                """
                ,(component_id,)
            )
            query: str = self.cursor.fetchone()
            
            if query is None:
                raise ValueError('Invalid id')
            query = query[0]
            power = PowerQuantity(0)
            return power.from_json_string(query)