from .power_budget import *
from .baseDAO import BaseDAO



class PowerSupplyDAO(BaseDAO):
    
    # This method is required to fulfill the abstractmethod contract
    def _restrict_instantiation(self):
        pass  
    
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
                "total_components" INTEGER NOT NULL,
                PRIMARY KEY("power_supply_id" AUTOINCREMENT)
            )
            """,
            ()
            )
    
    
    def truncate_table(self):
        with self.connection:
            self.cursor.execute(
            f"""
            DELETE FROM {self.__getstate__POWER_SUPPLIES_TABLE_NAME} WHERE 1=1
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
        total_components: int = 0
        
        with self.connection:
            self.cursor.execute(
                f"""
                INSERT INTO {self.POWER_SUPPLIES_TABLE_NAME} ("name","nominal_voltage","max_output_current","additional_information","total_components")
                VALUES (?,?,?,?,?);
                """,
                (name,nominal_voltage,max_output_current,additional_information,total_components)
            )
    
    def get_power_supply(self,power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT * FROM {self.POWER_SUPPLIES_TABLE_NAME} WHERE power_supply_id = ?
                """
                ,(power_supply_id,)
            )
            return self.cursor.fetchone()
    