from operator import truediv
from flask_restful import Resource, reqparse
from models.autor import AutorModel
serializer = reqparse.RequestParser()
serializer.add_argument(
    'autor_nombre',
    type=str,
    required= True,
    help='Falta el autor_nombre'
)

class AutoresController(Resource):
    def post(self):
        informacion = serializer.parse_args()
        #"INSERT INTO T_AUTOR (AUTOR_NOMBRE) VALUES (INFORMACION['AUTOR_NOMBRE'])"
        # creamos una nueva instancia de nuestro modelo del Autor pero aun no se ha creado en la bd, esto sirve para validar que los campos ingresados cumplan con las definiciones de las columnas
        nuevoAutor = AutorModel(informacion['autor_nombre'])
        # ahora si se guarda en la bd, si hubiese algun problema dara el error de la BD pero ese indice (pk) si es autoincrementable salta una posicion
        nuevoAutor.save()
        print(nuevoAutor)
        return {
            'success': True,
            'content': nuevoAutor.json(), 
            'message': 'Autor creado exitosamente'
        }, 201
        
        def get(self):
            #"SELECT * FROM  T_AUTOR"
            lista_autores=AutorModel.query.all()
            resultado=[]
            for autor in lista_autores:
                resultado.append(autor.json())
                print(autor.json())
            return{
                "success":True,
                "content":resultado,
                "message":None
            }

class AutorController(Resource):
    def get(self,id):
        #.all() retorna todas las coincidencias  => Retorna una lista  de instancias
        #.first() retorna el primer registrpo de las coincidencias => retorna una instancia

        autorEncontrado=AutorModel.query.filter_by(autorId=id).first()
        print(autorEncontrado)
        if autorEncontrado is None:
              return {
                "succes" :False,
                "content":None,
                "message": "El autor no existe"
        },404
        else:
            return {
                "succes" :True,
                "content":autorEncontrado.json(),
                "message": None
        }

    def put(self,id):
        autorEncontrado=AutorModel.query.filter_by(autorId=id).first()
        # No siempre es necesaria hacer la validacion q el objeto exista puesto q el front se debe encargar de hacer esta validaciom
        if autorEncontrado:
            data=serializer.parse_args()
            autorEncontrado.autorNombre =data["autor_nombre"]
            autorEncontrado.save()
            return{
                "success":True,
                "content":autorEncontrado.json(),
                "message": "Se actualizo el autor con exito"
            },201
        else:
            return{
                "success":False,
                "content":None,
                "message":"No se encontro el autor a actualizar"
            },404

    def delete(self,id):
        autorEncontrado=AutorModel.query.filter_by(autorId=id).first()
        if autorEncontrado:
            autorEncontrado.delete()
            return {
                "success" : True,
                "content" :None,
                "message" :"Se elimino absolutamente el autor de la bd"
            }
        else:
            return {
                "success" :False,
                "content" :None,
                "message" :"No se encontro el autor a eliminar"
            },404
        



