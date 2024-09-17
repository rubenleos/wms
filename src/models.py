from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

db = SQLAlchemy()  # No inicializamos SQLAlchemy aquí, lo haremos en la aplicación principal

class porders(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    alm = db.Column(db.Text)
    cve_pro = db.Column(db.Text)
    cve_cpr = db.Column(db.Text)
    ref = db.Column(db.Text)
    notes = db.Column(db.Text)
    requested_at = db.Column(db.DateTime)
    expected_at = db.Column(db.DateTime)
    received_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
    onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(36), nullable=False)
    completed_at = db.Column(db.DateTime)
    completed_by = db.Column(db.String(36))

class users(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    slug = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    email_validated = db.Column(db.DateTime)
    phone = db.Column(db.String(20))
    phone_validated = db.Column(db.DateTime)
    company = db.Column(db.String(255))
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

class locations(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.Enum('active', 'inactive'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False),
    limit_id = db.Column(db.String(5))
    
class containers(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), default="AB001")
    service_item_id = db.Column(db.String(36), db.ForeignKey('service_items.id'))
    weight = db.Column(db.Float)

class container_items(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    container_id = db.Column(db.String(36), db.ForeignKey('containers.id'), nullable=False)
    item_id = db.Column(db.String(36), db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Float)

class service_items(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    description = db.Column(db.Text)
    picture = db.Column(db.Text)
    tags = db.Column(db.Text)
    available = db.Column(db.Float)
    existencia = db.Column(db.Float)
    weight = db.Column(db.Float)
    avg_cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class location_items(db.Model):
    location_id = db.Column(db.String(36), db.ForeignKey('locations.id'), primary_key=True)
    item_id = db.Column(db.String(36), db.ForeignKey('item.id'), primary_key=True) 
    avg_cost = db.Column(db.Float)
    quantity = db.Column(db.Integer) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class receipts(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    alm = db.Column(db.Text)
    cve_pro = db.Column(db.Text)
    ref = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,  onupdate=datetime.utcnow, nullable=False)
    updated_by = db.Column(db.String(36), nullable=False)
    completed_at = db.Column(db.DateTime)
    completed_by = db.Column(db.String(36))
    status = db.Column(db.Integer, nullable=False)
    porder_id = db.Column(db.String(36),db.ForeignKey('porders.id'), nullable=False)
    
class receipts_lines(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    receipt_id = db.Column(db.String(36), db.ForeignKey('receipts.id'), nullable=False)
    porder_id = db.Column(db.String(36))
    item_id = db.Column(db.String(36), nullable=False)  # Assuming it references another table, adjust if needed
    idem_id = db.Column(db.String(36), nullable=False)  # Assuming it references another table, adjust if needed
    avg_cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.String(36), nullable=False)
    location_id = db.Column(db.String(36),  nullable=False)
    container_id = db.Column(db.String(36),  nullable=False)
    lot_id = db.Column(db.String(36), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    qty_change = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class item(db.Model):
    id = db.Column(db.String(36), primary_key=True) 
    category_id = db.Column(db.String(36),nullable=False)
    cve_pro = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    picture = db.Column(db.Text)  # You might want to consider a specific image storage solution later
    tags = db.Column(db.Text)
    available = db.Column(db.Float)
    existencia = db.Column(db.Float)
    unit_in = db.Column(db.Text)
    unit_out = db.Column(db.Text)
    fac_ent_sal = db.Column(db.Float)
    juego = db.Column(db.Float)
    weight = db.Column(db.Float)
    avg_cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class porder_lines(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    porder_id = db.Column(db.String(36), db.ForeignKey('porders.id'), nullable=False)
    item_id = db.Column(db.String(36), nullable=False) 
    avg_cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class locationsLimit(db.Model):
    __tablename__ = 'locations_limit'

    id = db.Column(db.String(36), primary_key=True)
    location_id = db.Column(db.String(36), nullable=False)  # Asegúrate de que 'location_id' no sea nulo
    limitante = db.Column(db.Integer, nullable=False)  

class roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    ver_ordenes_venta = db.Column(db.Boolean)
    picking = db.Column(db.Boolean)
    packing_despacho = db.Column(db.Boolean)
    recibir_mercancia = db.Column(db.Boolean)
    manejar_devoluciones = db.Column(db.Boolean)
    control_stock = db.Column(db.Boolean)
    reportes = db.Column(db.Boolean)
    servicio_cliente = db.Column(db.Boolean)
    acciones_avanzadas = db.Column(db.Boolean)
    editar_ordenes = db.Column(db.Boolean)
    
class sites(db.Model):
    id = db.Column(db.Varchar, primary_key=True)

__all__ = ['db', 'porders', 'locations', 'users', 'containers', 'container_items', 'service_items',
        'location_items', 'receipts', 'receipt_items', 'transactions','item','porder_lines','roles','sites']     


