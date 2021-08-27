from rest_framework import serializers

from django.contrib.auth import authenticate

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Serializing user registration and creating a new one. """

    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, allow_blank=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        password = data.get('password', None)
        username = data.get('username', None)

        if not username:
            raise serializers.ValidationError('A username is required to log in.')

        if not password:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('User with this email and password was not found')
        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated')

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """ Serializing and Deserializing User objects. """
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'last_name', 'first_name')

        # Параметр read_only_fields является альтернативой явному указанию поля
        # с помощью read_only = True, как мы это делали для пароля выше.
        # Причина, по которой мы хотим использовать здесь 'read_only_fields'
        # состоит в том, что нам не нужно ничего указывать о поле. В поле
        # пароля требуются свойства min_length и max_length,
        # но это не относится к полю токена.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """ Выполняет обновление User. """

        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            # Для ключей, оставшихся в validated_data мы устанавливаем значения
            # в текущий экземпляр User по одному.
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
