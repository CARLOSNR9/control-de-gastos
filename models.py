from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Transaccion(Base):
    __tablename__ = 'transacciones'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    categoria = Column(String)
    monto = Column(Float)
    fecha = Column(DateTime)
    tipo = Column(String)  # "entrada" o "salida"

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)

# Conexión a la base de datos SQLite
engine = create_engine('sqlite:///transacciones.db')
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
