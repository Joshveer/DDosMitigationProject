-- Drop the existing table if it exists
DROP TABLE IF EXISTS traffic;

-- Drop the existing alerts table if it exists
DROP TABLE IF EXISTS alerts;

-- Create the new traffic table
CREATE TABLE traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_ip TEXT,
    destination_ip TEXT,
    protocol TEXT,
    packet_size INTEGER,
    flags TEXT,
    src_port INTEGER,
    dst_port INTEGER
);

-- Create the new alerts table
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    alert_type TEXT,
    source_ip TEXT,
    details TEXT
);

-- Verify the new schema
.schema

-- Exit SQLite
.quit
