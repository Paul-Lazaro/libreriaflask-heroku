from flask_restful import Resource,reqparse
from models.sede import SedeModel
from models.sedeLibro import SedeLibroModel

#get all sedes
#create sede
#vincula una sede con varios libros y viceversa (un libro con varias sedes)

serializer=reqparse.RequestParser(bundle_errors=True) #bundle_errors=True me devuelve todos los errores
serializer.add_argument(
    "sede_latitud",
    type=float,
    required=True,
    help="Falta la sede latitud",
    location="json",
    #es como un alias , es como se va allmar una vez q hemos usado el metodo parse_args(). NO RECOMENDABLE
    dest="latitud"
)
serializer.add_argument(
    "sede_ubicacion",
    type=str,
    required=True,
    help="Falta la sede ubicacion",
    location="json",
    dest="ubicacion"
)
serializer.add_argument(
    "sede_longitud",
    type=float,
    required=True,
    help="Falta la sede longitud",
    location="json",
    dest="longitud"
)


class SedesController(Resource):
    def post(self):
        data=serializer.parse_args()
        print(data)
        #SedeModel(data["sede_ubicacion"],data["sede_latitud"],data["sede_longitud"])
        #LOS TIPO DE DATOS Q NO SON NI NUMERICOS NI STRING =DECIMAL ,FECHA NOSE PUEDEN SERIALIZAR SE TIENEN QUE CONEVERTIR EN STRING EN EL MODELO
        nuevaSede=SedeModel(data["ubicacion"],data["latitud"],data["longitud"])
        nuevaSede.save()
        return {
            "success":True,
            "content":nuevaSede.json(),
            "message":"se creo la sede con exito"
        },201

    def get(self):
        sedes=SedeModel.query.all()
        resultado=[]
        for sede in sedes: 
            resultado.append(sede.json())
        return {
            "success":True,
            "content":resultado,
            "message":None
        }




#Busqueda de todos los libros de una sede con sius autores
class LibroSedeController(Resource):
    def get(self,id_sede):
 
        sede=SedeModel.query.filter_by(sedeId=id_sede).first()
        sedeLibros=sede.libros #Todas mi sedelibros
        libros=[]
        for sedeLibro in sedeLibros:
            libro = sedeLibro.libroSede.json()
            # agregar el autor de ese libro
            libro['autor'] = sedeLibro.libroSede.autorLibro.json()
             #agregando la categoria dek libro para solamnete su descripcion (no necesito el ID) 
            libro["categoria"]=sedeLibro.libroSede.categoriaLibro.json()
            del libro["categoria"]["categoria_id"]
            del libro["autor_id"]

            libros.append(libro)
            #libros.append(sedeLibro.libroSede.json())
            #print(sedeLibro.libroSede.json())
         
            resultado=sede.json()
            resultado["libros"]=libros
            return {
                "succes" :True,
                "content":resultado
        }


#Busqueda de todos los libros de una sede segun su categoria
#categoria 
#sede
#127.0.0.1:5000/buscarLibroCategoria?sede=1&categpria=2
class LibroCategoriaSedeController(Resource):
 
    def get (self):
        serializer.remove_argument("sede_latitud")
        serializer.remove_argument("sede_ubicacion")
        serializer.remove_argument("sede_longitud")
        serializer.add_argument(
            "categoria",
            type=int,
            required=True,
            help="Falta la categoria",
            location="args"
    )

        serializer.add_argument(
            "sede",
            type=int,
            required=True,
            help="Falta la sede",
            location="args"  #sirve para q me lo mande por el querystring (de forma dinamica)
         )

        data=serializer.parse_args()
        sede=SedeModel.query.filter_by(sedeId=data["sede"]).first()
        # Luego de mi sede ingresar a mi sede_libro->[]...,luego ingresar a mis libros  y hacer el filtro segun la categoria (data["categoria"])
        #print(sede.libros)
            
        libros=[]
#TODOS MI SEDE LIBRO
        for sedelibro in sede.libros: 
            if (sedelibro.libroSede.categoria==data["categoria"]):
                libros.append(sedelibro.libroSede.json())
           
        return {
            "success":True,
            "content":libros, 
        }
    

        
   