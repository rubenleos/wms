CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY, 
    slug VARCHAR(255) NOT NULL, 
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    avatar VARCHAR(255), 
    email VARCHAR(255) NOT NULL,
    email_validated DATETIME, 
    phone VARCHAR(20), 
    phone_validated DATETIME, 
    company VARCHAR(255), 
    status BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    last_login DATETIME 
);

CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY, 
    alm_orig TEXT, 
    alm_dest TEXT, 
    created_at DATETIME NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,   

    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE TABLE porders (
    id VARCHAR(36) PRIMARY KEY, 
    alm TEXT, 
    cve_pro TEXT, 
    cve_cpr TEXT,
    ref TEXT,
    notes TEXT,
    requested_at DATETIME, 
    expected_at DATETIME, 
    received_at DATETIME, 
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    completed_at DATETIME,
    completed_by VARCHAR(36),
    FOREIGN KEY (updated_by) REFERENCES users(id),
    FOREIGN KEY (completed_by) REFERENCES users(id)
);

CREATE TABLE roles (
    id INT PRIMARY KEY,
    role VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE role_user (
    id INT PRIMARY KEY,
    role_id INT NOT NULL,
    user_id UUID NOT NULL, 
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id)
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE credentials (
    provider_id VARCHAR(255) NOT NULL, 
    provider_key TEXT NOT NULL,
    user_id UUID NOT NULL,
    hasher VARCHAR(255) NOT NULL, 
    password_hash TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    PRIMARY KEY (provider_id, provider_key), 
    FOREIGN KEY (user_id) REFERENCES users(id) 
);

CREATE TABLE social_profiles (
    user_id UUID NOT NULL,
    platform VARCHAR(255) NOT NULL, 
    platform_user TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, platform), 
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE shipments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36), 
    container_id VARCHAR(36),
    created_by VARCHAR(36) NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    alm_orig TEXT,
    alm_dest TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id), 
    FOREIGN KEY (container_id) REFERENCES containers(id), 
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE TABLE transactions (
    id VARCHAR(36) PRIMARY KEY, 
    item_id VARCHAR(36) NOT NULL,
    location_id VARCHAR(36) NOT NULL,
    container_id VARCHAR(36) NOT NULL,
    lot_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    quantity FLOAT NOT NULL,
    qty_change FLOAT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (item_id) REFERENCES item(id),
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (container_id) REFERENCES containers(id),
    FOREIGN KEY (lot_id) REFERENCES (lot_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE locations (
    id VARCHAR(36) PRIMARY KEY,
    status ENUM('active', 'inactive') NOT NULL, 
    created_at DATETIME NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE TABLE locations_limit (
    id VARCHAR(36) PRIMARY KEY,
    location_id VARCHAR(36) NOT NULL,
    limitante INT NOT NULL 
);


CREATE TABLE order_lines (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    item_id VARCHAR(36) NOT NULL,
    avg_cost FLOAT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);
---**
CREATE TABLE item (
    id VARCHAR(36) PRIMARY KEY,
    cve_pro TEXT NOT NULL,
    category_id VARCHAR(36),
    description TEXT,
    picture TEXT, 
    tags TEXT,
    available FLOAT,
    existencia FLOAT,
    unit_in TEXT,
    unit_out TEXT,
    fac_ent_sal FLOAT,
    juego FLOAT,
    weight FLOAT,
    avg_cost FLOAT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE service_items (
    id VARCHAR(36) PRIMARY KEY,
    description TEXT,
    picture TEXT, 
    tags TEXT,
    available FLOAT,
    existencia FLOAT,
    weight FLOAT,
    avg_cost FLOAT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE lots (
    id VARCHAR(36) PRIMARY KEY,
    cve_pro TEXT,
    lot_number TEXT,
    expiration_date DATE,
    juego FLOAT,
    weight FLOAT,
    avg_cost FLOAT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

-- Create the 'location_items' table
CREATE TABLE location_items (
    location_id VARCHAR(36) NOT NULL,
    item_id VARCHAR(36) NOT NULL,
    avg_cost FLOAT,
    quantity INT,
    created_at TEXT,
    FOREIGN KEY (location_id) REFERENCES locations(id),
    FOREIGN KEY (item_id) REFERENCES item(id) 
);

-- Create the **table
CREATE TABLE locations (
    id VARCHAR(5) PRIMARY KEY,
    status ENUM('active', 'inactive') NOT NULL,
    created_at DATETIME NOT NULL,
    created_by VARCHAR(36) NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    limits_id Varchar(5)
    FOREIGN KEY (created_by) REFERENCES users(id),
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Create the 'containers' table
CREATE TABLE containers (
    id VARCHAR(36) PRIMARY KEY,
    location_id VARCHAR(36),
    service_item_id VARCHAR(36),
    weight FLOAT,
    FOREIGN KEY (location_id) REFERENCES locations(id),
    -- Assuming 'service_item_id' references a 'service_items' table
    FOREIGN KEY (service_item_id) REFERENCES service_items(id)
);

-- Create the 'container_items' table
CREATE TABLE container_items (
    id VARCHAR(36) PRIMARY KEY,
    container_id VARCHAR(36) NOT NULL,
    item_id VARCHAR(36) NOT NULL,
    quantity FLOAT,
    FOREIGN KEY (container_id) REFERENCES containers(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);
CREATE TABLE categories (
    id VARCHAR(36) PRIMARY KEY,
    parent_category VARCHAR(36),
    slug TEXT,
    name TEXT,
    description TEXT,
    tags TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    
);




CREATE TABLE porders (
    id VARCHAR(36) PRIMARY KEY, 
    alm TEXT, 
    cve_pro TEXT, 
    cve_cpr TEXT,
    ref TEXT,
    notes TEXT,
    requested_at DATETIME, 
    expected_at DATETIME, 
    received_at DATETIME, 
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    completed_at DATETIME,
    completed_by VARCHAR(36)
);



Create table porder_lines(
     id VARCHAR(36) PRIMARY KEY,
    porder_id VARCHAR(36) NOT NULL,
    item_id VARCHAR(36) NOT NULL,
    avg_cost FLOAT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (porder_id) REFERENCES porders(id)
    );

 Create table receipts(
    id VARCHAR(36) PRIMARY KEY,
    porder_id  Varchar(10)
    alm TEXT, 
    cve_pro TEXT, 
    ref TEXT,
    notes TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    updated_by VARCHAR(36) NOT NULL,
    completed_at DATETIME,
    completed_by VARCHAR(36)
    FOREIGN KEY (porder_id) REFERENCES porders(id)
 );

 create table locations_limit
 (
    id VARCHAR(36) PRIMARY KEY,
    location_id VARCHAR(36) NOT NULL,
    limitante INT NOT NULL  
)


ALTER TABLE receipts
ADD COLUMN status int ;

alter table 
------------------------

INSERT INTO item (id, cve_pro, category_id, description, picture, tags, available, existencia, unit_in, unit_out, fac_ent_sal, juego, weight, avg_cost, created_at, updated_at)
VALUES (
    'item_001',       -- id (asegúrate de que sea único)
    'PROD-001',       -- cve_pro
    'categoria_1',    -- category_id (reemplaza con un ID existente en la tabla 'categories')
    'Producto de ejemplo 1', -- description
    'https://example.com/imagen1.jpg', -- picture (opcional)
    'etiqueta1, etiqueta2', -- tags (opcional)
    50.0,             -- available
    100.0,            -- existencia
    'unidad_entrada', -- unit_in
    'unidad_salida',  -- unit_out
    1.2,              -- fac_ent_sal
    0.5,              -- juego
    2.5,              -- weight
    10.99,            -- avg_cost
    NOW(),            -- created_at (usa la fecha y hora actual)
    NOW()             -- updated_at (usa la fecha y hora actual)
);


INSERT INTO locations (id, status, created_at, created_by, updated_at, updated_by)
VALUES (
    'A1',  -- id (asegúrate de que sea único)
    'active',               -- status
    NOW(),                  -- created_at 
    '123',           -- created_by (reemplaza con un ID de usuario existente)
    NOW(),                  -- updated_at 
    '123'            -- updated_by (reemplaza con un ID de usuario existente)
);

INSERT INTO containers (id, location_id, service_item_id, weight)
VALUES 
    ('001', 'A1', '001', 10.5)

INSERT INTO service_items (id, description, picture, tags, available, existencia, weight, avg_cost, created_at, updated_at)
VALUES (
    '001',      -- id (ensure it's unique)
    'Example Service Item',   -- description
    'https://example.com/image.jpg', -- picture (optional)
    'tag1, tag2',             -- tags (optional)
    100.0,                    -- available
    200.0,                    -- existencia
    5.5,                      -- weight
    19.99,                    -- avg_cost
    NOW(),                    -- created_at (use current datetime)
    NOW()                     -- updated_at (use current datetime)
);

  
INSERT INTO item (id, cve_pro, category_id, description, picture, tags, available, existencia, unit_in, unit_out, fac_ent_sal, juego, weight, avg_cost, created_at, updated_at)
VALUES (
    UUID(), 
    'PROD-001', 
    '5524', 
    'Descripción detallada del producto', 
    'https://ejemplo.com/imagen_producto.jpg', 
    'etiqueta1, etiqueta2', 
    15.0, 
    20.0, 
    'Pieza', 
    'Pieza', 
    1.0, 
    0.0, 
    0.5, 
    120.50, 
    NOW(), 
    NOW() 
);

INSERT INTO categories (id, name, description, created_at, updated_at) 
VALUES (
    5524, -- O cualquier método que uses para generar IDs únicos
    'linea_blanca', 
    'abarrotes', 
    NOW(), 
    NOW()
);

ALTER TABLE nombre_tabla
ADD nombre_campo tipo_dato,
ADD CONSTRAINT nombre_restriccion FOREIGN KEY (nombre_campo) REFERENCES tabla_referenciada(campo_referenciado);

ALTER TABLE nombre_tabla
ADD nombre_campo tipo_dato restricciones;

ALTER TABLE locations
ADD locations;


Alter table locations 
ADD limit_id Varchar(5) ;
ADD CONSTRAINT fk_limit_locations FOREIGN KEY (limit_id) REFERENCES locations_limit(id);

ALTER TABLE locations 
ADD CONSTRAINT nombre_restriccion FOREIGN KEY (nombre_campo_existente) REFERENCES tabla_referenciada(campo_referenciado);


ALTER TABLE locations 
ADD CONSTRAINT fk_limit_locations  FOREIGN KEY (limit_id) REFERENCES locations_limit(id);



ALTER TABLE locations 
MODIFY COLUMN  limit_id  varchar(5);

Insert into locations_limit(id,location_id,limitante)
Values('AB123','AB123',100);

INSERT INTO containers(id,location_id,service_item_id,weight)
Values('002','AA123','001',10.5)




CREATE TABLE roles (
    id INT PRIMARY KEY , -- Identificador único para cada rol
    nombre VARCHAR(50) NOT NULL UNIQUE, 
    ver_ordenes_venta BOOLEAN NOT NULL DEFAULT FALSE, 
    picking BOOLEAN NOT NULL DEFAULT FALSE, 
    packing_despacho BOOLEAN NOT NULL DEFAULT FALSE, 
    recibir_mercancia BOOLEAN NOT NULL DEFAULT FALSE, 
    manejar_devoluciones BOOLEAN NOT NULL DEFAULT FALSE,
    control_stock BOOLEAN NOT NULL DEFAULT FALSE, 
    reportes BOOLEAN NOT NULL DEFAULT FALSE, 
    servicio_cliente BOOLEAN NOT NULL DEFAULT FALSE, 
    acciones_avanzadas BOOLEAN NOT NULL DEFAULT FALSE,
    editar_ordenes BOOLEAN NOT NULL DEFAULT FALSE 
);
create Table Sites (
  id VARCHAR(36) PRIMARY KEY

)

-- Insertar rol 'Picker'
INSERT INTO roles (nombre, ver_ordenes_venta, picking)
VALUES ('Picker', TRUE, TRUE);

-- Insertar rol 'Packer'
INSERT INTO roles (nombre, ver_ordenes_venta, packing_despacho)
VALUES ('Packer', TRUE, TRUE);

-- Insertar rol 'Goods In'
INSERT INTO roles (nombre, recibir_mercancia)
VALUES ('Goods In', TRUE);

-- Insertar rol 'Returns'
INSERT INTO roles (nombre, manejar_devoluciones)
VALUES ('Returns', TRUE);

-- Insertar rol 'Stock Control'
INSERT INTO roles (nombre, ver_ordenes_venta, picking, packing_despacho, recibir_mercancia, manejar_devoluciones, control_stock)
VALUES ('Stock Control', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);

-- Insertar rol 'Reporting'
INSERT INTO roles (nombre, ver_ordenes_venta, reportes)
VALUES ('Reporting', TRUE, TRUE);

-- Insertar rol 'Customer Service'
INSERT INTO roles (nombre, ver_ordenes_venta, manejar_devoluciones, servicio_cliente)
VALUES ('Customer Service', TRUE, TRUE, TRUE);

-- Insertar rol 'Warehouse Manager'
INSERT INTO roles (nombre, ver_ordenes_venta, picking, packing_despacho, recibir_mercancia, manejar_devoluciones, control_stock, reportes, servicio_cliente, acciones_avanzadas, editar_ordenes)
VALUES ('Warehouse Manager', TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);

