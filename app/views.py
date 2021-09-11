from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required,admin_requerido
from .models import *


@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)



def inicio(request): 
    # users = User.objects.all().exclude(id = request.session["user_id"]) 
    if "usuario_id" not in request.session: 
        return redirect("/")
    
    citas = Cita.objects.all()
    favoritas = Favorita.objects.filter(user_id = request.session["user_id"])

    for x in favoritas: 
        citas = cita.exclude(id = x.cita.id)

    #context = {
        #'citas': 'citas'
        #'favoritas': 'favoritas'
    #}
    #return render(request, 'registro.html', context)



@admin_requerido
def administrador(request):

    context = {
        'saludo': 'ADMINISTRADOR'
    }
    return render(request, 'admin.html', context)



#def añadircita(request):
        #if request.method == 'POST':


