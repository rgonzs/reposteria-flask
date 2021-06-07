from flask_restful import Resource, reqparse

from config.conexion_bd import base_de_datos
from models.ingrediente import IngredienteModel

serializerIngrediente = reqparse.RequestParser(bundle_errors=True)
serializerIngrediente.add_argument(
    'nombre',
    type=str,
    required=True,
    help='Es necesario el ingrediente',
    location='json'
)


class IngredientesController(Resource):
    def post(self):
        data = serializerIngrediente.parse_args()
        nombreIngrediente = data.get('nombre')
        nuevoIngrediente = IngredienteModel(nombreIngrediente)
        nuevoIngrediente.save()

        return {
            'success': True,
            'content': nuevoIngrediente.json(),
            'message': 'Ingrediente creado'
        }

    def get(self):
        data = base_de_datos.session.query(IngredienteModel).all()
        data = [item.json() for item in data]
        return {
            'success': True,
            'content': data,
            'message': None
        }


class IngredienteController(Resource):
    def get(self, id):
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente:
            return {
                'success': True,
                'content': ingrediente.json(),
                'message': None
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Ingrediente no existe'
            }, 404
    
    def put(self, id):
        ingrediente = base_de_datos.session.query(
            IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente:
            data = serializerIngrediente.parse_args()
            ingrediente.ingredienteNombre = data.get('nombre')
            ingrediente.save()
            return {
                "success": True,
                "content": ingrediente.json(),
                "message": None
            }
        else:
            return {
                "success": False,
                "content": None,
                "message": "Ingrediente no encontrado"
            }, 404
