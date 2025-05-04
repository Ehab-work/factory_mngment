from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for reading user information.
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'role_display', 'address', 'salary', 'age', 'job_title', 
                 'phone_number', 'national_id', 'is_active', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 
                 'role', 'address', 'salary', 'age', 'job_title', 'phone_number', 'national_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
            
        # Validate phone number if provided
        if attrs.get('phone_number'):
            import re
            if not re.match(r'^\+?1?\d{9,15}$', attrs['phone_number']):
                raise serializers.ValidationError({"phone_number": "Phone number format is invalid."})
                
        # Validate national ID if provided
        if attrs.get('national_id'):
            import re
            if not re.match(r'^\d{14}$', attrs['national_id']):
                raise serializers.ValidationError({"national_id": "National ID must be exactly 14 digits."})
                
        # Validate age if provided
        if attrs.get('age') is not None:
            if attrs['age'] < 18 or attrs['age'] > 70:
                raise serializers.ValidationError({"age": "Age must be between 18 and 70."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for users to update their own profile.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number']
        
class ChangeRoleSerializer(serializers.Serializer):
    """
    Serializer for admins to change a user's role.
    """
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    
    def validate_role(self, value):
        if value not in [choice[0] for choice in User.ROLE_CHOICES]:
            raise serializers.ValidationError("Invalid role selection.")
        return value