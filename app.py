from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Transaccion, Categoria, Base

app = Flask(__name__)

# Crear una sesión
engine = create_engine('sqlite:///transacciones.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/agregar_transaccion', methods=['POST'])
def agregar_transaccion():
    data = request.json
    nueva_transaccion = Transaccion(
        descripcion=data['descripcion'],
        categoria=data['categoria'],
        monto=data['monto'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d'),
        tipo=data['tipo']
    )
    session.add(nueva_transaccion)
    session.commit()
    return jsonify({'mensaje': 'Transacción agregada'})

@app.route('/obtener_transacciones', methods=['GET'])
def obtener_transacciones():
    categoria = request.args.get('categoria')
    if categoria:
        transacciones = session.query(Transaccion).filter_by(categoria=categoria).order_by(Transaccion.fecha.desc()).all()
    else:
        transacciones = session.query(Transaccion).order_by(Transaccion.fecha.desc()).all()
    return jsonify([{
        'id': t.id,
        'descripcion': t.descripcion,
        'categoria': t.categoria,
        'monto': t.monto,
        'fecha': t.fecha.strftime('%Y-%m-%d'),
        'tipo': t.tipo
    } for t in transacciones])

@app.route('/eliminar_transaccion/<int:id>', methods=['DELETE'])
def eliminar_transaccion(id):
    transaccion = session.query(Transaccion).get(id)
    if transaccion:
        session.delete(transaccion)
        session.commit()
        return jsonify({'mensaje': 'Transacción eliminada'})
    else:
        return jsonify({'mensaje': 'Transacción no encontrada'}), 404

@app.route('/editar_transaccion/<int:id>', methods=['PUT'])
def editar_transaccion(id):
    data = request.json
    transaccion = session.query(Transaccion).get(id)
    if transaccion:
        transaccion.descripcion = data['descripcion']
        transaccion.categoria = data['categoria']
        transaccion.monto = data['monto']
        transaccion.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d')
        transaccion.tipo = data['tipo']
        session.commit()
        return jsonify({'mensaje': 'Transacción actualizada'})
    else:
        return jsonify({'mensaje': 'Transacción no encontrada'}), 404

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    data = request.json
    nueva_categoria = Categoria(nombre=data['nombre'])
    session.add(nueva_categoria)
    session.commit()
    return jsonify({'mensaje': 'Categoría agregada'})

@app.route('/obtener_categorias', methods=['GET'])
def obtener_categorias():
    categorias = session.query(Categoria).all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre
    } for c in categorias])

@app.route('/eliminar_categoria/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    categoria = session.query(Categoria).get(id)
    if categoria:
        session.delete(categoria)
        session.commit()
        return jsonify({'mensaje': 'Categoría eliminada'})
    else:
        return jsonify({'mensaje': 'Categoría no encontrada'}), 404

@app.route('/editar_categoria/<int:id>', methods=['PUT'])
def editar_categoria(id):
    data = request.json
    categoria = session.query(Categoria).get(id)
    if categoria:
        categoria.nombre = data['nombre']
        session.commit()
        return jsonify({'mensaje': 'Categoría actualizada'})
    else:
        return jsonify({'mensaje': 'Categoría no encontrada'}), 404

@app.route('/datos_reportes', methods=['GET'])
def datos_reportes():
    resumen_mensual = session.query(
        Transaccion.fecha,
        Transaccion.tipo,
        Transaccion.monto
    ).all()
    
    # Crear un diccionario para agrupar los datos por mes
    resumen_por_mes = {}
    for transaccion in resumen_mensual:
        mes = transaccion.fecha.strftime('%B')
        if mes not in resumen_por_mes:
            resumen_por_mes[mes] = {'ingresos': 0, 'gastos': 0}
        if transaccion.tipo == 'entrada':
            resumen_por_mes[mes]['ingresos'] += transaccion.monto
        else:
            resumen_por_mes[mes]['gastos'] += transaccion.monto
    
    resumen_mensual_datos = [
        {'mes': mes, 'ingresos': valores['ingresos'], 'gastos': valores['gastos']}
        for mes, valores in resumen_por_mes.items()
    ]

    desglose_categoria = session.query(
        Transaccion.categoria,
        Transaccion.tipo,
        Transaccion.monto
    ).all()

    # Crear un diccionario para agrupar los datos por categoría
    desglose_por_categoria = {}
    for transaccion in desglose_categoria:
        if transaccion.tipo == 'salida':  # Solo considerar los gastos
            if transaccion.categoria not in desglose_por_categoria:
                desglose_por_categoria[transaccion.categoria] = 0
            desglose_por_categoria[transaccion.categoria] += transaccion.monto
    
    desglose_categoria_datos = [
        {'categoria': categoria, 'monto': monto}
        for categoria, monto in desglose_por_categoria.items()
    ]

    # Obtener la fecha de la última transacción
    ultima_transaccion = session.query(Transaccion).order_by(Transaccion.fecha.desc()).first()
    fecha_ultima_transaccion = ultima_transaccion.fecha.strftime('%Y-%m-%d') if ultima_transaccion else ''

    transacciones = session.query(Transaccion).all()
    transacciones_datos = [
        {
            'fecha': transaccion.fecha.strftime('%Y-%m-%d'),
            'descripcion': transaccion.descripcion,
            'categoria': transaccion.categoria,
            'monto': transaccion.monto,
            'tipo': transaccion.tipo
        }
        for transaccion in transacciones
    ]

    datos = {
        'resumenMensual': resumen_mensual_datos,
        'desgloseCategoria': desglose_categoria_datos,
        'transacciones': transacciones_datos,
        'fechaUltimaTransaccion': fecha_ultima_transaccion
    }

    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)
