import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo
class Oxxo(db.Model):
    __tablename__ = 'oxxo'

    cod_sucursal = db.Column(db.String, primary_key=True)
    nombre_gerente = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    no_sucursal = db.Column(db.String)

    def to_dict(self):
        return {
            "cod_sucursal": self.cod_sucursal,
            "nombre_gerente": self.nombre_gerente,
            "ap_paterno": self.ap_paterno,
            "ap_materno": self.ap_materno,
            "no_sucursal": self.no_sucursal
        }

# -----------------------------------------
# GET - Obtener todos los oxxos
# -----------------------------------------
@app.route('/oxxo', methods=['GET'])
def get_oxxos():
    oxxos = Oxxo.query.all()
    return jsonify([oxxo.to_dict() for oxxo in oxxos])

# -----------------------------------------
# GET - Obtener uno por código
# -----------------------------------------
@app.route('/oxxo/<string:cod_sucursal>', methods=['GET'])
def get_oxxo(cod_sucursal):
    oxxo = Oxxo.query.get(cod_sucursal)
    if not oxxo:
        return jsonify({"error": "Sucursal no encontrada"}), 404
    return jsonify(oxxo.to_dict())

# -----------------------------------------
# POST - Crear nuevo oxxo
# -----------------------------------------
@app.route('/oxxo', methods=['POST'])
def create_oxxo():
    data = request.get_json()

    nuevo = Oxxo(
        cod_sucursal=data['cod_sucursal'],
        nombre_gerente=data['nombre_gerente'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        no_sucursal=data['no_sucursal']
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify(nuevo.to_dict()), 201

# -----------------------------------------
# PUT - Actualizar oxxo
# -----------------------------------------
@app.route('/oxxo/<string:cod_sucursal>', methods=['PUT'])
def update_oxxo(cod_sucursal):
    oxxo = Oxxo.query.get(cod_sucursal)

    if not oxxo:
        return jsonify({"error": "Sucursal no encontrada"}), 404

    data = request.get_json()

    oxxo.nombre_gerente = data.get('nombre_gerente', oxxo.nombre_gerente)
    oxxo.ap_paterno = data.get('ap_paterno', oxxo.ap_paterno)
    oxxo.ap_materno = data.get('ap_materno', oxxo.ap_materno)
    oxxo.no_sucursal = data.get('no_sucursal', oxxo.no_sucursal)

    db.session.commit()

    return jsonify(oxxo.to_dict())

# -----------------------------------------
# DELETE - Eliminar oxxo
# -----------------------------------------
@app.route('/oxxo/<string:cod_sucursal>', methods=['DELETE'])
def delete_oxxo(cod_sucursal):
    oxxo = Oxxo.query.get(cod_sucursal)

    if not oxxo:
        return jsonify({"error": "Sucursal no encontrada"}), 404

    db.session.delete(oxxo)
    db.session.commit()

    return jsonify({"mensaje": "Sucursal eliminada correctamente"})

# -----------------------------------------

if __name__ == '__main__':
    app.run(port=5010, debug=True)