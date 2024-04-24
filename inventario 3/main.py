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
    minando = db.Column(db.Boolean, nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable = False)


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
      minando = True if 'minando' in request.form else False
      
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
      return redirect(url_for('get_paquetes'))
    else:
        empleados = Empleados.query.all()
        return render_template('index.html', empleado=empleados)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    paquete = Paquetes.query.get_or_404(id)
    if request.method == 'POST':
      paquete.minando = True if 'minando' in request.form else False 
      db.session.commit()
      return redirect(url_for('get_paquetes'))
    
    return render_template('formulariomod.html', paquete=paquete)

@app.route('/delete/<id>')
def delete(id):
    paquete = Paquetes.query.get(id)
    db.session.delete(paquete)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)