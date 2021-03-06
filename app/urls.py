from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index), 
    
    path('registro/', auth.registro),
    path('login/', auth.login),
    path('logout/', auth.logout),


    path('', views.index), 
    path('inicio/', views.inicio), 
    #path('añadircita/', views.añadircita),
    #path('añadirafavoritos/', views.añadirafavoritos),
    #path('añadirafavoritos/<int:id>', views.añadirafavoritos),
    #path('borrar/<int:id>', views.borrar),
    #path('usuario/<int:id>', views.usuario)
    path('perfil/<int:id>/', views.edit),
    path('editarperfil/<int:num>/', views.editarperfil),
    path('añadircita', views.añadircita),
    path('citas/', views.paginacitas),
    path('add_like/<int:num>/', views.post_likes),
    path('user/<int:id>/', views.page_user),
]
