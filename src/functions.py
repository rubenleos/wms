from models import porder_lines, receipts_lines,receipts,porders  # Asegúrate de importar tus modelos aquí también
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Crea el motor de la base de datos (ajusta la URI según tu configuración)
engine = create_engine('mysql+pymysql://root:Maycodb$96@192.168.1.224:3307/MaycoWms')

# Crea una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

def compare_cve_pro(porder_id):
    try:
        # Unir las tablas porders_lines y receipts_lines por porder_id, y filtrar por el porder_id proporcionado
        query = session.query(porder_lines.item_id, receipts_lines.item_id).join(receipts_lines, porder_lines.porder_id == receipts_lines.porder_id).filter(porder_lines.porder_id == porder_id)
        results = query.all()

        different_item_id = []
        for porder_item_id, receipt_item_id in results:
            if porder_item_id != receipt_item_id:
                different_item_id.append({
                    "porder_item_id": porder_item_id,
                    "receipt_item_id": receipt_item_id
                })

        return different_item_id

    except Exception as e:
        print(f"Error in compare_cve_pro: {e}")
        return [] 