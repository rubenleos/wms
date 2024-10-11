from flask_marshmallow import Marshmallow
from models import porders,users ,locations,containers,container_items,service_items,location_items,receipts,receipts_lines,transactions,item,porder_lines,locationsLimit,roles,sites,ordencpr,cprdet,cprrme
ma = Marshmallow() 

class POrderSchema(ma.SQLAlchemyAutoSchema):
    __tablename__ = 'porders' 
    class Meta:
        model = porders 
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = users
        load_instance = True

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = locations
        load_instance = True

class ContainerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = containers
        load_instance = True

class ContainerItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = container_items
        load_instance = True        

class ServiceItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = service_items
        load_instance = True

class LocationItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = location_items
        load_instance = True

class ReceiptSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receipts
        load_instance = True      

class ReceiptLinesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = receipts_lines
        load_instance = True              

class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = transactions
        load_instance = True

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = item
        load_instance = True  

class PordersLinesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = porder_lines
        load_instance = True                

class LocationsSchemas(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = locations
            load_instance = True  

class LocationsLimitsSchemas(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = locationsLimit
            load_instance = True  

class RolesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = roles
        load_instance = True
    
    id = ma.auto_field()
    nombre = ma.auto_field()
    ver_ordenes_venta = ma.auto_field()
    picking = ma.auto_field()
    packing_despacho = ma.auto_field()
    recibir_mercancia = ma.auto_field()
    manejar_devoluciones = ma.auto_field()
    control_stock = ma.auto_field()
    reportes = ma.auto_field()
    servicio_cliente = ma.auto_field()
    acciones_avanzadas = ma.auto_field()
    editar_ordenes = ma.auto_field() 
            
class sitesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = sites
        load_instance = True
    id = ma.auto_field()

class OrderCprSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ordencpr
        load_instance = True

class CprdetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = cprdet
        load_instance = True        

class Cprme(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =cprrme
        load_instance = True

    
    
  