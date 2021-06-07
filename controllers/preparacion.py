from models.postre import PostreModel
from models.preparacion import PreparacionModel
from flask_restful import Resource, reqparse
from config.conexion_bd import base_de_datos


serializerPreparacion = reqparse.RequestParser(bundle_errors=True)
serializerPreparacion.add_argument(
    'orden',
    type=int,
    required=True,
    help='Es necesario el orden',
    location='json'
)

serializerPreparacion.add_argument(
    'descripcion',
    type=str,
    required=True,
    help='Es necesaria la descripcion',
    location='json'
)

serializerPreparacion.add_argument(
    'postre_id',
    type=int,
    required=True,
    help='Es necesario el ID del postre',
    location='json'
)


def validarPostre(postre_id):
    return base_de_datos.session.query(PostreModel).filter_by(postreId=postre_id).first()


class PreparacionesController(Resource):
    def post(self):
        data = serializerPreparacion.parse_args()
        nuevaPreparacion = PreparacionModel(
            data.get('orden'),
            data.get('descripcion'),
            data.get('postre_id')
        )
        if validarPostre(postre_id=data.get('postre_id')):
            orden = base_de_datos.session.query(PreparacionModel).filter_by(
                postre=data.get('postre_id'), preparacionOrden=data.get('orden')).first()
            if orden:
                return {
                    'success': False,
                    'content': None,
                    'message': 'El orden %s para el postre %s ya fue tomado' % (data.get('orden'), data.get('postre_id'))
                }, 400

            ultimoOrden = base_de_datos.session.query(PreparacionModel).filter_by(
                postre=data.get('postre_id')).order_by(
                PreparacionModel.preparacionOrden.desc()).first()
            if ultimoOrden:
                if ultimoOrden.preparacionOrden == int(data.get('orden')) - 1:
                    nuevaPreparacion.save()
                else:
                    return {
                        'success': False,
                        'message': 'El orden no es el que deberia ser',
                        'content': None
                    }
            else:
                if data.get('orden') == 1:
                    nuevaPreparacion.save()
                else:
                    return {
                        'success': False,
                        'message': 'El orden inicial debe de ser 1',
                        'content': None
                    }
            return {
                'success': True,
                'content': nuevaPreparacion.json(),
                'message': 'Orden creado exitosamente'
            }, 201
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Postre no existe'
            }, 400

    def get(self, postre_id):
        # PARA TRAER SOLO UNOS CAMPOS SE USA EL ".with_entities()" con los campos dentro de los parentesis
        print(base_de_datos.session.query(PreparacionModel).filter_by(
            postre=postre_id).with_entities(
            PreparacionModel.preparacionDescripcion, PreparacionModel.preparacionOrden).order_by(
            PreparacionModel.preparacionOrden.asc()).all())
        data = base_de_datos.session.query(PreparacionModel).filter_by(
            postre=postre_id).order_by(PreparacionModel.preparacionOrden.asc()).all()
        if data:
            postre = data[0].preparacionPostre.json()
            preparaciones = [item.json() for item in data]
            postre['preparaciones'] = preparaciones
            return {
                'success': True,
                'content': postre,
            }
        else:
            return {
                'success': True,
                'content': None,
            }
