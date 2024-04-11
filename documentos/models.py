from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # filename will be uploaded file's name
    # instance.usuario.username will be the username of the uploader
    return 'documentos/pdfs/{0}/{1}'.format(instance.usuario.id, filename)


class Documento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=user_directory_path)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    aprobado = models.BooleanField(default=False)
    aprobador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='aprobador', null=True, blank=True)

    def __str__(self):
      return f"{self.id} - {self.titulo} - {self.usuario.username} - {self.estado} - {self.aprobado}"
    