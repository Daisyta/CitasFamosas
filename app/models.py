from django.db import models
import re

# Create your models here.
class UsuarioManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['nombre']) < 2:
            errors['nombre_len'] = "nombre debe tener al menos 2 caracteres de largo";

        if len(postData['apellido']) < 2:
            errors['apellido_len'] = "apellido debe tener al menos 2 caracteres de largo";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

        if not SOLO_LETRAS.match(postData['nombre']):
            errors['solo_letras'] = "solo letras en nombre porfavor"

        if len(postData['password']) < 4:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors

    
    def validador_edit(self, postData):
        
        errors = {}
        if postData['editar_nombre'] =='' or postData['editar_apellido'] =='' or postData['editar_email'] =='':
            errors['edit_campos'] = " los campos no pueden estar vacios"
        
        if User.objects.filter(email= postData['editar_email']).exclude(email=postData['editar_email']).exists():
            errors['email_existe'] = " El email que ingresaste ya existe"
        
        return errors


class Usuario(models.Model):
    CHOICES = (
        ("user", 'Usuario'),
        ("admin", 'Admin')
    )
    nombre = models.CharField(max_length=100)
    apellido = models.EmailField(max_length=255, unique=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def __repr__(self):
        return f"{self.nombre} {self.apellido}"
        
class CitaManager(models.Manager):

    def validacioncita(self, postData):
        
        errors = {}

        if len(postData['autor']) < 3:
            errors['autor'] = "El campo autor debe ser mayor a 3 caracteres"
        
        if len(postData['quote_text']) < 10:
            errors['cita_text'] = "El campo cita debe ser mayor a 10 caracteres"
        
        return errors


	# def validacionañadircita(self, contenido_cita, enviada_por, recibida_por):

    #     errors = {}

	# 	if len(contenido_cita) > 0:
    #                 cita =  Cita.objects.create(
    #                         contenido_cita=contenido_cita,
    #                         enviada_por_id=enviada_por,
    #                         recibida_por_id=recibida_por,
    #                 )
    #                 return cita
	# 	else:
    #                 return "La cita no puede estar en blanco!"

#una cita: quien la hace,la cita misma,quien la cita,quien le da likes
#un usuario puede hacer varias citas,por eso,es uno a muchos
# mi cita quoteada yo la puedo borrar,por eso el ondelete
#la cita puede tener likes
class Cita(models.Model):
    autor = models.CharField(max_length=255) 
    contenido_cita = models.CharField(max_length=255)
    citado_por = models.ForeignKey("Usuario", related_name="Micitaquoteada",on_delete=models.CASCADE)
    like = models.ManyToManyField("Usuario", related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = CitaManager()


#un usuario puede tener citas favoritas favoritas
# yo puedo tener citas fav mis favoritas
#class Favorita(models.Model):
    #usuario = models.ForeignKey("Usuario", related_name="favoritas")
    #cita = models.ForeignKey("Cita", related_name="miscitasfavoritas")