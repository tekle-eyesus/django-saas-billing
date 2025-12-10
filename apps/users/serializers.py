from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.organizations.models import Organization

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organization_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'organization_name')

    def create(self, validated_data):
        org_name = validated_data.pop('organization_name')
        password = validated_data.pop('password')

        with transaction.atomic():
            org = Organization.objects.create(name=org_name, slug=org_name.lower().replace(' ', '-'))

            user = User.objects.create_user(
                **validated_data,
                organization=org,
                role='OWNER',  # First user is always the Owner
                username=validated_data['email'] 
            )
            user.set_password(password)
            user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    """ Used to read user data """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'organization_name')