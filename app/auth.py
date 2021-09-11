from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import *


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        print(request.POST)
        user = Usuario.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['usuario'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = Usuario.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_nombre'] =  request.POST['nombre']
            request.session['register_apellido'] =  request.POST['apellido']
            request.session['register_email'] =  request.POST['email']
            

        else:
            request.session['register_nombre'] = ""
            request.session['register_apellido'] =  ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = Usuario.objects.create(
                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                email=request.POST['email'],
                password=password_encryp,
                
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            usuario = {
                "id" : usuario_nuevo.id,
                "nombre": usuario_nuevo.nombre,
                "apellido": usuario_nuevo.apellido,
                "email": usuario_nuevo.email,
                
            }

            request.session['usuario'] = usuario
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')
