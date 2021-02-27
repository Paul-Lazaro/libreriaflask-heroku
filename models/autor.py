from config.base_datos import bd
# https://docs.sqlalchemy.org/en/13/core/type_basics.html?highlight=datatypes
# Si aun no sabemos que tipos de datos podemos utilizar en sqlalchemy podemos usar:
# from sqlalchemy import types
class AutorModel(bd.Model):
    # para cambiar el nombre de la tabla a crearse
    __tablename__= "t_autor"
    autorId = bd.Column(
                        name="autor_id", # Nombre de la col en la bd
                        type_=bd.Integer, # tipo de dato en la bd
                        primary_key=True, # setear si va a ser pk o no
                        autoincrement= True, # setear si va a ser AI o no 
                        nullable= False, # setear si va a admitir valores nulos o no
                        unique=True, # si no se va a repetir el valor o no
                        )
    autorNombre = bd.Column(name="autor_nombre", type_=bd.String(45))
  #si no indicamos un backref flask  lo genera aleotoriamente  y ser amas complicado averigiuar su nombre
  #el backref sirve para usarse  en el modelo hijo (para q nos devuelva los datos del padre)
  #lazy define cuando SQALchemy va a cargar la data de la base de datos
  #select/True  es el valor por defecto , significa q SQALchemy cragara los datos segun seaa necesario
  #"join"/False  le dice a SQLALchemy q cargue la relacion enb la misma consukltausan un JOIN
  #subquery  trabaja como un join pero en su lugar de hacerlo en una misma consulta lo hara en una subconsulta 
  #dynamic es especial si se tiene muchos elementos y se deseA  aplicafr filtros adicionales .SQLALchemy devolvera otro objeto de consyta q se puede cus
    libros =bd.relationship("LibroModel",backref="autorlibro",lazy=True)#En el caso de fk se apunta al nombre de la tabla , mientras que en los realtionship se apunta al nombre del modelo
    #En el caso de los relationship normal no puede estar creado la tabla aun

    def __init__(self, nombreAutor):
        self.autorNombre = nombreAutor

    def __str__(self):
        return "{}:{}".format(self.autorId, self.autorNombre)

    
    def save(self):
        # el metodo session devuelve la sesion actual y evita que se cree una nueva sesion y asi relentizar la conexion a mi bd
        # el metodo add sirve para agregar toda mi instancia (mi nuevo autor) a un formato que sea valido para la bd
        bd.session.add(self)
        # el commit sirve para que los cambios realizados a la bd se hagan efecto, esto generalmente se usa con transacciones
        bd.session.commit()

    def json(self):
      return {
        "autor_id":self.autorId,
        "autor_nombre":self.autorNombre
      }

    def delete(self):
      # con el delete se hace la eliminacion temporal de la base de datos 
      bd.session.delete(self) # solo se borra de la memoria temporal no del disco duro
      bd.session.commit() #Aqui ya borra tosdo