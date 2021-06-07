from controllers.preparacion import PreparacionesController
from controllers.postre import BusquedaPostre, PostreController, PostresController
from models.receta import RecetaModel
from models.ingrediente import IngredienteModel
from config.conexion_bd import base_de_datos
from controllers.ingrediente import IngredienteController, IngredientesController
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

from os import environ

# CONFIGURAR SWAGGER
SWAGGER_URL = "/api/docs"  # Sirve para indicar en que ruta  se encontrara la documentacion
API_URL = "/static/swagger.json"  # Indicar la ubicacion del archivo json
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'Reposteria Flask - Swagger Documentation'}
)

# FIN DE CONFIGURACION

# from models.postre import PostreModel
# from models.preparacion import PreparacionModel


load_dotenv()

app = Flask(__name__)
# Srive para registrar en el caso que nosotros tengamos un proyecto interno para agregarlo a un proyecto principal
app.register_blueprint(swagger_blueprint)
api = Api(app)
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/?highlight=connection%20uri%20format#configuration
# dialect://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')

# si se establece en TRUE, Flask-SQLAlchemy rastreara las modificaciones de los objetos y lanzara señales, su valor predeterminado es None, igual habilita
# el tracking pero emite una advertencia que se deshabilitara de manera predeterminada en futuras versiones, esto consume memoria adicional y si no se
# va utilizar es mejor desactivarlo (False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_de_datos.init_app(app)
base_de_datos.create_all(app=app)


@app.route('/')
def initial_controller():
    return {
        "message": "Bienvenido a mi API de RECETAS DE POSTRES 🎂"
    }


# DEFINO LAS RUTAS USANDO FLASKRESTFUL
api.add_resource(PostresController, '/postres')
api.add_resource(PostreController, '/postres/<int:id>')
api.add_resource(BusquedaPostre, '/busqueda_postre')
api.add_resource(PreparacionesController, '/preparaciones', '/preparaciones/<int:postre_id>')
api.add_resource(IngredientesController, '/ingredientes')
api.add_resource(IngredienteController, '/ingrediente', '/ingrediente/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
