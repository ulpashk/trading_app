from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_image']

    def update(self, instance, validated_data):
        request = self.context.get('request')  # Get request from context

        # Allow only admins to update the 'role' field
        if 'role' in validated_data:
            if not request or request.user.role != "admin":
                validated_data.pop('role')  # Remove role from update data

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'profile_image']

    def validate_role(self, value):
        """
        Ensure only admins can create another admin user.
        """
        request = self.context.get('request')  # Get the request context
        if value == "admin":
            if not request or not request.user.is_authenticated or request.user.role != "admin":
                raise serializers.ValidationError("Only admins can create an admin user.")
        elif value not in ['trader', 'sales', 'customer']:
            raise serializers.ValidationError("Invalid role selected.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'customer'),
            profile_image=validated_data.get('profile_image', None),
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        refresh = RefreshToken.for_user(user)
        return {
            "message": "Login successful",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile_image']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance