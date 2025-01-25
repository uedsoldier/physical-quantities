from modules.power_budget import *
from modules.baseDAO import BaseDAO
from modules.unit import *
from modules.utilities.json_utilities import *



class PowerSupplyDAO(BaseDAO):
    
    def __init__(self, filepath):
        super().__init__(filepath)
        self.create_table()
        self.create_triggers()
        
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
    def create_triggers(self):
        # Trigger to update power supply id in components table if a power supply is deleted
        self.cursor.execute(
            f"""
            CREATE TRIGGER IF NOT EXISTS trigger_power_supplies_delete
            AFTER DELETE ON {self.POWER_SUPPLIES_TABLE_NAME}
            FOR EACH ROW
            BEGIN
                UPDATE {self.COMPONENTS_TABLE_NAME}
                SET power_supply_id = NULL
                WHERE power_supply_id = OLD.power_supply_id;
            END;
        """,()
        )
                
    
    def create_table(self):
        with self.connection:
            self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.POWER_SUPPLIES_TABLE_NAME} (
                "power_supply_id" INTEGER NOT NULL,
                "name" TEXT NOT NULL,
                "nominal_voltage" TEXT NOT NULL,
                "max_output_current" TEXT NOT NULL,
                "additional_information" TEXT NOT NULL,
                "component_count" INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY("power_supply_id" AUTOINCREMENT)
            )
            """,
            ()
            )
    
    
    def truncate_table(self):
        with self.connection:
            self.cursor.execute(
            f"""
            DELETE FROM {self.POWER_SUPPLIES_TABLE_NAME} WHERE 1=1
            """,
            ()
            )
    
    def get_power_supply_additional_information(self,ps: BasePowerSupply) -> str: # TODO: add more power supply type
        if( isinstance(ps, Battery)):
            chemistry: str = ps.chemistry
            subchemistry: str = ps.subchemistry
            cell_voltage: str = ps.cell_voltage.to_json_string()
            cell_count: int = ps.cell_count
            capacity: str = ps.capacity.to_json_string()
            
            return f'{{"capacity":{capacity},"chemistry":{chemistry},"subchemistry":{subchemistry},"cell_voltage":{cell_voltage},"cell_count":{cell_count}}}'
        if( isinstance(ps, DCDCConverter)):
            dcdc_type: str = ps.dcdc_type
            min_input_voltage: str = ps.min_input_voltage.to_json_string()
            max_input_voltage: str = ps.max_input_voltage.to_json_string()
            efficiency: str = ps.efficiency
            return f'{{"dcdc_type":{dcdc_type},"min_input_voltage":{min_input_voltage},"max_input_voltage":{max_input_voltage},"efficiency":{efficiency}}}'
        else:
            print('Unknown power supply instance')
            return 'N/A'
    
    
    def add_power_supply(self, power_supply: BasePowerSupply):    # TODO: add more power supply types
        name: str = power_supply.name
        nominal_voltage: str = power_supply.nominal_voltage.to_json_string()
        max_output_current: str = power_supply.max_output_current.to_json_string()
        additional_information: str = self.get_power_supply_additional_information(power_supply)
        
        with self.connection:
            self.cursor.execute(
                f"""
                INSERT INTO {self.POWER_SUPPLIES_TABLE_NAME} ("name","nominal_voltage","max_output_current","additional_information")
                VALUES (?,?,?,?);
                """,
                (name,nominal_voltage,max_output_current,additional_information)
            )
    
    def get_power_supply(self,power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT * FROM {self.POWER_SUPPLIES_TABLE_NAME} WHERE power_supply_id = ?
                """
                ,(power_supply_id,)
            )
            query = self.cursor.fetchone()
            if query is None:
                raise ValueError('Invalid id')
            return query
    
    def get_power_supply_voltage(self, power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT nominal_voltage FROM {self.POWER_SUPPLIES_TABLE_NAME} WHERE power_supply_id = ?
                """
                ,(power_supply_id,)
            )
            query: str = self.cursor.fetchone()
            
            if query is None:
                raise ValueError('Invalid id')
            query = query[0]
            data = json_string_to_dict(query)
            value: float =data['value']
            unit_symbol: str = data['unit']
            unit = find_unit_by_symbol(unit_symbol)
            unit_type = find_unit_type_by_symbol(unit_symbol)
            return VoltageQuantity(value,unit)