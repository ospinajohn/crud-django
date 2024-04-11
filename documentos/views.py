import os
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from documentos.models import Documento

def es_administrador(user):
    return user.is_authenticated and user.is_staff

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                if request.POST["email"] == "admin@admin.com":
                    user = User.objects.create_superuser(
                        request.POST["email"], password=request.POST["password1"], first_name=request.POST["name"], last_name=request.POST["last_name"])
                else:
                    user = User.objects.create_user(
                        request.POST["email"], password=request.POST["password1"], first_name=request.POST["name"], last_name=request.POST["last_name"])
                user.save()
                login(request, user)
                return redirect('documentos_usuario')
            except IntegrityError:
                return render(request, 'signup.html', {"error": "Este email ya ha sido registrado."})
        else:
            return render(request, 'signup.html', {"error": "Las contraseñas no coinciden."})

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user = authenticate(request, username=request.POST["email"], password=request.POST["password"])
        if user is None:
            return render(request, 'login.html', {"error": "Usuario y/o contraseña incorrectos."})
        else:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_documentos')
            else:
                return redirect('documentos_usuario')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def documentos_viws(request):
    # obtener los documentos de la base de datos solo los que pertenecen al usuario logueado
    documentos = Documento.objects.filter(usuario=request.user, estado='activo')
    return render(request, 'documentos.html', {"documentos": documentos})

@login_required
def upload_documento(request):
    if request.method == 'GET':
        return render(request, 'subir_documento.html')
    else:
        if request.POST["titulo"] and request.POST["descripcion"] and request.FILES["archivo"]:
            documento = Documento()
            documento.titulo = request.POST["titulo"]
            documento.descripcion = request.POST["descripcion"]
            documento.archivo = request.FILES["archivo"]
            documento.fecha = timezone.now()
            documento.usuario = request.user
            documento.estado = 'activo'
            documento.save()
            return redirect('documentos_usuario')
        else:
            return render(request, 'subir_documento.html', {"error": "Todos los campos son requeridos."})
        
@login_required
def update_documento(request, documento_id):
    documento = get_object_or_404(Documento, pk=documento_id)
    if request.method == 'GET':
        return render(request, 'editar_documento.html', {"documento": documento})
    else:
        if request.POST["titulo"] and request.POST["descripcion"]:
            archivo_anterior = documento.archivo.path
            documento.titulo = request.POST["titulo"]
            documento.descripcion = request.POST["descripcion"]
            documento.archivo = request.FILES["archivo"]
            documento.fecha = timezone.now()
            documento.usuario = request.user
            documento.estado = 'activo'
            documento.save()
            # eliminar el archivo anterior
            if os.path.exists(archivo_anterior):
                os.remove(archivo_anterior)
            return redirect('documentos_usuario')
        else:
            return render(request, 'editar_documento.html', {"error": "Todos los campos son requeridos."})
        
@login_required
def delete_documento(request, documento_id):
    documento = get_object_or_404(Documento, pk=documento_id)
    documento.estado = 'inactivo'
    documento.save()
    return redirect('documentos_usuario')

@login_required
def detalle_documento(request, documento_id):
    documento = get_object_or_404(Documento, pk=documento_id)
    return render(request, 'detalle_documento.html', {"documento": documento})

@user_passes_test(es_administrador)
def admin_documentos(request):

    documentos = Documento.objects.filter(estado='activo', aprobado=False)
    return render(request, 'documentos_admin.html', {"documentos": documentos})

@user_passes_test(es_administrador)
def aprobar_documento(request, documento_id):
    documento = get_object_or_404(Documento, pk=documento_id)
    documento.aprobado = True
    documento.aprobador = request.user
    documento.save()
    return redirect('admin_documentos', {"mensaje": "Documento aprobado."})
