from django.contrib.auth.models import User
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'date_joined']
        extra_kwargs = {'username': {'required': False}}

    def change(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        try:
            if User.objects.filter(
                    username=validated_data['username']).exists() or User.objects.filter(
                    email=validated_data['email']).exists():
                raise serializers.ValidationError("User Already exists.")
            else:
                return self.change(instance, validated_data)
        except KeyError:
            return self.change(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
