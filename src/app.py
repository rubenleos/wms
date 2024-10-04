from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  
from sqlalchemy.exc import IntegrityError, DataError
from flask_marshmallow import Marshmallow
import uuid
from sqlalchemy import text
from datetime import datetime
import logging
from functions import compare_cve_pro
from models import db, porders ,users,locations ,containers,container_items,service_items,location_items,receipts,receipts_lines,transactions,item,porder_lines,locationsLimit,roles,sites
from schemas import ma, POrderSchema ,UserSchema,LocationSchema,ContainerSchema,ContainerItemSchema,LocationItemSchema,ReceiptSchema,ReceiptLinesSchema,TransactionSchema,ItemSchema,PordersLinesSchema,LocationsLimitsSchemas,RolesSchema,sitesSchema
from config.config import Config  # Importa la clase Config
import re
app = Flask(__name__)
app.config.from_object(Config)
#

db.init_app(app)   # Inicializamos SQLAlchemy con la app

ma = Marshmallow(appc)
# Define el modelo para representar la tabla 
porder_schema = POrderSchema()
user_schema =UserSchema()
locationSchema=LocationSchema()
container_schema=ContainerSchema()
container_item_schema =ContainerItemSchema()
receiptSchema=ReceiptSchema()
receipt_lines_schema=ReceiptLinesSchema()
transaction_schema=TransactionSchema()
item_schema=ItemSchema()
receipt_schema = ReceiptSchema()
porder_l_schema = PordersLinesSchema()
locationsLimitsSchemas = LocationsLimitsSchemas()
roles_schema=RolesSchema()
sites_schema = sitesSchema()

@app.route('/')
def hello():
    return 'Api iniciada'

#  registro de porder
@app.route('/porders', methods=['POST'])
def create_porder():
    data = request.get_json()

    new_porder = porders(
        # 'id' en los datos de la solicitud
        id=data['id'], 
        alm=data.get('alm'),
        cve_pro=data.get('cve_pro'),
        cve_cpr=data.get('cve_cpr'),
        ref=data.get('ref'),
        notes=data.get('notes'),
        requested_at=data.get('requested_at'),
        expected_at=data.get('expected_at'),
        updated_by=data['updated_by']  #
    )

    db.session.add(new_porder)
    db.session.flush() 

    new_porder_item1 = porder_lines(
    id="1223",
    porder_id=new_porder.id,
    item_id="1a01",
    
    avg_cost=10.5,
    quantity=5
)
    db.session.add(new_porder_item1 )

    db.session.commit()

    return porder_schema.jsonify(new_porder), 201

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    new_user = users(
        id=data['id'],
        slug=data['slug'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        avatar=data.get('avatar'),  # Puede ser opcional, así que usamos .get()
        email=data['email'],
        email_validated=datetime.strptime(data.get('email_validated'), '%Y-%m-%dT%H:%M:%S') if data.get('email_validated') else None,
        phone=data.get('phone'),  # Puede ser opcional
        phone_validated=datetime.strptime(data.get('phone_validated'), '%Y-%m-%dT%H:%M:%S') if data.get('phone_validated') else None,
        company=data.get('company'),  # Puede ser opcional
        status=data['status'],
        created_at=datetime.utcnow(),  # Usamos la fecha y hora actual en UTC
        updated_at=datetime.utcnow(),  # Usamos la fecha y hora actual en UTC
        last_login=datetime.strptime(data.get('last_login'), '%Y-%m-%dT%H:%M:%S') if data.get('last_login') else None
    )

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201
##verificar por que escribi 2 
@app.route('/location_items', methods=['POST'])
def create_location():
    data = request.get_json()

    new_location = locations(
        id=data['id'],
        status=data['status'],
        created_by=data['created_by'],
        updated_by=data['updated_by']
    )

    db.session.add(new_location)
    db.session.commit()

    return locationSchema.jsonify(new_location), 201

@app.route('/containers', methods=['POST'])
def create_container():
    data = request.get_json()
    container_id = data['id']
    if not re.match(r'^[A-Za-z]{2}\d{3}$', container_id):
            return jsonify({'error': 'ID container  formato invalido.'}), 400

    new_container = containers(
        id=data['id'],
        location_id='AB002',
        service_item_id=data['service_item_id'],
        weight=data['weight']
    )

    db.session.add(new_container)
    db.session.commit()

    return container_schema.jsonify(new_container), 201

@app.route('/container_items', methods=['POST'])
def create_container_item():
    try:
        data = request.get_json()
        print(data['container_id'])
        # Check if the container exists
        container = containers.query.get(data['container_id'])
        
        if not container:
            return jsonify({'error': 'Container not found'}), 400  # Or another appropriate status code

        new_container_item = container_items(
            id=data['id'],
            container_id=data['container_id'],
            item_id=data['item_id'],
            quantity=data['quantity']
        )

        db.session.add(new_container_item)
        db.session.commit()

        return container_item_schema.jsonify(new_container_item), 201

    except IntegrityError as e:
        db.session.rollback()
        if "Duplicate entry" in str(e):
            return jsonify({'error': 'Duplicate ID. Please provide a unique ID.'}), 400
        elif "Cannot add or update a child row" in str(e):
            return jsonify({'error': 'Foreign key constraint violated. Please check container_id and item_id.'}), 400
        else:
            return jsonify({'error': 'Integrity error. Please check your data.'}), 400

@app.route('/service_items', methods=['POST'])
def create_service_item():
    data = request.get_json()

    new_service_item = service_items(
        id=data['id'],
        description=data['description'],
        picture=data.get('picture'),  # Puede ser opcional
        tags=data.get('tags'),        # Puede ser opcional
        available=data['available'],
        existencia=data['existencia'],
        weight=data['weight'],
        avg_cost=data['avg_cost']
    )

    db.session.add(new_service_item)
    db.session.commit()

    return service_item_schema.jsonify(new_service_item), 201

##verificar porque esta dupicado
@app.route('/location_items', methods=['POST'])
def create_location_item():
    data = request.get_json()

    new_location_item = location_items(
        location_id=data['location_id'],
        item_id=data['item_id'],
        avg_cost=data['avg_cost'],
        quantity=data['quantity']
    )
    db.session.add(new_location_item)
    db.session.commit()

@app.route('/receipts', methods=['POST'])
def create_receipt():
    data = request.get_json()

    new_receipt = receipts(
        id=data['id'], 
        alm=data.get('alm'),
        cve_pro=data.get('cve_pro'),
        ref=data.get('ref'),
        notes=data.get('notes'),
        updated_by=data['updated_by'] 
    )

    db.session.add(new_receipt)
    db.session.commit()

    return receiptSchema.jsonify(new_receipt), 201

@app.route('/receipt_items', methods=['POST'])
def create_receipt_item():
    data = request.get_json()

    new_receipt_item = receipt_items(
        id=data['id'],
        receipt_id=data['receipt_id'],
        item_id=data['item_id'],
        idem_id=data['idem_id'],
        avg_cost=data['avg_cost'],
        quantity=data['quantity']
    )

    db.session.add(new_receipt_item)
    db.session.commit()

    return receipt_lines_schema.jsonify(new_receipt_item), 201

@app.route('/transactions', methods=['POST'])#INSERT TRANSACTIONS 
def create_transaction():
    data = request.get_json()
        # Check if the item exists
    items = item.query.get(data['item_id'])
    if not items:
        return jsonify({'error': 'Item not found'}), 400 

    new_transaction = transactions(
        #id=data['id'],
        item_id=data['item_id'],
        location_id=data['location_id'],
        container_id=data['container_id'],
        lot_id=data['lot_id'],
        user_id=data['user_id'],
        quantity=data['quantity'],
        qty_change=data['qty_change']
    )

    db.session.add(new_transaction)
    db.session.commit()

    return transaction_schema.jsonify(new_transaction), 201

@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()

 
        new_item = item(
            id=str(uuid.uuid4()),
            cve_pro=data['cve_pro'],
            category_id=data.get('category_id'),
            description=data.get('description'),
            picture=data.get('picture'),
            tags=data.get('tags'),
            available=data.get('available'),
            existencia=data.get('existencia'),
            unit_in=data.get('unit_in'),
            unit_out=data.get('unit_out'),
            fac_ent_sal=data.get('fac_ent_sal'),
            juego=data.get('juego'),
            weight=data.get('weight'),
            avg_cost=data.get('avg_cost')
        )

        db.session.add(new_item)
        db.session.commit()

        return item_schema.jsonify(new_item), 201

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error de integridad al crear item: {e}")
        return jsonify({"error": "Error de integridad de datos. Verifica las claves foráneas y restricciones únicas."}), 400

    except DataError as e:
        db.session.rollback()
        logging.error(f"Error de tipo de datos al crear item: {e}")
        return jsonify({"error": "Error de tipo de datos. Verifica los valores ingresados."}), 400

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inesperado al crear item: {e}")
        return jsonify({"error": "Ocurrió un error al crear el item."}), 500

###
@app.route('/locations', methods=['POST'])
def createLocations():
    try: 
        data = request.get_json()
          # Asegúrate de que los datos requeridos estén presentes en el JSON
        required_fields = ['id', 'status', 'created_by', 'updated_by']
        for field in required_fields:
            if field not in data:
                print("no hay datos")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        limit_id = data.get('limit_id')
        location_id = data['id']
        if not re.match(r'^[A-Za-z]{2}\d{3}$', location_id):
            return jsonify({'error': 'ID de formato invalido.'}), 400
        if limit_id:
            existing_limit = locationsLimit.query.get(limit_id)  
            if not existing_limit:
                return jsonify({'No existe': 'No existe Limite'}), 400    
        new_location = locations(
            id=data['id'], 
            site_id=data['site_id'],
            status=data['status'],
            created_at=datetime.utcnow(),  
            created_by=data['created_by'],
            updated_at=datetime.utcnow(),  
            updated_by=data['updated_by'],
            limit_id=data.get('limit_id')  
        )
        db.session.add(new_location)
        db.session.commit()
        return locationSchema.jsonify(new_location), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error de integridad al crear Location: {e}")
        return jsonify({"error": "Error de integridad de datos. Verifica las claves foráneas y restricciones únicas."}), 400

    except DataError as e:
        db.session.rollback()
        logging.error(f"Error de tipo de datos al crear location: {e}")
        return jsonify({"error": "Error de tipo de datos. Verifica los valores ingresados."}), 400

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inesperado al crear location: {e}")
        return jsonify({"error": f"Ocurrió un error al crear la location.{e}"}), 500    

@app.route('/receipts2', methods=['POST'])
def create_receipt2():
    try:
        data = request.get_json()
        porder_id = data.get('porder_id') 

        if not porder_id:
            return jsonify({"porder id no existe"})

        existing_porder = porders.query.get(porder_id)

        if existing_porder is None:
            return jsonify({"error": "POrder not found"}), 404

        if existing_porder.completed_at is not None: 
            new_receipt = receipts(
                id=str(uuid.uuid4()),
                alm=existing_porder.alm,
                cve_pro=existing_porder.cve_pro,
                ref=existing_porder.ref,
                notes=existing_porder.notes,
                updated_by=existing_porder.updated_by,
                status=1 ,
                porder_id = data.get('porder_id') 

            )
            db.session.add(new_receipt)
            db.session.flush() 

            new_receipt_item1 = receipts_lines(
               id="1223",
               receipt_id=new_receipt.id,
               item_id="1a01",
               idem_id="1",
               avg_cost=10.5,
               quantity=5
           )
    #        db.session.add(new_receipt_item1)
            
            ####
     #       new_item = item(
      #      id=str(uuid.uuid4()),
       #     cve_pro=existing_porder.cve_pro,
        #    category_id="5524", 
       #     description="item_creado",
        #    picture="www.example.com/",
         #   tags="454",
      #      available=30.0, 
       #     existencia=50.0,  
        #    unit_in="45",
         #   unit_out="20",
          #  fac_ent_sal=1.0, 
           # juego=5.0,
            #weight=5.0,
           # avg_cost=5.0
#)

            db.session.add(new_item)
       

        



            new_transaction1 = transactions(
                id="transaction_1",
                item_id="item_001",
                location_id="A1",
                container_id="001",
                lot_id="123",
                user_id="123",
                quantity=5.0,
                qty_change=2.0
            )
            db.session.add(new_transaction1)

            db.session.commit()

            return receipt_schema.jsonify(new_receipt), 201

        else:
            new_receipt = receipts(
                id=str(uuid.uuid4()),
                alm=existing_porder.alm,
                cve_pro=existing_porder.cve_pro,
                ref=existing_porder.ref,
                notes=existing_porder.notes,
                updated_by=existing_porder.updated_by,
                status=2,
                porder_id = data.get('porder_id') 

            )
            db.session.add(new_receipt)
            db.session.flush() 

            new_receipt_item1 = receipts_lines(
                id="3",
                receipt_id=new_receipt.id,
                item_id="item_ejemplo_1",
                idem_id="idem_ejemplo_1",
                avg_cost=10.5,
                quantity=5
            )
            db.session.add(new_receipt_item1)

            new_item = item(
            id=str(uuid.uuid4()),
            cve_pro=existing_porder.cve_pro,
            category_id="5524", 
            description="item_creado",
            picture="www.example.com/",
            tags="454",
            available=30.0, 
            existencia=50.0,  
            unit_in="45",
            unit_out="20",
            fac_ent_sal=1.0, 
            juego=5.0,
            weight=5.0,
            avg_cost=5.0
)

            db.session.add(new_item)

            new_transaction1 = transactions(
                id="transaction_12",
                item_id="item_001",
                location_id="A1",
                container_id="001",
                lot_id="123",
                user_id="123",
                quantity=5.0,
                qty_change=2.0
            )
            db.session.add(new_transaction1)

            db.session.commit()

            return receipt_schema.jsonify(new_receipt), 201

            

           # return jsonify({"message": "POrder is not completed yet"}), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500 

#  estado de un receipt y crear registros relacionados 
@app.route('/porders2', methods=['POST'])
def create_porder2():
    try:
        data = request.get_json()
        receipt_id = data.get('receipt_id') 

        if not receipt_id:
            return jsonify({"error": "Missing 'receipt_id' in JSON data"}), 400

        existing_receipt = receipts.query.get(receipt_id)

        if existing_receipt is None:
            return jsonify({"error": "Receipt not found"}), 404

        if existing_receipt.status in [2, 3]:  
            new_porder = porders(
                id=str(uuid.uuid4()),  
                alm=existing_receipt.alm,    
                cve_pro=existing_receipt.cve_pro,
                ref=existing_receipt.ref,
                notes=existing_receipt.notes,
                updated_by=existing_receipt.updated_by,
                completed_at=datetime.utcnow() if existing_receipt.status == 3 else None, 
                completed_by=existing_receipt.updated_by if existing_receipt.status == 3 else None 
            )
            db.session.add(new_porder)
            db.session.commit()

            return porder_schema.jsonify(new_porder), 201

        else:
            return jsonify({"message": "Receipt is not in a processable state"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

# Crea un nuevo registro de receipt a partir de un porder existente
@app.route('/receipts', methods=['POST'])
def create_receipt11():
    try:
        data = request.get_json()
        porder_id = data.get('porder_id')  # Obtener el ID del porder del JSON

        if not porder_id:
            return jsonify({"error": "Missing 'porder_id' in JSON data"}), 400

        existing_porder = porders.query.get(porder_id)

        if existing_porder is None:
            return jsonify({ "Porder no existe"}), 404

        if existing_porder.completed_at is not None:  
            new_receipt = receipts(
                id=str(uuid.uuid4()),
                alm=existing_porder.alm,
                cve_pro=existing_porder.cve_pro,
                ref=existing_porder.ref,
                notes=existing_porder.notes,
                updated_by=existing_porder.updated_by,
                status=1
            )
            db.session.add(new_receipt)
            db.session.commit()

            return receipt_schema.jsonify(new_receipt), 201

        else:
            new_receipt = receipts(
                id=str(uuid.uuid4()),
                alm=existing_porder.alm,
                cve_pro=existing_porder.cve_pro,
                ref=existing_porder.ref,
                notes=existing_porder.notes,
                updated_by=existing_porder.updated_by,
                status=2
            )
            return jsonify({"message": "POrder is not completed yet"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/porders/complete', methods=['PUT']) 
def complete_porder():
    try:
        data = request.json()
        porder_id = data.get('porder_id')  

        if not porder_id:
            return jsonify({"error": "Missing 'porder_id' in JSON data"}), 400

        existing_porder = porders.query.get(porder_id)

        if existing_porder is None:
            return jsonify({"error": "POrder not found"}), 404

        completed_at = data.get('completed_at')

        if completed_at is not None:
            existing_porder.completed_at = datetime.strptime(completed_at, '%Y-%m-%dT%H:%M:%S')
            existing_porder.completed_by = data.get('completed_by') 

            # Buscar el receipt asociado al porder
            associated_receipt = receipts.query.filter_by(porder_id=porder_id).first()

            if associated_receipt:
                associated_receipt.status = 3 

        db.session.commit()

        return porder_schema.jsonify(existing_porder), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/receiptsselect', methods=['GET']) 
def get_receipt():
    data = request.get_json()
    receipt_id = data.get('id')

    if not receipt_id:
        return jsonify({'message': 'Receipt ID is required'}), 400

    receipt = receipts.query.get(receipt_id)

    if not receipt:
        return jsonify({'message': 'Receipt not found'}), 404

    result = receipt_schema.dump(receipt)
    return jsonify(result), 200

@app.route('/compare_cve_pro', methods=['GET'])
def compare_cve_pro_api():
    data = request.get_json()
    porder_id = data.get('porder_id')

    if not porder_id:
        return jsonify({"error": "Missing 'porder_id' in JSON data"}), 400

    differences = compare_cve_pro(porder_id) 
    return jsonify(differences), 200

@app.route('/compare_item_id', methods=['GET'])
def compare_item_id_api():
    data = request.get_json()
    porder_id = data.get('porder_id')

    if not porder_id:
        return jsonify({"error": "Missing 'porder_id' in JSON data"}), 400

    differences = compare_cve_pro(porder_id) 
    return jsonify(differences), 200

@app.route('/containers/<container_id>', methods=['PUT'])
def mover(container_id):
    try:
        data = request.get_json()
        new_location = data.get('location_id')

        if not new_location:
            return jsonify({'error': 'Falta "location_id" en los datos JSON'}), 400

        # Corrección: Usar el modelo 'containers' para la consulta
        container_to_move = containers.query.get(container_id)

        if not container_to_move:
            return jsonify({'message': "Contenedor no encontrado"}), 404

        container_to_move.location_id = new_location
        db.session.commit()

        return container_schema.jsonify(container_to_move), 200

    except Exception as e:
        db.session.rollback()  # Revierte los cambios en caso de error
        return jsonify({'error': str(e)}), 500

@app.route('/roles', methods=['GET'])
def obtener_roles():
    try:
        # Consulta de roles
        consulta = db.session.query(roles)
        print(consulta.statement.compile(compile_kwargs={"literal_binds": True}))  # Imprimir la consulta SQL

        # Ejecutar la consulta
        todos_los_roles = consulta.all()
        for role in todos_los_roles:
            print(f'ID: {role.id}, Nombre: {role.nombre}')  # Imprimir los atributos
        
        # Serializar los resultados
        resultado = roles_schema.dump(todos_los_roles)
        print(f'Serializado: {resultado}')                   # Verificar si se está serializando correctamente

        # Retornar los resultados serializados como JSON
        return jsonify(resultado)
    except Exception as e:
        print(f'Error: {e}')  # Para debugging
        return jsonify({'error': str(e)}), 500

@app.route('/roles', methods=['POST'])
def crear_rol():
   
    data = request.get_json()
        # Check if the item exists
   

    new_rol= roles(
        id=data['id'],
        nombre=data['nombre'],
        ver_ordenes_venta=data['ver_ordenes_venta'],
        picking=data['picking'],
        packing_despacho=data['packing_despacho'],
        control_stock=data['control_stock'],
        reportes =data['reportes'],
        servicio_cliente=data['servicio_cliente'],
        acciones_avanzadas=data['acciones_avanzadas'],
        editar_ordenes=data['editar_ordenes']
    )

    db.session.add(new_rol)
    db.session.commit()

    return transaction_schema.jsonify(new_rol), 201


@app.route('/sites', methods=['POST'])
def crear_site():
    data = request.get_json()

    # Check if a site with this ID already exists
    existing_site = sites.query.filter_by(id=data['id']).first()
    if existing_site:
        return jsonify({'error': 'Site with this ID already exists'}), 400  # Bad Request

    new_site = sites(id=data['id'])
    db.session.add(new_site)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({'error': 'Site with this ID already exists'}), 400 

    return sites_schema.jsonify(new_site)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
