from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, orm


class PostreModel(base_de_datos.Model):
    # para cambiar el nombre de la tabla en base de datos
    __tablename__ = 'postres'
    postreId = Column(name='id', primary_key=True, autoincrement=True,
                      unique=True, type_=types.Integer)
    postreNombre = Column(name='nombre', type_=types.String(length=45))
    postrePorcion = Column(name='porcion', type_=types.String(length=45))
    # El relationship =>  sirve para indicar  todos los hijos que puede tener ese modelo (todas sus FKs) que puedan existir en un determinado modelo
    # El backref => creara un atributo virtual en el model del hijo (Preparacion) para que pueda acceder a todo el objeto PostreModel sin la
    # necesidad de hacer una subconsulta (creara un Join cuando sea necesario)
    # lazy => define cuando SQLAlchemy va a cargar la data adyacente en la base de datos
    # True/'select': cargara los datos adyacentes
    # False/'join': solamente cargara cuando sea necesario (cuando se utilicen dichos datos)
    # 'subquery' => trabaja los datos PERO en una subconsulta
    # 'dynamic' => en este se pueden agregar filtros adicionales. SQLAlchemy devolvera otro objeto dentro de la clase
    prepaciones = orm.relationship('PreparacionModel', backref='preparacionPostre', lazy=True)
    recetas = orm.relationship('RecetaModel', backref='recetaPostre')

    def __init__(self, nombre, porcion):
        self.postreNombre = nombre
        self.postrePorcion = porcion
    
    def __str__(self) -> str:
        return f'El postre es {self.postreNombre}'
    
    def save(self):
        # El metodo session.add crea un nuevo registro en la base de datos PERO no lo guarda porque esta trabajandose 
        # mediante transacciones entonces esperara que se guarden de manera permanente haciendo un commit o rechazando 
        # todos los cambios mediante un rollback
        # la informacion ya existira en labd (select * from postres where id )
        base_de_datos.session.add(self)
        # ahora si todos los pasos de escritura, actualizacion y eliminacion de la bd fueron exitosos entonces se guardaran
        # todos los cambios de manera permanente.
        # todas las sesiones que esten pendientes de guardar PERMANENTE sus cambios en la bd al usar el commit se
        # guarda de forma permamente
        base_de_datos.session.commit()
        # metodo que sirve para cerrar la session en la bd.
        # base_de_datos.session.close()
    
    def json(self):
        return {
            'id': self.postreId,
            'postreNombre': self.postreNombre,
            'postrePorcion': self.postrePorcion
        }
    
    def delete(self):
        base_de_datos.session.delete(self)
        base_de_datos.session.commit()