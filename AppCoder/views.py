from django.shortcuts import render
from .models import Curso, Profesor, Estudiante, Avatar
from .forms import ProfesorForm, RegistroUsuarioForm, UserEditForm, AvatarFormulario
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required #para vistas basadas en funciones DEF  
from django.contrib.auth.mixins import LoginRequiredMixin #para vistas basadas en clases CLASS   

from django.contrib.auth.models import User

# Create your views here.

def crear_curso(request):

    nombre_curso="Programacion"
    comision_curso=10010
    print("Creando curso")
    curso=Curso(nombre=nombre_curso, comision=comision_curso)
    curso.save()
    respuesta=f"Curso creado--- {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

    
def cursos(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    return render(request, "AppCoder/cursos.html", {"avatar": avatar})


@login_required
def profesores(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass

    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            profesor = Profesor()
            profesor.nombre = form.cleaned_data['nombre']
            profesor.apellido = form.cleaned_data['apellido']
            profesor.email = form.cleaned_data['email']
            profesor.profesion = form.cleaned_data['profesion']
            profesor.save()
            form = ProfesorForm()
    else:
        form = ProfesorForm()

    profesores = Profesor.objects.all() #Profesor.objects.filter(nombre__icontains="P").all()
    
    return render(request, "AppCoder/profesores.html", {"profesores": profesores, "form" : form, "avatar": avatar})

@login_required
def busquedaComision(request):
    
    return render(request, "AppCoder/busquedaComision.html")

@login_required
def buscar(request):
    
    comision= request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision)#buscar otros filtros en la documentacion de django
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje": "Che Ingresa una comision para buscar!"})

@login_required
def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    print(profesor)
    profesor.delete()
    profesores=Profesor.objects.all()
    form = ProfesorForm()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado correctamente", "form": form})


@login_required
def editarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form= ProfesorForm(request.POST)
        if form.is_valid():
            
            info=form.cleaned_data
            
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]

            profesor.save()
            profesores=Profesor.objects.all()
            form = ProfesorForm()
            return render(request, "AppCoder/Profesores.html" ,{"profesores":profesores, "mensaje": "Profesor editado correctamente", "form": form})
        pass
    else:
        formulario= ProfesorForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
        return render(request, "AppCoder/editarProfesor.html", {"form": formulario, "profesor": profesor})
@login_required
def estudiantes(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    return render(request, "AppCoder/estudiantes.html", {"avatar":avatar})

def entregables(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    return render(request, "AppCoder/entregables.html", {"avatar":avatar})

def inicio(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    return HttpResponse("Bienvenido a la pagina principal", {"avatar", avatar})


def inicioApp(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    # print(avatar.imagen)
    return render(request, "AppCoder/inicio.html", {"avatar":avatar})


# vistas basadas en clases:

class EstudianteList(LoginRequiredMixin, ListView):#vista usada para LISTAR
    model= Estudiante
    template_name= "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteDetalle(LoginRequiredMixin, DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(LoginRequiredMixin, DeleteView):#vista usada para ELIMINAR
    model=Estudiante
    success_url= reverse_lazy("estudiante_list")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']


#login logout register

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            info=form.cleaned_data
            
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)#verifica si el usuario existe, si existe, lo devuelve, y si no devuelve None 
            
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente"})
            else:
                return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
    else:
        form=AuthenticationForm()
        return render(request, "AppCoder/login.html", {"form": form})




def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get("username")
            form.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {username} creado correctamente"})
        else:
            return render(request, "AppCoder/register.html", {"form": form, "mensaje":"Error al crear el usuario"})
    else:
        form= RegistroUsuarioForm()
        return render(request, "AppCoder/register.html", {"form": form})
    

@login_required
def editarPerfil(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            usuario.username = informacion['username']
            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.password2 = informacion['password2']
            usuario.last_name = informacion['last_name']
            usuario.first_name = informacion['first_name']

            usuario.save()

            return render(request, "AppCoder/inicio.html")

    else:

        miFormulario = UserEditForm(initial={
            'email': usuario.email,
            'username': usuario.username,
            'last_name': usuario.last_name,
            'first_name': usuario.first_name,
            })

    return render(request, "AppCoder/editarPerfil.html", {"miFormulario": miFormulario, "usuario": usuario, "avatar": avatar})


@login_required
def agregar_avatar(request):
    try:
        avatar = Avatar.objects.filter(user=request.user.id).last()
        print(avatar)
    except:
        avatar = None
        pass
    if request.method == 'POST':
        miFormulario = AvatarFormulario(request.POST, request.FILES)

        if miFormulario.is_valid():
            u = User.objects.get(username=request.user)

            avatar = Avatar(user=u, imagen=miFormulario.cleaned_data["imagen"])

            avatar.save()

            return render(request, "AppCoder/inicio.html", {"avatar":avatar})
    else:
        miFormulario = AvatarFormulario()
    
    return render(request, "AppCoder/agregarAvatar.html", {"miFormulario":miFormulario, "avatar":avatar})