-- Crear la tabla PowerSupplies con campo additional_information como JSON
CREATE TABLE IF NOT EXISTS PowerSupplies (
    power_supply_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nominal_voltage TEXT NOT NULL, -- JSON como {"value": 12.0, "unit": "V"}
    max_output_current TEXT NOT NULL, -- JSON como {"value": 10.0, "unit": "A"}
    additional_information TEXT NOT NULL, -- JSON con información adicional
    component_count INTEGER NOT NULL DEFAULT 0 -- Contador de componentes asociados
);

-- Crear la tabla Components
CREATE TABLE IF NOT EXISTS Components (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    voltage TEXT, -- JSON como {"value": 32.0, "unit": "V"}
    current TEXT, -- JSON como {"value": 5.0, "unit": "A"}
    power TEXT,   -- JSON como {"value": 160.0, "unit": "W"}
    power_supply_id INTEGER,
    FOREIGN KEY (power_supply_id) REFERENCES PowerSupplies (power_supply_id)
);

-- Crear trigger para actualizar component_count al insertar un componente
CREATE TRIGGER IF NOT EXISTS trigger_component_insert
AFTER INSERT ON Components
FOR EACH ROW
WHEN NEW.power_supply_id IS NOT NULL
BEGIN
    UPDATE PowerSupplies
    SET component_count = component_count + 1
    WHERE power_supply_id = NEW.power_supply_id;
END;

-- Crear trigger para actualizar component_count al eliminar un componente
CREATE TRIGGER IF NOT EXISTS trigger_component_delete
AFTER DELETE ON Components
FOR EACH ROW
WHEN OLD.power_supply_id IS NOT NULL
BEGIN
    UPDATE PowerSupplies
    SET component_count = component_count - 1
    WHERE power_supply_id = OLD.power_supply_id;
END;

-- Crear trigger para manejar cambios en power_supply_id de un componente
CREATE TRIGGER IF NOT EXISTS trigger_component_update
AFTER UPDATE ON Components
FOR EACH ROW
BEGIN
    -- Reducir contador de la fuente anterior si cambia
    UPDATE PowerSupplies
    SET component_count = component_count - 1
    WHERE power_supply_id = OLD.power_supply_id AND OLD.power_supply_id IS NOT NULL;

    -- Incrementar contador de la nueva fuente
    UPDATE PowerSupplies
    SET component_count = component_count + 1
    WHERE power_supply_id = NEW.power_supply_id AND NEW.power_supply_id IS NOT NULL;
END;

-- Crear trigger para actualizar componentes al eliminar una fuente
CREATE TRIGGER IF NOT EXISTS trigger_power_supplies_delete
AFTER DELETE ON PowerSupplies
FOR EACH ROW
BEGIN
    UPDATE Components
    SET power_supply_id = NULL
    WHERE power_supply_id = OLD.power_supply_id;
END;

-- Insertar datos de prueba en PowerSupplies
INSERT INTO PowerSupplies (name, nominal_voltage, max_output_current, additional_information, component_count) VALUES
('DCDC_Converter-Buck-653470', '{"value": 12.0, "unit": "V"}', '{"value": 10.0, "unit": "A"}',
 '{"dcdc_type":"Buck","min_input_voltage":{"value":12.0,"unit":"V"},"max_input_voltage":{"value":24.0,"unit":"V"},"efficiency":0.9}', 0),
('DCDC_Converter-Buck-7A3B20', '{"value": 5.0, "unit": "V"}', '{"value": 3.0, "unit": "A"}',
 '{"dcdc_type":"Buck","min_input_voltage":{"value":5.0,"unit":"V"},"max_input_voltage":{"value":15.0,"unit":"V"},"efficiency":0.85}', 0),
('DCDC_Converter-Buck-Boost-C0FFEE', '{"value": 12.0, "unit": "V"}', '{"value": 10.0, "unit": "A"}',
 '{"dcdc_type":"Buck-Boost","min_input_voltage":{"value":12.0,"unit":"V"},"max_input_voltage":{"value":24.0,"unit":"V"},"efficiency":1.0}', 0),
('DCDC_Converter-Buck-Boost-DEADBEEF', '{"value": 6.0, "unit": "V"}', '{"value": 2.0, "unit": "A"}',
 '{"dcdc_type":"Buck-Boost","min_input_voltage":{"value":6.0,"unit":"V"},"max_input_voltage":{"value":12.0,"unit":"V"},"efficiency":0.92}', 0),
('DCDC_Converter-Boost-123ABC', '{"value": 12.0, "unit": "V"}', '{"value": 5.0, "unit": "A"}',
 '{"dcdc_type":"Boost","min_input_voltage":{"value":12.0,"unit":"V"},"max_input_voltage":{"value":24.0,"unit":"V"},"efficiency":0.95}', 0),
('DCDC_Converter-Boost-DEF456', '{"value": 24.0, "unit": "V"}', '{"value": 3.0, "unit": "A"}',
 '{"dcdc_type":"Boost","min_input_voltage":{"value":24.0,"unit":"V"},"max_input_voltage":{"value":48.0,"unit":"V"},"efficiency":0.9}', 0),
('Lead_Acid_Battery-ABC123', '{"value": 6.0, "unit": "V"}', '{"value": 5.0, "unit": "A"}',
 '{"capacity":{"value":250.0,"unit":"mAh"},"chemistry":"Lead-Acid","subchemistry":"Undefined","cell_voltage":{"value":2.0,"unit":"V"},"cell_count":3}', 0),
('Lithium_Battery-7F9D9C', '{"value": 14.4, "unit": "V"}', '{"value": 3.0, "unit": "A"}',
 '{"capacity":{"value":5000.0,"unit":"mAh"},"chemistry":"Lithium","subchemistry":"Li-ion","cell_voltage":{"value":3.6,"unit":"V"},"cell_count":4}', 0),
('Lithium_Battery-BEEFCAFE', '{"value": 3.7, "unit": "V"}', '{"value": 1.0, "unit": "A"}',
 '{"capacity":{"value":1000.0,"unit":"mAh"},"chemistry":"Lithium","subchemistry":"Li-ion","cell_voltage":{"value":3.7,"unit":"V"},"cell_count":1}', 0);

-- Insertar datos de prueba en Components
INSERT INTO Components (name, voltage, current, power, power_supply_id) VALUES
('Component-FF12A3', '{"value": 12.0, "unit": "V"}', '{"value": 2.0, "unit": "A"}', '{"value": 24.0, "unit": "W"}', 1),
('Component-AB34C5', '{"value": 12.0, "unit": "V"}', '{"value": 1.5, "unit": "A"}', '{"value": 18.0, "unit": "W"}', 1),
('Component-9D45E6', '{"value": 12.0, "unit": "V"}', '{"value": 1.0, "unit": "A"}', '{"value": 12.0, "unit": "W"}', 1),
('Component-A1B2C3', '{"value": 12.0, "unit": "V"}', '{"value": 2.5, "unit": "A"}', '{"value": 30.0, "unit": "W"}', 1),
('Component-D4E5F6', '{"value": 5.0, "unit": "V"}', '{"value": 0.8, "unit": "A"}', '{"value": 4.0, "unit": "W"}', 2),
('Component-E7F8G9', '{"value": 5.0, "unit": "V"}', '{"value": 0.5, "unit": "A"}', '{"value": 2.5, "unit": "W"}', 2),
('Component-H1I2J3', '{"value": 5.0, "unit": "V"}', '{"value": 1.0, "unit": "A"}', '{"value": 5.0, "unit": "W"}', 2),
('Component-F4G5H6', '{"value": 12.0, "unit": "V"}', '{"value": 2.0, "unit": "A"}', '{"value": 24.0, "unit": "W"}', 5),
('Component-G7H8I9', '{"value": 12.0, "unit": "V"}', '{"value": 3.0, "unit": "A"}', '{"value": 36.0, "unit": "W"}', 5),
('Component-K1L2M3', '{"value": 12.0, "unit": "V"}', '{"value": 1.0, "unit": "A"}', '{"value": 12.0, "unit": "W"}', 5),
('Component-N4O5P6', '{"value": 14.4, "unit": "V"}', '{"value": 0.5, "unit": "A"}', '{"value": 7.2, "unit": "W"}', 8);
