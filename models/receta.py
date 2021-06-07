from sqlalchemy.sql.expression import true
from config.conexion_bd import base_de_datos
from sqlalchemy import Column, types, ForeignKey


class RecetaModel(base_de_datos.Model):
    __tablename__ = 'recetas'
    recetaId = Column(name='id', type_=types.Integer, primary_key=True,
                      nullable=False, unique=True, autoincrement=True)
    recetaCantidad = Column(name='cantidad', type_=types.Integer)
    recetaUnidadMedida = Column(name='unidad_medida', type_=types.String(20))
    postre = Column(ForeignKey(column='postres.id'), name='postres_id',
                    type_=types.Integer, nullable=False)
    ingrediente = Column(
        ForeignKey(column='ingredientes.id'),
        name='ingredientes_id', type_=types.Integer, nullable=False)

    def __init__(self, cantidad, unidad_medida, postre, ingrediente) -> None:
        self.cantidad = cantidad
        self.unidad_medida = unidad_medida
        self.postre = postre
        self.ingrediente - ingrediente
