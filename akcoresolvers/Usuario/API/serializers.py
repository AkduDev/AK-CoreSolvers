from rest_framework import serializers
from Usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo', 'telefono', 'carne_identidad', 'password']

    def create(self, validated_data):
       
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()

        return usuario