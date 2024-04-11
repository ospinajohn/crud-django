"""
URL configuration for gestion_documentos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from documentos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup , name='signup'),
    path('documentos/', views.documentos_viws, name='documentos_usuario'),
    path('logout/', views.signout, name='logout'),
    path('login/', views.login_view, name='login'),
    path('upload/', views.upload_documento, name='upload_documento'),
    path('documentos/delete/<int:documento_id>', views.delete_documento, name='delete_documento'),
    path('documentos/edit/<int:documento_id>', views.update_documento, name='update_documento'),
    path('documentos/<int:documento_id>', views.detalle_documento, name='detalle_documento'),

    #admin
    path('documentos/admin', views.admin_documentos, name='admin_documentos'),
    path('documentos/admin/aprobar/<int:documento_id>', views.aprobar_documento, name='aprobar_documento'),
]

    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
