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


def editarperfil(request, num): #get
    context = {"perfil": Usuario.objects.get(id=num)
    
    }
    return render(request, 'perfil.html', context)
    
def paginacitas(request):
    context = {"citas": Cita.objects.all(),
                "likes": Cita.objects.values_list('like', flat=True)
    }
    return render(request, 'citas.html', context)

def añadircita(request):

    errors = Cita.objects.validacioncita(request.POST)
    
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ("/citas/")
    else:
        Cita.objects.create(autor= request.POST['autor'],
        contenido_cita= request.POST['cita_text'],
        citado_por= User.objects.get(id=request.session['usuario'] ['id']))
        return redirect('/citas/')

def edit(request, id): #post

    errors = User.objects.validadoreditarperfil(request.POST)
    
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f"/edit_account/{id}/")
    else:
        ed_user = User.objects.get(id=id)
        ed_user.name = request.POST['editar_nombre']
        ed_user.last_name = request.POST['editar_apellido']
        ed_user.email = request.POST['editar_email']
        ed_user.save()
        return redirect("/citas/")

def post_likes(request, num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id= request.session['usuario'] ['id'])
    quote.like.add(user)

    return redirect("/citas/")

def page_user(request, id):

    context = {'perfil': User.objects.get(id=id),
                'perfil_quotes': Quote.objects.filter(citado_por=id)
    
    }
    return render(request, 'user.html', context)
