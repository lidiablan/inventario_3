from flask import url_for, render_template, redirect, Flask, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Prueba3:Practicas2024%40@92.222.101.198/inventario3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Empleados(db.Model):
    __tablename__ = "empleados"
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    paquetes = db.Column(db.Integer, nullable = False)

class Paquetes(db.Model):
    __tablename__ = "paquetes"
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(180), nullable=False)
    sn = db.Column(db.String(255), nullable=False)
    compania_transporte = db.Column(db.String(255), nullable=False)
    track = db.Column(db.String(255), nullable=False)
    tipo_producto = db.Column(db.String(255), nullable=False)
    origen = db.Column(db.String(255), nullable=False)
    destino = db.Column(db.String(255), nullable=False)
    minando = db.Column(db.Boolean, default=False, nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable = False)
    
""" 
class Empleado_Baja(db.Model):
    __tablename__ = "empleado_baja"
    id = db.Column(db.Integer, primary_key=True)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable = False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)

class Paquetes_Devueltos(db.Model):
    __tablename__ = "paquetes_devueltos"
    id = db.Column(db.Integer, primary_key=True)
    id_paquete = db.Column(db.Integer, db.ForeignKey('paquetes.id'), nullable = False)
    
class Paquetes_Recogidos(db.Model):
    __tablename__ = "paquetes_recogidos"
    id = db.Column(db.Integer, primary_key=True)
    id_paquete = db.Column(db.Integer, db.ForeignKey('paquetes.id'), nullable = False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable = False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
"""

#PAQUETES
@app.route('/', methods=['GET'])
def get_paquetes():
    paquetes = Paquetes.query.all()
    return render_template('index.html', paquetes=paquetes)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_paquete(id):
    paquetes = Paquetes.query.get_or_404(id)
    return jsonify({
        'id': paquetes.id,
        'fecha_hora': paquetes.fecha_hora,
        'id_empleado': paquetes.id_empleado,
        'descripcion' : paquetes.descripcion,
        'sn' : paquetes.sn,
        'compania_transporte' : paquetes.compania_transporte,
        'track' : paquetes.track,
        'tipo_producto' : paquetes.tipo_producto,
        'origen' : paquetes.origen,
        'destino' : paquetes.destino,
        'minando' : paquetes.minando,
    })

@app.route('/')
@app.route('/', methods=['POST'])
def formulario():
    if request.method == 'POST':
      empleado = int(request.form['registrador'])
      descripcion = request.form['descripcion']
      sn = request.form['sn']
      compania_transporte = request.form['compania_transporte']
      track = request.form['track']
      tipo_producto = request.form['tipo_producto']
      origen = request.form['origen']
      destino = request.form['destino']
      #minando = True if 'minando' in request.form else False
      minando = request.form['minando']
      
      nuevo_paquete = Paquetes(
          id_empleado=empleado,
          descripcion=descripcion,
          sn=sn,
          compania_transporte=compania_transporte,
          track=track,
          tipo_producto=tipo_producto,
          origen=origen,
          destino=destino,
          minando=minando
      )
      
      db.session.add(nuevo_paquete)
      db.session.commit()
      return redirect('/' , str(nuevo_paquete.id))
    else:
        empleados = Empleados.query.all()
        return render_template('index.html', empleado=empleados)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    paquete = Paquetes.query.get_or_404(id)
    if request.method == 'POST':
      #paquete.minando = True if 'minando' in request.form else False
      paquete.minando = request.form["minando"]
      db.session.commit()
      return redirect(url_for('get_paquetes'))
    
    return render_template('formulariomod.html', paquete=paquete)

@app.route('/delete/<id>')
def delete(id):
    paquete = Paquetes.query.get(id)
    db.session.delete(paquete)
    db.session.commit()
    return redirect('/')
   
#EMPLEADOS
@app.route('/', methods=['GET'])
def get_empleados():
    empleados = Empleados.query.all()
    return render_template('index.html')

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_empleado(id):
    empleado = Empleados.query.get_or_404(id)
    return jsonify({
        'id': empleado.id,
        'nombre': empleado.nombre,
        'paquetes': empleado.paquete,
    })

@app.route('/empleado', methods=['POST'])
def formularioEmpleado():
    if request.method == 'POST':
      nombre = request.form['nombre']
      paquetes = request.form['paquetes']
      
      nuevo_empleado = Empleados(
          nombre=nombre,
          paquetes=paquetes
      )
      
      db.session.add(nuevo_empleado)
      db.session.commit()
      return redirect('/' , str(nuevo_empleado.id))
    else:
        empleados = Empleados.query.all()
        return render_template('formularioEmpleado.html', empleado=empleados)

@app.route('/updateEmpleado/<id>', methods=['GET', 'POST'])
def updateEmpleado(id):
    empleado = Empleados.query.get(id)
    if request.method == 'POST':
      empleado.nombre = request.form["nombre"]
      empleado.paquetes = request.form["paquetes"]
      db.session.commit()
      flash("El empleado se modificó correctamente")
      return redirect(url_for('get_empleados'))
    
    return render_template('formularioModEmpleado.html', empleado=empleado)

@app.route('/deleteEmpleado/<id>')
def deleteEmpleado(id):
    empleado = Empleados.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    flash("El empleado se eliminó correctamente")
    return redirect(url_for ('get_empleados'))

'''
#EMPLEADOS DE BAJA
@app.route('/', methods=['GET'])
def get_empleados_baja():
    empleadosBaja = Empleado_Baja.query.all()
    return render_template('index.html', empleados=empleadosBaja)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_empleado_baja(id):
    empleadoBaja = Empleado_Baja.query.get_or_404(id)
    return jsonify({
        'id': empleadoBaja.id,
        'id_empleado': empleadoBaja.id_empleado,
        'fecha_hora': empleadoBaja.fecha_hora
    })

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def formularioEmpleadoBaja(id):
    if request.method == 'POST':
      id_empleado = request.form['id_empleado']
      fecha_hora = request.form['fecha_hora']
      
      nuevo_empleado_baja = Empleado_Baja(
          id_empleado=id_empleado,
          fecha_hora=fecha_hora
      )
      
      db.session.add(nuevo_empleado_baja)
      db.session.commit()
      return redirect('/' , str(nuevo_empleado_baja.id))

@app.route('/update/<id>', methods=['GET', 'POST'])
def updateEmpleadoBaja(id):
    empleadoBaja = Empleado_Baja.query.get(id)
    if request.method == 'POST':
      empleadoBaja.id_empleado = request.form["id_empleado"]
      empleadoBaja.fecha_hora = request.form["fecha_hora"]
      db.session.commit()
      flash("El empleado de baja se modificó correctamente")
      return redirect(url_for('get_empleados_baja'))
    
    return render_template('empleadomod.html', empleado=empleado)

@app.route('/delete/<id>')
def deleteEmpleadoBaja(id):
    empleadoBaja = Empleado_Baja.query.get_or_404(id)
    db.session.delete(empleadoBaja)
    db.session.commit()
    flash("El empleado de baja se eliminó correctamente")
    return redirect(url_for ('get_empleados'))

#PAQUETES DEVUELTOS
@app.route('/', methods=['GET'])
def get_paquetes_devueltos():
    paquetesDevueltos = Paquetes_Devueltos.query.all()
    return render_template('index.html', paquetes=paquetesDevueltos)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_paquete_devuelto(id):
    paquetesDevueltos = Paquetes_Devueltos.query.get_or_404(id)
    return jsonify({
        'id': paquetesDevueltos.id,
        'id_paquete': paquetesDevueltos.id_paquete,
    })

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def formularioPaqueteDevuelto():
    if request.method == 'POST':
      id_paquete = request.form['id_paquete']
      
      nuevo_paquete_devuelto = Paquetes_Devueltos(
          id_paquete=id_paquete,
      )
      
      db.session.add(nuevo_paquete_devuelto)
      db.session.commit()
      return redirect('/' , str(nuevo_paquete_devuelto.id))

@app.route('/update/<id>', methods=['GET', 'POST'])
def updatePaqueteDevuelto(id):
    paqueteDevuelto = Paquetes_Devueltos.query.get_or_404(id)
    if request.method == 'POST':
      paqueteDevuelto.id_paquete = request.form["id_paquete"]
      db.session.commit()
      return redirect(url_for('/'))
    
    return render_template('formulariomod.html', paquete=paquete)

@app.route('/delete/<id>')
def deletePaqueteDevuelto(id):
    paqueteDevuelto = Paquetes_Devueltos.query.get(id)
    db.session.delete(paqueteDevuelto)
    db.session.commit()
    return redirect('/')

#PAQUETES RECOGIDOS
@app.route('/', methods=['GET'])
def get_paquetes_recogidos():
    paquetesRecogidos = Paquetes_Recogidos.query.all()
    return render_template('index.html', paquetes=paquetesRecogidos)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_paquete_recogido(id):
    paquetesRecogidos = Paquetes_Recogidos.query.get_or_404(id)
    return jsonify({
        'id': paquetesRecogidos.id,
        'id_paquete': paquetesRecogidos.id_paquete,
        'id_empleado': paquetesRecogidos.id_empleado,
        'fecha_hora': paquetesRecogidos.fecha_hora,
    })

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def formularioPaqueteRecogido():
    if request.method == 'POST':
      id_paquete = request.form['id_paquete']
      id_empleado = request.form['id_empleado']
      fecha_hora = request.form['fecha_hora']
      
      nuevo_paquete_recogido = Paquetes_Recogidos(
          id_paquete=id_paquete,
          id_empleado=id_empleado,
          fecha_hora=fecha_hora,
      )
      
      db.session.add(nuevo_paquete_recogido)
      db.session.commit()
      return redirect('/' , str(nuevo_paquete_recogido.id))

@app.route('/update/<id>', methods=['GET', 'POST'])
def updatePaqueteRecogido(id):
    paqueteRecogido = Paquetes_Recogidos.query.get_or_404(id)
    if request.method == 'POST':
      paqueteRecogido.id_paquete = request.form["id_paquete"]
      paqueteRecogido.id_empleado = request.form["id_empleado"]
      paqueteRecogido.fecha_hora = request.form["fecha_hora"]
      db.session.commit()
      return redirect(url_for('/'))
    
    return render_template('formulariomod.html', paquete=paquete)

@app.route('/delete/<id>')
def deletePaqueteRecogido(id):
    paqueteRecogido = Paquetes_Recogidos.query.get(id)
    db.session.delete(paqueteRecogido)
    db.session.commit()
    return redirect('/')
'''

if __name__ == '__main__':
    app.run(debug=True)