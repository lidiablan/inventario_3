"""from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
 from config.database import Session """
from flask import url_for, render_template, redirect, Flask, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Prueba3:Practicas2024%40@92.222.101.198/inventario3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lidia:abc123..@localhost/inventario3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Paquetes(db.Model):
    __tablename__ = "paquetes"
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(255), nullable=False)
    sn = db.Column(db.String(255), nullable=False)
    compañiaTransporte = db.Column(db.String(255), nullable=False)
    track = db.Column(db.String(255), nullable=False)
    tipoProducto = db.Column(db.String(255), nullable=False)
    origen = db.Column(db.String(255), nullable=False)
    destino = db.Column(db.String(255), nullable=False)
    minando = db.Column(db.Boolean, default=False, nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleados.id_empleado'), nullable = False)

class Empleados(db.Model):
    __tablename__ = "empleados"
    id_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    #paquetes = db.relationship('Paquetes', backref='empleado', lazy=True)

#PAQUETES
@app.route('/', methods=['GET'])
def get_paquetes():
    paquetes = Paquetes.query.all()
    return render_template('index.html', paquete=paquetes)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_paquete(id):
    paquete = Paquetes.query.get_or_404(id)
    return jsonify({
        'id': paquete.id,
        'fecha_hora': paquete.fecha_hora,
        'id_empleado': paquete.id_empleado,
        'descripcion' : paquete.descripcion,
        'sn' : paquete.sn,
        'compañiaTransporte' : paquete.compañiaTransporte,
        'track' : paquete.track,
        'tipoProducto' : paquete.tipoProducto,
        'origen' : paquete.origen,
        'destino' : paquete.destino,
        'minando' : paquete.minando,
    })

@app.route('/')
@app.route('/new', methods=['GET', 'POST'])
def formulario(id):
    if request.method == 'POST':
      id_empleado = int(request.form['id_empleado'])
      descripcion = request.form['descripcion']
      sn = request.form['sn']
      compañiaTransporte = request.form['compañiaTransporte']
      track = request.form['track']
      tipoProducto = request.form['tipoProducto']
      origen = request.form['origen']
      destino = request.form['destino']
      minando = True if 'minando' in request.form else False
      
      nuevo_paquete = Paquetes(
          id_empleado=id_empleado,
          descripcion=descripcion,
          sn=sn,
          compañiaTransporte=compañiaTransporte,
          track=track,
          tipoProducto=tipoProducto,
          origen=origen,
          destino=destino,
          minando=minando
      )
      
      db.session.add(nuevo_paquete)
      db.session.commit()
      return redirect('/' , str(nuevo_paquete.id))
    else:
        empleados = Empleados.query.all()
        return render_template('/', empleado=empleados)

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    paquete = Paquetes.query.get(id)
    if request.method == 'POST':
      paquete.minando = True if 'minando' in request.form else False
      db.session.commit()
      return redirect(url_for('get_paquetes'))
    
    return render_template('formulario mod.html', paquete=paquete)

@app.route('/delete/<id>', methods=['DELETE'])
def delete(id):
    paquete = Paquetes.query.get_or_404(id)
    db.session.delete(paquete)
    db.session.commit()
    flash("El paquete se eliminó correctamente")
    return redirect(url_for ('get_paquetes'))
   
#EMPLEADOS
@app.route('/', methods=['GET'])
def get_empleados():
    empleados = Empleados.query.all()
    return render_template('index.html', empleados=empleados)

@app.route('/')
@app.route('/index/<id>', methods=['GET'])
def get_empleado(id):
    empleado = Empleados.query.get_or_404(id)
    return jsonify({
        'id': empleado.id,
        'nombre': empleado.nombre,
        #'paquetes': empleado.paquete,
    })

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def formularioEmpleado(id):
    if request.method == 'POST':
      nombre = request.form['nombre']
      #paquetes = request.form['paquetes']
      
      nuevo_empleado = Empleados(
          nombre=nombre,
          #paquetes=paquetes
      )
      
      db.session.add(nuevo_empleado)
      db.session.commit()
      return redirect('/' , str(nuevo_empleado.id))

@app.route('/update/<id>', methods=['GET', 'POST'])
def updateEmpleado(id):
    empleado = Empleados.query.get(id)
    if request.method == 'POST':
      empleado.nombre = request.form["nombre"]
      #empleado.paquetes = request.form["paquetes"]
      db.session.commit()
      flash("El empleado se modificó correctamente")
      return redirect(url_for('get_empleados'))
    
    return render_template('empleadomod.html', empleado=empleado)

@app.route('/delete/<id>', methods=['DELETE'])
def deleteEmpleado(id):
    empleado = Empleados.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    flash("El empleado se eliminó correctamente")
    return redirect(url_for ('get_empleados'))

if __name__ == '__main__':
    app.run(debug=True)

'''
#Ver todos los empleados de baja
@app.get('/empleadosBaja', tags=['empleadosBaja'], response_model=dict, status_code=200)
def get_empleados_baja(self):
    result = self.db.query(EmpleadosBajaModel).all()
    return result

#Metodo para crear un empleado de baja
@app.post('/empleadosBaja', tags=['empleadosBaja'], response_model=dict, status_code=201)
def create_empleadoBaja(self, empleado: Empleados) -> dict:
    new_empleado_baja = EmpleadosBajaModel(**empleado.dict())
    self.db.add(new_empleado_baja)
    self.db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el empleado que esta de baja"})

#Metodo para modificar un empleado de baja
@app.put('/empleadosBaja/{id}', tags=['empleadosBaja'], response_model=dict, status_code=200)
def update_empleado_baja(self, id: int, data: Empleados)-> dict:
    empleadoBaja = self.db.query(EmpleadosBajaModel).filter(EmpleadosBajaModel.id == id).first()
    empleadoBaja.nombre = data.nombre
    empleadoBaja.fecha_hora = data.fecha_hora
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el empleado de baja"})

#Metodo para eliminar un empleado de baja
@app.delete('/empleadosBaja/{id}', tags=['empleadosBaja'], response_model=dict, status_code=200)
def delete_empleado_baja(self, id: int)-> dict:
    self.db.query(EmpleadosBajaModel).filter(EmpleadosBajaModel.id == id).delete()
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el empleado de baja"})

    self.db.query(PaquetesModel).filter(PaquetesModel.id == id).delete()
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el paquete"})

#Ver todos los paquetes devueltos
@app.get('/paquetesDevueltos', tags=['paquetesDevueltos'], response_model=dict, status_code=200)
def get_paquetes_devueltos(self):
    result = self.db.query(PaquetesDevueltosModel).all()
    return result

#Metodo para modificar un paquete devuelto
@app.put('/paquetesDevueltos/{id}', tags=['paquetesDevueltos'], response_model=dict, status_code=200)
def update_paquete_devuelto(self, id: int, movie: Paquetes)-> dict:
    paquetesDevuelto = self.db.query(PaquetesDevueltosModel).filter(PaquetesDevueltosModel.id == id).first()
    paquetesDevuelto.id = data.id
    paquetesDevuelto.id_paquete = data.id_paquete
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el paquete devuelto"})

#Metodo para eliminar un paquete devuelto
@app.delete('/paquetesDevueltos/{id}', tags=['paquetesDevueltos'], response_model=dict, status_code=200)
def delete_paquete_devuelto(self, id: int)-> dict:
    self.db.query(PaquetesDevueltosModel).filter(PaquetesDevueltosModel.id == id).delete()
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el paquete devuelto"})

#Ver todos los paquetes recogidos
@app.get('/paquetesRecogidos', tags=['paquetesRecogidos'], response_model=dict, status_code=200)
def get_paquetes_recogidos(self):
    result = self.db.query(PaquetesRecogidosModel).all()
    return result

#Ver un paquete recogido por su id
@app.get('/paquetesRecogidos/{id}', tags=['paquetesRecogidos'], response_model=dict)
def get_paquete_recogido(self, id: int = Path(ge=1, le=2000)):
    result = self.db.query(PaquetesRecogidosModel).filter(PaquetesRecogidosModel.id == id).first()
    return result

#Metodo para crear un paquete recogido
@app.post('/paquetesRecogido', tags=['paquetesRecogido'], response_model=dict, status_code=201)
def create_paquete_recogido(paquete: Paquetes) -> dict:
    new_paquete_recogido = PaquetesRecogidosModel(**paquete.dict())
    self.db.add(new_paquete_recogido)
    self.db.commit()
    return JSONResponse(status_code=201, content={"message": "Se ha registrado el paquete recogido"})

#Metodo para modificar un paquete recogido
@app.put('/paquetes/{id}', tags=['paquetes'], response_model=dict, status_code=200)
def update_paquete_recogido(self, id: int, movie: Paquetes)-> dict:
    paquetesRecogido = self.db.query(PaquetesRecogidosModel).filter(PaquetesRecogidosModel.id == id).first()
    paquetesRecogido.id = data.id
    paquetesRecogido.id_paquete = data.id_paquete
    paquetesRecogido.id_empleado = data.id_empleado
    paquetesRecogido.fecha_hora = data.fecha_hora
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado el paquete recogido"})

#Metodo para eliminar un paquete recogido
@app.delete('/paquetesRecogidos/{id}', tags=['paquetesRecogidos'], response_model=dict, status_code=200)
def delete_paquete_recogido(self, id: int)-> dict:
    self.db.query(PaquetesRecogidosModel).filter(PaquetesRecogidosModel.id == id).delete()
    self.db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado el paquete recogido"})
'''