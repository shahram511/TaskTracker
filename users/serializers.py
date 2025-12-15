from rest_framework import serializers
from .models import User, Profile
from django.contrib.auth.password_validation import validate_password
 
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True,required=True,label='تایید پسورد')
    phone_number = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['password', 'password_confirmation', 'email', 'phone_number']
        
        
    def validate_phone_number(self, value):
        if not value.startswith('09'):
            raise serializers.ValidationError('شماره تلفن باید با 09 شروع شود')
        if len(value) != 11:
            raise serializers.ValidationError('شماره تلفن باید 11 رقم باشد')
        if not value.isdigit():
            raise serializers.ValidationError('شماره تلفن باید عدد باشد')

        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('شماره تلفن قبلاً ثبت شده است')
        return value
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({'password': 'پسورد و تایید پسورد مطابقت ندارند'})
        return attrs
    
        

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),            
        )
        return user
    
    
class ProfileSerializer(serializers.ModelSerializer):   
    phone_number = serializers.CharField(source='user.phone_number', read_only=True) 
    
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'avatar', 'bio','created_at']
        read_only_fields = ['created_at']

    