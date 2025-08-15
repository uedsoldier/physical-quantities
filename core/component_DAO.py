from .power_budget import *
from .baseDAO import BaseDAO
from core.dao_db_schema import (
    COMPONENTS_TABLE_NAME,
    POWER_SUPPLIES_TABLE_NAME,
    COLUMN_COMPONENT_ID,
    COLUMN_COMPONENT_NAME,
    COLUMN_VOLTAGE,
    COLUMN_CURRENT,
    COLUMN_POWER,
    COLUMN_POWER_SUPPLY_ID,
    COLUMN_COMPONENT_COUNT
)


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
                AFTER INSERT ON {COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                WHEN NEW.{COLUMN_POWER_SUPPLY_ID} IS NOT NULL
                BEGIN
                    UPDATE {POWER_SUPPLIES_TABLE_NAME}
                    SET {COLUMN_COMPONENT_COUNT} = {COLUMN_COMPONENT_COUNT} + 1
                    WHERE {COLUMN_POWER_SUPPLY_ID} = NEW.{COLUMN_POWER_SUPPLY_ID};
                END;
            """,
                (),
            )

            # Trigger to decrement component count on delete
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS trigger_component_delete
                AFTER DELETE ON {COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                WHEN OLD.{COLUMN_POWER_SUPPLY_ID} IS NOT NULL
                BEGIN
                    UPDATE {POWER_SUPPLIES_TABLE_NAME}
                    SET {COLUMN_COMPONENT_COUNT} = {COLUMN_COMPONENT_COUNT} - 1
                    WHERE {COLUMN_POWER_SUPPLY_ID} = OLD.{COLUMN_POWER_SUPPLY_ID};
                END;
            """,
                (),
            )

            # Trigger to handle increment/decrement component count on power_supply_id update
            self.cursor.execute(
                f"""
                CREATE TRIGGER IF NOT EXISTS trigger_component_update
                AFTER UPDATE ON {COMPONENTS_TABLE_NAME}
                FOR EACH ROW
                BEGIN
                    UPDATE {POWER_SUPPLIES_TABLE_NAME}
                    SET {COLUMN_COMPONENT_COUNT} = {COLUMN_COMPONENT_COUNT} - 1
                    WHERE {COLUMN_POWER_SUPPLY_ID} = OLD.{COLUMN_POWER_SUPPLY_ID} AND OLD.{COLUMN_POWER_SUPPLY_ID} IS NOT NULL;

                    UPDATE {POWER_SUPPLIES_TABLE_NAME}
                    SET {COLUMN_COMPONENT_COUNT} = {COLUMN_COMPONENT_COUNT} + 1
                    WHERE {COLUMN_POWER_SUPPLY_ID} = NEW.{COLUMN_POWER_SUPPLY_ID} AND NEW.{COLUMN_POWER_SUPPLY_ID} IS NOT NULL;
                END;
            """,
                (),
            )

    def create_table(self):
        with self.connection:
            self.cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {COMPONENTS_TABLE_NAME} (
                "{COLUMN_COMPONENT_ID}" INTEGER NOT NULL,
                "{COLUMN_COMPONENT_NAME}" TEXT NOT NULL,
                "{COLUMN_VOLTAGE}" TEXT,
                "{COLUMN_CURRENT}" TEXT,
                "{COLUMN_POWER}" TEXT,
                "{COLUMN_POWER_SUPPLY_ID}" INTEGER,
                PRIMARY KEY("{COLUMN_COMPONENT_ID}" AUTOINCREMENT)
                FOREIGN KEY("{COLUMN_POWER_SUPPLY_ID}") REFERENCES "{POWER_SUPPLIES_TABLE_NAME}"("{COLUMN_POWER_SUPPLY_ID}")
            )
            """,
                (),
            )

    def truncate_table(self):
        with self.connection:
            self.cursor.execute(
                f"""
            DELETE FROM {COMPONENTS_TABLE_NAME} WHERE 1=1
            """,
                (),
            )

    def get_component_by_id(self, component_id: int):
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT * FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            query = self.cursor.fetchone()
            if query is None:
                raise ValueError("Invalid id")
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
                INSERT INTO {COMPONENTS_TABLE_NAME} ("name","{COLUMN_VOLTAGE}","{COLUMN_CURRENT}","{COLUMN_POWER}","{COLUMN_POWER_SUPPLY_ID}")
                VALUES (?,?,?,?,?);
                """,
                (name, voltage, current, power, power_supply_id),
            )

    def get_component_assigned_power_supply(self, component_id: int) -> int | None:
        # Check if a component is assigned to a specific power supply. If true returns the power supply id.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_POWER}_supply_id FROM {COMPONENTS_TABLE_NAME}
                WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            id = self.cursor.fetchone()[0]
            return id  # Returns id or None

    def is_component_assigned(self, component_id: int) -> bool:
        # Check if a component is already assigned to any power supply.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_POWER_SUPPLY_ID} FROM {COMPONENTS_TABLE_NAME}
                WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            ps_id = self.cursor.fetchone()[0]
            return ps_id is not None  # Returns True if assigned, False otherwise

    def is_component_assigned_to_power_supply(
        self, component_id: int, power_supply_id: int
    ) -> bool:
        # Check if a component is already assigned to a specific power supply.
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT COUNT(*) FROM {COMPONENTS_TABLE_NAME}
                WHERE {COLUMN_COMPONENT_ID} = ? AND {COLUMN_POWER_SUPPLY_ID} = ?
                """,
                (component_id, power_supply_id),
            )
            count = self.cursor.fetchone()[0]
            return count > 0  # Returns True if assigned, False otherwise

    def assign_power_supply_to_component(self, component_id: int, power_supply_id: int):
        if self.is_component_assigned_to_power_supply(component_id, power_supply_id):
            print(
                f"Component {component_id} is already assigned to Power Supply {power_supply_id}."
            )
            return
        with self.connection:
            self.cursor.execute(
                f"""
                UPDATE {COMPONENTS_TABLE_NAME}
                SET {COLUMN_POWER_SUPPLY_ID} = ? 
                WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (power_supply_id, component_id),
            )

    def get_components_list(self, power_supply_id: int) -> list:
        with self.connection:
            self.cursor.execute(
                f"""SELECT * FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_ID} = ?""",
                (power_supply_id,),
            )
            return self.cursor.fetchall()

    def get_components_count(self, power_supply_id: int) -> int:
        with self.connection:
            self.cursor.execute(
                f"""SELECT COUNT(*) FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_POWER_SUPPLY_ID} = ?""",
                (power_supply_id,),
            )
            return self.cursor.fetchone()[0]

    def get_component_voltage(self, component_id: int) -> VoltageQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_VOLTAGE} FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            query: str = self.cursor.fetchone()

            if query is None:
                raise ValueError("Invalid id")
            query = query[0]
            voltage = VoltageQuantity(0)
            return voltage.from_json_string(query)

    def get_component_current(self, component_id: int) -> ElectricCurrentQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT {COLUMN_CURRENT} FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            query: str = self.cursor.fetchone()

            if query is None:
                raise ValueError("Invalid id")
            query = query[0]
            current = ElectricCurrentQuantity(0)
            return current.from_json_string(query)

    def get_component_power(self, component_id: int) -> PowerQuantity:
        with self.connection:
            self.cursor.execute(
                f"""
                SELECT power FROM {COMPONENTS_TABLE_NAME} WHERE {COLUMN_COMPONENT_ID} = ?
                """,
                (component_id,),
            )
            query: str = self.cursor.fetchone()

            if query is None:
                raise ValueError("Invalid id")
            query = query[0]
            power = PowerQuantity(0)
            return power.from_json_string(query)
