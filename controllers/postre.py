# un controlador es el comportamiento que va a tener mi API cuando se llame a determinada ruta
# /postres GET => mostrar los postres
from flask_restful import Resource, reqparse
from models.postre import PostreModel
from config.conexion_bd import base_de_datos

# serializer (serializador)

serializerPostres = reqparse.RequestParser(bundle_errors=True)
serializerPostres.add_argument(
    'nombre',
    type=str,  # tipo de dato
    required=True,  # si es de caracter obligatorio o no
    help='Falta el nombre',  # mensaje de ayuda en caso sea obligatorio  y no lo mandase
    location='json'  # en que parte del request me mandara, json (body) o url
)
serializerPostres.add_argument(
    'porcion',
    type=str,  # tipo de dato
    required=True,  # si es de caracter obligatorio o no
    # mensaje de ayuda en caso sea obligatorio  y no lo mandase
    help='Falta la porcion {error_msg}',
    choices=('Familiar', 'Personal', 'Mediano'),
    location='json'  # en que parte del request me mandara, json (body) o url
)


class PostresController(Resource):
    def get(self):
        # SELECT * FROM POSTRES
        postres = PostreModel.query.all()
        resultado = [postre.json() for postre in postres]
        return {
            'success': True,
            'content': resultado,
            'message': None
        }

    def post(self):
        data = serializerPostres.parse_args()
        nuevoPostre = PostreModel(nombre=data.get('nombre'), porcion=data.get('porcion'))
        nuevoPostre.save()
        return {
            'success': True,
            'content': nuevoPostre.json(),
            'message': 'Postre creado exitosamente'
        }, 201


class PostreController(Resource):
    def get(self, id):
        # asi es como se usa con la documentacion nativa de SQLAlchemy
        # https://docs.sqlalchemy.org/en/14/orm/query.html?highlight=filter_by#sqlalchemy.orm.Query.filter_by
        # SELECT * from postres where id = 1;
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        # otro_postre2 = base_de_datos.session.query(PostreModel).filter(PostreModel.postreId == id).first()

        # como la documentacion de flask sql alchemy
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records
        #postre = PostreModel.query.filter_by(postreId=id).first()
        return ({
            'success': True,
            'content': postre.json(),
            'message': None
        }, 200) if postre else ({
            'success': False,
            'content': None,
            'message': 'Postre no encontrado'
        }, 404)

    def put(self, id):
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        if postre:
            data = serializerPostres.parse_args()
            postre.postreNombre = data.get('nombre')
            postre.postrePorcion = data.get('porcion')
            postre.save()

            return {
                'success': True,
                'content': postre.json(),
                'message': 'Postre actualizado correctamente'
            }, 201
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Postre no encontrado'
            }, 404

    def delete(self, id):
        # METODO 1
        # # postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).delete()
        # # base_de_datos.session.commit()
        # METODO 2
        postre = base_de_datos.session.query(PostreModel).filter_by(postreId=id).first()
        if postre:
            postre.delete()
            return {
                'success': True,
                'content': postre.json(),
                'message': 'Postre eliminado exitosamente'
            }
        else:
            return {
                'success': False,
                'content': None,
                'message': 'Postre no existe'
            }


class BusquedaPostre(Resource):
    serializerBusqueda = reqparse.RequestParser()
    serializerBusqueda.add_argument(
        'nombre',
        type=str,
        location='args',
        required=False
    )
    serializerBusqueda.add_argument(
        'porcion',
        type=str,
        location='args',
        required=False,
        choices=('Familiar', 'Personal', 'Mediano'),
        help='Opcion invalida, las opciones son Familiar, Personal, Mediano'
    )

    def get(self):
        # Ejercicio
        # primero validar si hay nombre, porcion o ambos
        filtros = self.serializerBusqueda.parse_args()
        
        nombre = filtros.get('nombre')
        porcion = filtros.get('porcion')
        
        if nombre and porcion:
            resultado = base_de_datos.session.query(PostreModel).filter_by(
                postreNombre=nombre, postrePorcion=porcion).all()
        elif nombre:
            resultado = base_de_datos.session.query(PostreModel).filter_by(
                postreNombre=nombre).all()
        elif porcion:
            resultado = base_de_datos.session.query(
                PostreModel).filter_by(postrePorcion=porcion).all()
        else:
            return {
                'message': 'Necesitas dar al menos un parametro'
            }, 400
        # Recorremos el array de resultados y devolvemos el JSON
        resultado = [item.json() for item in resultado]
        return {
            'message': None,
            'content': resultado,
            'success': True
        }
