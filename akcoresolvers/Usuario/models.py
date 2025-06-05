from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, telefono, carne_identidad, password=None):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        
        usuario = self.model(
            correo=self.normalize_email(correo),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            carne_identidad=carne_identidad,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, apellido, telefono, carne_identidad, password):
        usuario = self.create_user(
            correo=correo,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            carne_identidad=carne_identidad,
            password=password,
        )
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    # Campos personalizados
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    carne_identidad = models.CharField(max_length=20, unique=True)
    
    # Campos obligatorios para Django
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'correo'  
    REQUIRED_FIELDS = ['nombre', 'apellido', 'telefono', 'carne_identidad']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.correo})"




class SesionUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)  # Token único por sesión
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    ultima_actividad = models.DateTimeField(default=timezone.now)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Sesión de {self.usuario} ({self.fecha_inicio})"