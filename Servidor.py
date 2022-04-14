#Se importan las librerias
import json
from flask import Flask, request
from datetime import datetime 
app = Flask(__name__)

#Se Crean los Arreglos
Libros = []
Prestamistas = []
Prestamos = []

#Se lee el archivo Libros.json y el contenido en el arreglo Libros
with open('Libros.json') as json_Libros:
        Libros = json.load(json_Libros)

#Se lee el archivo Prestamistas.json y el contenido en el arreglo Prestamistas        
with open('Prestamistas.json') as json_Prestamista:
        Prestamistas = json.load(json_Prestamista)

#Se lee el archivo Prestamo.json y el contenido en el arreglo Prestamos        
with open('Prestamos.json') as json_Prestamo:
        Prestamos = json.load(json_Prestamo)
 
#Se da un mensaje de inicio.    
@app.route('/')
def hello():
    return {'Server' : 'ON'}

#ENDPOINT Crear Libro, Metodo POST
@app.route('/book', methods=['POST'])
#Metodo que Crear Libro
def Crear_Libro():
    libro = request.get_json()
    registrado = False
    try:
        #Se valida que los campos ingresados se guarden en el archivo libro.json
        if("isbn" in libro and "author" in libro and "title" in libro and "edition" in libro and "year" in libro and "no_copies" in libro and "no_available_copies" in libro and "no_bookshelf" in libro and "no_bookshelf_row" in libro):
            Libros = Leer_Libros()
            #Se recorre el arreglo Libro
            for lib in Libros:
                #Se verifica que el libro que se intenta registrar no exista.
                if(lib['isbn'] == libro['isbn']):
                    registrado = True        
            if(not registrado):
                #Se guardan los datos en el archivo Libro.json
                Libros.append(libro)
                GuardarLibros(Libros)
                #Se agregan mensaje, y el codigo de estado HTTP
                return {'msg' : 'Libro Creado con Exito'},200
            else:
                #Se agregan mensaje, y el codigo de estado HTTP
                return {'msg' : 'El Libro Ingresado Ya se Encuentra Registrado'},400
        else:
            #Se agregan mensaje, y el codigo de estado HTTP
            return {'msg' : 'Faltan Datos Del Libro'},400
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg': 'ocurrió un error en el servidor'},500

#ENDPOINT Actualizar Libro, Metodo PUT
@app.route('/book', methods=['PUT'])
#Metodo que Actualizar Libro
def Actualizar_Libros():
    actuali_libro = request.get_json()
    try:
        #Se valida que los campos ingresados se guarden en el archivo libro.json
        if("isbn" in actuali_libro and "author" in actuali_libro and "title" in actuali_libro and "year" in actuali_libro):
            Libros = Leer_Libros()
            #Se recorre el arreglo Libro
            for lib in Libros:
                #Se verifica que el isbn ingresado exista en el Arreglo Libros
                if(lib['isbn'] == actuali_libro['isbn']):
                    #Se Cambian los datos nuevos ingresados.
                    lib['author'] = actuali_libro['author']
                    lib['title'] = actuali_libro['title']
                    lib['year'] = actuali_libro['year']
                    #Se Guardan los cambios en el Archivo Libros.json y en el Arreglo
                    GuardarLibros(Libros)
                    #Se agregan mensaje, y el codigo de estado HTTP
                    return {'msg' : 'Libro Actualizado con Exito'},200
            #Se agregan mensaje, y el codigo de estado HTTP
            return {'msg' : 'El ISBN Ingresado No Existe'},400
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg' : 'Faltan Datos Del Libro'},400        
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg' : 'ocurrió un error en el servidor'},500    

#ENDPOINT Buscar Libro, Metodo GET 
@app.route('/book', methods=['GET'])
#Metodo Buscar Libro
def Buscar_Libro():
    Libros = Leer_Libros() 
    #Se establecen los parametros por los cuales se realizara la busqueda
    title = request.args.get('title')
    year_from = request.args.get('year_from')
    year_to = request.args.get('year_to')
    author = request.args.get('author')
    resultados = []
    try:
        #Se valida que
        if(title != None):
            #Se recorre el arreglo Libros
            for lib in Libros:
                #Se valida que el titulo del libro buscado exista en el arreglo Libros
                if(lib['title'] == title):
                    resultados.append(lib)
            #Retornara el resultado del titulo encontrado.
            return json.dumps(resultados),200

        if(author != None):
            #Se recorre el arreglo Libros
            for lib in Libros:
                #Se valida que el autor buscado exista en el arreglo Libros
                if(lib['author'] == author):
                    resultados.append(lib)
            #Retornara el resultado del titulo encontrado.
            return json.dumps(resultados),200

        if(year_from != None and year_to != None): 
            #Se recorre el arreglo Libro
            for lib in Libros:
                #Se valida el intervalo de fechas buscadas coincida en el arreglo Libros
                if(lib['year'] >= int(year_from) and lib['year'] <= int(year_to)):
                    resultados.append(lib)
            #Retornara el resultado del titulo encontrado.
            return json.dumps(resultados),200
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg': 'ocurrió un error en el servidor'},500

#ENDPOINT Crear Prestamista, Metodo POST 
@app.route('/person', methods=['POST'])
def Crear_Prestamista():
    #Se crean las variables
    prestamista = request.get_json()
    registrado = False
    try:
        #Se valida que los datos ingresados se guarden en el arreglo Prestamista y el archivo Prestamistas.json
        if("cui" in prestamista and "last_name" in prestamista and "first_name" in prestamista):
            Prestamistas = Leer_Prestamistas()
            #Se recorre el archivo Prestamistas
            for pres in Prestamistas:
                #Se valida que el CUI a registrar no exista en Arreglo Prestamistas
                if(pres['cui'] == prestamista['cui']):
                    registrado = True
            #Se valida que el Prestamista no esta Registrado
            if(not registrado):
                #Se guarda el prestamista en el Arreglo Prestamistas
                Prestamistas.append(prestamista)
                print(prestamista)
                Guardar_Prestamista(Prestamistas)
                #Se agregan mensaje, y el codigo de estado HTTP
                return {'msg' : 'Prestamista Creado Con Exito'},200
            else:
                #Se agregan mensaje, y el codigo de estado HTTP
                return {'msg' : 'El Prestamista Ya Se Encuentra Registrado'},400
        else:
            #Se agregan mensaje, y el codigo de estado HTTP
            return{'msg' : 'Faltan Datos del Prestamista'},400
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return{'msg' : 'Ocurrio un Error en el Servidor'},500

#ENDPOINT Consultar Prestamista, Metodo GET                 
@app.route('/person/<cui>', methods=['GET'])
#Metodo Consultar Prestamista
def Consultar_Prestamista(cui):
    #Se Crean las variables
    Prestamistas = Leer_Prestamistas()
    Prestamos = Leer_Prestamo()
    datos_prestamo = {}
    record = {}
    try:
        #Se recorre el arreglo Prestamistas
        for pres in Prestamistas:
            #Se valida que el CUI buscado exista en el Arreglo Prestamista
            if(pres['cui'] == cui):
                #Se mostrara los datos del CUI buscado
                datos_prestamo['first_name'] = pres['first_name']
                datos_prestamo['last_name'] = pres['last_name']
                datos_prestamo['record'] = []
                #Se recorre el arreglo Prestamo
                for rec in Prestamos:
                    #Se valida que el CUI buscado exista en el arreglo Record
                    if(cui == rec['cui']):
                        #Se mostrara los datos de los prestamos realizados por el Prestamista
                        record['uuid'] = rec['uuid']
                        record['isbn'] = rec['isbn']
                        record['title'] = rec['title']
                        record['lend_date'] = rec['lend_date']
                        record['return_date'] = rec['return_date']
                        datos_prestamo['record'].append(record)
                        record = {}
                #Retornara los prestamos realizados por el Prestamista, y se agrega el codigo de estado HTTP
                return datos_prestamo,200
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg' : 'El CUI Ingresado NO Corresponde a Un Prestamista'},400
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg': 'ocurrió un error en el servidor'},500

#ENDPOINT Prestar Libro, Metodo POST 
@app.route('/borrow', methods=['POST'])
#Metodo Prestar Libro
def Prestar_Libro():
    #Se crean las variables
    Libros = Leer_Libros()
    Prestamistas = Leer_Prestamistas()
    Prestamos = Leer_Prestamo()
    prestamo = {}
    prestamo_activo = False
    cui = request.get_json()
    try:
        #Se recorre el arreglo Prestamistas
        for pres in Prestamistas: 
            #Se valida que el CUI ingresado exista en el arreglo Prestamistas
            if(pres['cui'] == cui['cui']):
                #Se recorre el arreglo Prestamos
                for prest in Prestamos:
                    #Se valida que CUI ingresado no tenga un Prestamo Activo 
                    if(prest['cui'] == cui['cui']):
                        if(prest['return_date'] == ''):
                            prestamo_activo = True
                #Se valida que CUI ingresado no tenga un Prestamo Activo
                if(not prestamo_activo):
                    #Se recorre el arreglo Libros
                    for lib in Libros:
                        #Se valida que el ISBN ingresado exista en el Arreglo Libros
                        if(lib['isbn'] == cui['isbn']):
                            #Se valida que el numero de copias disponibles sea mayor a 0, para poder dar el prestamo
                            if(lib['no_available_copies']>0):
                                #Si el numero de copias es mayor a 0, el numero de copias se restara en -1
                                lib['no_available_copies'] -=1
                                #Se crea un UUID, con la convinacion del CUI del Prestamista y el ISBN del libro prestado.
                                prestamo['uuid'] = cui['cui'] + '_' + str(cui['isbn'])
                                prestamo['cui'] = cui['cui']
                                prestamo['isbn'] = cui['isbn']
                                prestamo['title'] = lib['title']
                                #Se crea la variable con la cual se obtendra la hora.
                                now = datetime.now()
                                #Se obtiene la hora del prestamo
                                prestamo['lend_date'] = now.strftime('%d-%m-%Y %H:%M:%S')
                                prestamo['return_date'] = ''
                                #Se guarda el arreglo prestamo
                                Prestamos.append(prestamo)
                                #Se vacia el arreglo prestamo
                                prestamo = {}
                                #Se guarda el archivo Libros
                                GuardarLibros(Libros)
                                #Se guarda el archibo Prestamos
                                Guardar_Prestamo(Prestamos)
                                #Se agregan mensaje, y el codigo de estado HTTP
                                return{'msg' : 'Libro Prestado con Exito'},200
                            else:
                                #Se agregan mensaje, y el codigo de estado HTTP
                                return{'msg' : 'No Existen Copias Disponibles de Este Libro'},400
                    #Se agregan mensaje, y el codigo de estado HTTP
                    return{'msg' : 'El ISBN No Corresponde Con Ningun Libro Registrado'},400
                else:
                    #Se agregan mensaje, y el codigo de estado HTTP
                    return{'msg' : 'El Prestamista Posee un Prestamo Activo'},400
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg' : 'El CUI Ingresado No Corresponde con Ningun Prestamista'},400                 
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return {'msg': 'ocurrió un error en el servidor'},500

#ENDPOINT Devolver Libro, Metodo PATCH 
@app.route('/borrow/<uuid>', methods = ['PATCH'])
#Metodo Devolver Libro
def Devolver_Libro(uuid):
    #Se crean las variables
    Libros = Leer_Libros()
    Prestamos = Leer_Prestamo()
    try:
        #Se recorre el arreglo Prestamos
        for pres in Prestamos:
            #Se valida que el UUID ingresado exista en el arreglo Prestamos
            if(pres['uuid'] == uuid):
                #Se recorre el arreglo Libros
                for lib in Libros:
                    #Se valida que el el libro no se haya devuelto antes
                    if(pres['return_date'] == ""):
                        #Se valida que el ISBN ingresado exista en el arreglo Libros
                        if(pres['isbn'] == lib['isbn']):
                            #Si el ISBN existe, se sumara el numero de copias disponibles en +1
                            lib['no_available_copies'] += 1
                        #Se crea la variable, con  la que tomara la hora del momento de devolver el prestamo activo
                        now = datetime.now()
                        #Se tomara la hora de devolver el libro
                        pres['return_date'] = now.strftime('%d-%m-%Y %H:%M:%S')
                        #Se guardara el archivo Prestamos.json
                        Guardar_Prestamo(Prestamos)
                        #Se guardara el archivo Libros.json
                        GuardarLibros(Libros)  
                        #Se agregan mensaje, y el codigo de estado HTTP             
                        return {'msg' : 'El Libro se ha Devuelto con Exito'},200
                    else:
                        #Se agregan mensaje, y el codigo de estado HTTP
                        return{'msg' : 'El Libro que Desea Devolver ya se ha Devuelto'},400
        #Se agregan mensaje, y el codigo de estado HTTP
        return{'msg' : 'No se ha Encontrado el UUID'},400
    except:
        #Se agregan mensaje, y el codigo de estado HTTP
        return{'msg' : 'Error del Servidor'},500
    
#Metodo Archivo Libro.json    
def Leer_Libros():
    libros = None
    #Se recibe el archivo Libros.json
    with open('Libros.json') as json_Libros:
        #Se crea la variable libros, leyendo el archivo Libros.json
        libros = json.load(json_Libros)
    return libros

#Metodo Guardar Libros    
def GuardarLibros(lib):
    JsonLibros = json.dumps(lib)
    #Se recibe el archivo Libros.json
    with open('Libros.json', "w") as outfile:
        #Se escribe en el archivo Libros.json
        outfile.write(JsonLibros)

#Metodo Leer Prestamistas
def Leer_Prestamistas():
    prestamistas = None
     #Se recibe el archivo Prestamistas.json
    with open('Prestamistas.json') as json_Prestamista:
        #Se crea la variable libros, leyendo el archivo Prestamistas.json
        prestamistas = json.load(json_Prestamista)
    return prestamistas

#Metodo Guardar Prestamistas
def Guardar_Prestamista(pres):
    #Se recibe el archivo Prestamistas.json
    json_Prestamista = json.dumps(pres)
    #Se escribe en el archivo Prestamistas.json
    with open('Prestamistas.json', "w") as outfile:
        outfile.write(json_Prestamista)

#Metodo Leer Prestamos    
def Leer_Prestamo():  
    prestamos = None
     #Se recibe el archivo Prestamos.json
    with open('Prestamos.json') as json_Prestamo:
        #Se crea la variable libros, leyendo el archivo Prestamos.json
        prestamos = json.load(json_Prestamo)
    return prestamos      

#Metodo Guardar Prestamo        
def Guardar_Prestamo(prestamo):
    #Se recibe el archivo Prestamos.json
    json_Prestamo = json.dumps(prestamo)
    #Se escribe en el archivo Prestamos.json
    with open('Prestamos.json', "w") as outfile:
        outfile.write(json_Prestamo)

app.run()