from core.power_budget import *
from core.baseDAO import BaseDAO
from core.unit import *
from core.utilities.json_utilities import *
from core.dao_db_schema import (
    POWER_SUPPLIES_TABLE_NAME,
    COLUMN_POWER_SUPPLY_ID,
    COLUMN_POWER_SUPPLY_NAME,
    COLUMN_NOMINAL_VOLTAGE,
    COLUMN_MAX_OUTPUT_CURRENT,
    COLUMN_ADDITIONAL_INFO,
    COLUMN_COMPONENT_COUNT,
    COMPONENTS_TABLE_NAME,
)


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
            AFTER DELETE ON {POWER_SUPPLIES_TABLE_NAME}
            FOR EACH ROW
            BEGIN
                UPDATE {COMPONENTS_TABLE_NAME}
                SET {COLUMN_POWER_SUPPLY_ID} = NULL
                WHERE {COLUMN_POWER_SUPPLY_ID} = OLD.{COLUMN_POWER_SUPPLY_ID};
            END;
        """,
            (),
        )

    def create_table(self):
        with self.connection:
            self.cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {POWER_SUPPLIES_TABLE_NAME} (
                "{COLUMN_POWER_SUPPLY_ID}" INTEGER NOT NULL,
                "{COLUMN_POWER_SUPPLY_NAME}" TEXT NOT NULL,
                "{COLUMN_NOMINAL_VOLTAGE}" TEXT NOT NULL,
                "{COLUMN_MAX_OUTPUT_CURRENT}" TEXT NOT NULL,
                "{COLUMN_ADDITIONAL_INFO}" TEXT NOT NULL,
                "{COLUMN_COMPONENT_COUNT}" INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY("{COLUMN_POWER_SUPPLY_ID}" AUTOINCREMENT)
            )
            """,
                (),
            )

    def truncate_table(self):
        with self.connection:
            self.cursor.execute(
                f"""
            DELETE FROM {POWER_SUPPLIES_TABLE_NAME} WHERE 1=1
            """,
                (),
            )

    def get_power_supply_additional_information(
        self, ps: BasePowerSupply
    ) -> str:  # TODO: add more power supply type
        if isinstance(ps, Battery):
            chemistry: str = ps.chemistry
            subchemistry: str = ps.subchemistry
            cell_voltage: str = ps.cell_voltage.to_json_string()
            cell_count: int = ps.cell_count
            capacity: str = ps.capacity.to_json_string()

            return f'{{"capacity":{capacity},"chemistry":{chemistry},"subchemistry":{subchemistry},"cell_voltage":{cell_voltage},"cell_count":{cell_count}}}'
        if isinstance(ps, DCDCConverter):
            dcdc_type: str = ps.dcdc_type
            min_input_voltage: str = ps.min_input_voltage.to_json_string()
            max_input_voltage: str = ps.max_input_voltage.to_json_string()
            efficiency: str = ps.efficiency
            return f'{{"dcdc_type":{dcdc_type},"min_input_voltage":{min_input_voltage},"max_input_voltage":{max_input_voltage},"efficiency":{efficiency}}}'
        else:
            print("Unknown power supply instance")
            return "N/A"

    def add_power_supply(self, power_supply: BasePowerSupply):
        name: str = power_supply.name
        nominal_voltage: str = power_supply.nominal_voltage.to_json_string()
        max_output_current: str = power_supply.max_output_current.to_json_string()
        additional_information: str = self.get_power_supply_additional_information(
            power_supply
        )

        with self.connection:
            self.cursor.execute(
                f"""
                INSERT INTO {POWER_SUPPLIES_TABLE_NAME} ("{COLUMN_POWER_SUPPLY_NAME}","{COLUMN_NOMINAL_VOLTAGE}","{COLUMN_MAX_OUTPUT_CURRENT}","{COLUMN_ADDITIONAL_INFO}")
                VALUES (?,?,?,?);
                """,
                (name, nominal_voltage, max_output_current, additional_information),
            )

    def get_power_supply_by_id(self, power_supply_id: int) -> BasePowerSupply:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT * FROM {POWER_SUPPLIES_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_ID} = ?
                """,
                (power_supply_id,),
            )
            query = self.cursor.fetchone()
            if query is None:
                raise ValueError("Invalid id")
            return query

    def get_power_supply_voltage(self, power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_NOMINAL_VOLTAGE} FROM {POWER_SUPPLIES_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_ID} = ?
                """,
                (power_supply_id,),
            )
            query: str = self.cursor.fetchone()

            if query is None:
                raise ValueError("Invalid id")
            query = query[0]
            voltage = VoltageQuantity(0)
            return voltage.from_json_string(query)

    def get_power_supply_output_current(self, power_supply_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_MAX_OUTPUT_CURRENT} FROM {POWER_SUPPLIES_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_ID} = ?
                """,
                (power_supply_id,),
            )
            query: str = self.cursor.fetchone()

            if query is None:
                raise ValueError("Invalid id")

            query = query[0]
            output_current = ElectricCurrentQuantity(0)
            return output_current.from_json_string(query)

    def get_power_supply_ids_by_name(self, power_supply_name: str) -> List[int]:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_POWER_SUPPLY_ID} FROM {POWER_SUPPLIES_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_NAME} = ?
                """,
                (power_supply_name,),
            )
            query: List[int] = []
            raw_query = self.cursor.fetchall()
            query = [i[0] for i in raw_query ]
            return query