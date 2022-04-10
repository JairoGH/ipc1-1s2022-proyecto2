import json
from xmlrpc.client import Boolean
from flask import Flask, request
from flask import render_template
app = Flask(__name__)
Libros = []
Prestamistas = []
Prestamos = []

with open('Libros.json') as json_Libros:
        Libros = json.load(json_Libros)
        
with open('Prestamistas.json') as json_Prestamista:
        Prestamistas = json.load(json_Prestamista)
        
with open('Prestamos.json') as json_Prestamo:
        prestamos = json.load(json_Prestamo)
    
@app.route('/')
def hello():
    return {'Server' : 'ON'}

@app.route('/book', methods=['POST'])
def Crear_Libro():
    libro = request.get_json()
    registrado = False
    try:
        if("isbn" in libro and "author" in libro and "title" in libro and "edition" in libro and "year" in libro and "no_copies" in libro and "no_available_copies" in libro and "no_bookshelf" in libro and "no_bookshelf_row" in libro):
            Libros = Leer_Libros()
            for lib in Libros:
                if(lib['isbn'] == libro['isbn']):
                    registrado = True
            if(not registrado):
                Libros.append(libro)
                print (Libros)
                GuardarLibros(Libros)
                return {'msg' : 'Libro Creado con Exito'},200
            else:
                return {'msg' : 'El Libro Ingresado Ya se Encuentra Registrado'},400
        else:
            return {'msg' : 'Faltan Datos Del Libro'},400
    except:
        return {'msg': 'ocurrió un error en el servidor'},500

@app.route('/book', methods=['PUT'])
def Actualizar_Libros():
    actuali_libro = request.get_json()
    try:
        if("isbn" in actuali_libro and "author" in actuali_libro and "title" in actuali_libro and "year" in actuali_libro):
            Libros = Leer_Libros()
            for lib in Libros:
                if(lib['isbn'] == actuali_libro['isbn']):
                    lib['author'] = actuali_libro['author']
                    lib['title'] = actuali_libro['title']
                    lib['year'] = actuali_libro['year']
                    GuardarLibros(Libros)
                    return {'msg' : 'Libro Actualizado con Exito'},200
            return {'msg' : 'El ISBN Ingresado No Existe'},400
        return {'msg' : 'Faltan Datos Del Libro'},400        
    except:
        return {'msg' : 'ocurrió un error en el servidor'},500    
 
@app.route('/book', methods=['GET'])
def Buscar_Libro():
    Libros = Leer_Libros() 
    title = request.args.get('title')
    year_from = request.args.get('year_from')
    year_to = request.args.get('year_to')
    author = request.args.get('author')
    resultados = []
    
    if(title != None):
        for lib in Libros:
            if(lib['title'] == title):
                resultados.append(lib)
        return json.dumps(resultados),200
              
    if(author != None):
        for lib in Libros:
            if(lib['author'] == author):
                resultados.append(lib)
        return json.dumps(resultados),200
        
    if(year_from != None and year_to != None): 
        for lib in Libros:
            if(lib['year'] >= int(year_from) and lib['year'] <= int(year_to)):
                resultados.append(lib)
        return json.dumps(resultados),200
    return {'msg': 'ocurrió un error en el servidor'},500

@app.route('/person', methods=['POST'])
def Crear_Prestamista():
    prestamista = request.get_json()
    registrado = False
    try:
        if("cui" in prestamista and "last_name" in prestamista and "first_name" in prestamista):
            Prestamistas = Leer_Prestamistas()
            for pres in Prestamistas:
                if(pres['cui'] == prestamista['cui']):
                    registrado = True
            if(not registrado):
                Prestamistas.append(prestamista)
                print(prestamista)
                Guardar_Prestamista(Prestamistas)
                return {'msg' : 'Prestamista Creado Con Exito'},200
            else:
                return {'msg' : 'El Prestamista Ya Se Encuentra Registrado'},400
        else:
            return{'msg' : 'Faltan Datos del Prestamista'},400
    except:
        return{'msg' : 'Ocurrio un Error en el Servidor'},500
                
@app.route('/person/<cui>', methods=['GET'])
def Consultar_Prestamista(cui):
    Prestamistas = Leer_Prestamistas()
    try:
        for pres in Prestamistas:
            if(pres['cui'] == cui):
                return{'cui': pres['cui'],'first_name' : pres['first_name'],'last_name': pres['last_name']}
    except:
        return {'msg': 'ocurrió un error en el servidor'},500

@app.route('/borrow', methods=['POST'])
def Prestar_Libro():
    Prestamistas = Leer_Prestamistas()
    Libros = Leer_Libros()
    cui = request.get_json()
    for pres in Prestamistas:
            if(pres['cui'] == cui['cui']):
                for lib in Libros:
                    if(lib['isbn'] == cui['isbn']):
                        if(lib['no_available_copies']>=0):
                            lib['no_available_copies'] -=1
                            GuardarLibros(Libros)
                            return{'msg' : 'Libro Prestado con Exito'},200
                        else:
                            return{'msg' : 'No Existen Copias Disponibles de Este Libro'},400
                return{'msg' : 'El ISBN No Corresponde Con Ningun Libro Registrado'},400
            else:
                return {'msg' : 'El CUI Ingresado No Corresponde con Ningun Prestamista'},400                 

@app.route('/borrow/<uuid>', methods = ['PATCH'])
def Devolver_Libro(uuid):
    Prestamistas = Leer_Prestamistas()
    Libros = Leer_Libros()
    for pres in Prestamistas:
        if(pres['uuid'] == uuid):
            for lib in Libros:
                if(lib['isbn'] == pres['isbn']):
                    if(lib['no_available_copies' == lib['no_copies']]): 
                        return {} 

def Leer_Libros():
    libros = None
    with open('Libros.json') as json_Libros:
        libros = json.load(json_Libros)
    return libros
    
def GuardarLibros(lib):
    JsonLibros = json.dumps(lib)
    with open('Libros.json', "w") as outfile:
        outfile.write(JsonLibros)

def Leer_Prestamistas():
    prestamistas = None
    with open('Prestamistas.json') as json_Prestamista:
        prestamistas = json.load(json_Prestamista)
    return prestamistas

def Guardar_Prestamista(pres):
    json_Prestamista = json.dumps(pres)
    with open('Prestamistas.json', "w") as outfile:
        outfile.write(json_Prestamista)
      
def Leer_Prestamo():
    prestamos = None
    with open('Prestamos.json') as json_Prestamo:
        prestamos = json.load(json_Prestamo)
    return prestamos      
        
def Guardar_Prestamo(prestamo):
    json_Prestamo = json.dumps(prestamo)
    with open('Prestamos.json', "w") as outfile:
        outfile.write(json_Prestamo)

app.run()