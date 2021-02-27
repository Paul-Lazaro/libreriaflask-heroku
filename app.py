from flask import Flask ,request
from config.base_datos import bd
from flask_restful import Api
#from models.autor import AutorModel
from controllers.autor import AutoresController ,AutorController
#from models.categoria import  CategoriaModel
from controllers.categoria import CategoriaController
from models.libro import LibroModel
from controllers.libro import LibrosController,LibroModel,RegistroLibroSedeController
#from models.sede import SedeModel 
from controllers.sede import SedesController , LibroSedeController ,LibroCategoriaSedeController
#from models.sedeLibro import SedeLibroModel
from flask_cors  import CORS  #CONTROL DE ACCESO A LA API
#para la documenetaciom
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="" #esta variabñle se usa para indicar en que endpoint se encontrara la domumentacion
API_URL="/static/swagger.json" #se usa para indicar en q parte del proyecto se encuentra el archivo de la documentacion 
swagger_blueprint= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name":"Libreria Flask - SwaggerDocumentation"
    }
        
    
)


app=Flask(__name__)
app.register_blueprint(swagger_blueprint)

#formato://username:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI']='mysql://numjmbfsfzvdbzfp:f4xhk9fzmaayj85s@d6rii63wp64rsfb5.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/t7pdjw13yz44k2hq'
api =Api(app)
CORS(app) #PREMITIENDO TODOS LOS METODOS,DOMINIOS Y HEADERS

         # si tu servidfor no tiene contraseña
         #"mysql://root:@localhost:3306/flasklibreria"
#para evitar el warning de la funcionalidad de sqlalchemy de track modification:

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Inicio la aplñoicacion proveyendo las credenciales indivcadas en el app.config pero aun no se ha conectado a la BD

bd.init_app(app)
#Borrar base de datos mapeadas
#bd.drop_all(app=app)
#Recien se conecta a la BD , pero necesita el driver para poder conectarse : pip install mysqlclient
bd.create_all(app=app)

@app.route("/buscar")
def buscarLibro():
    print(request.args.get("palabra"))
    #de acuerdo a la palabra mandada q me de el resultado de la busqueda de todos los libros , sino hay ningun libro con esa palabra o no se mando la palabra indicar q la biusqueda no tuvo efecto con un BAD REQUESR

    palabra=request.args.get("palabra")
    if palabra:
        resultadoBusqueda=LibroModel.query.filter(LibroModel.libroNombre.like("%"+palabra+"%")).all()
        if resultadoBusqueda:
            resultado=[]
            for libro in resultadoBusqueda:
                resultado.append(libro.json())
                return{
                    "success":True,
                    "content": resultado,
                    "message":None
                     
                }
    return{
        "success":False,
        "content":None,
        "message":"No se encontro nada para buscar o la busqueda no tuvo exito"
    },400



 
#RUTAS DE MI API RESTFUL

api.add_resource(AutoresController,'/autores')
api.add_resource(AutorController, "/autor/<int:id>")
#/categorias /categforia con cualquiera de las dos 
api.add_resource(CategoriaController, "/categorias","/categoria")
api.add_resource(LibrosController, "/libro","/libros")
api.add_resource(SedesController,"/sedes","/sede")
api.resource(LibroSedeController,"/" )
api.add_resource(LibroCategoriaSedeController, "/busquedaLibroSedeCat")
api.add_resource(RegistroLibroSedeController, "/registrarSedesLibro")
if __name__=="__main__":
    app.run(debug=True)
    