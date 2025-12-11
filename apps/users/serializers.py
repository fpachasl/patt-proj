from rest_framework import serializers
from .models import CompanyUser, Role, User, Company, UserActionLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CompanyUserNestedSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = CompanyUser
        fields = ['company_name', 'role_in_company', 'joined_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Agrega campos personalizados del modelo User
        data['username'] = self.user.username
        data['rol_id'] = self.user.role.id if self.user.role else None
        data['id'] = self.user.id if self.user.id else None

        return data

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Role

class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Company
    
class UserActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = UserActionLog
        

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'cellphone', 'first_name', 'last_name']
        
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    company_user = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'cellphone',
            'first_name', 'last_name',
            'role', 'company_user', 'actions',
            'created_at', 'updated_at'
        ]

    def get_company_user(self, obj):
        company_user = CompanyUser.objects.filter(user=obj).select_related('company').first()
        if company_user:
            return CompanyUserNestedSerializer(company_user).data
        return None

    def get_actions(self, obj):
        logs = UserActionLog.objects.filter(user=obj).order_by('-timestamp')[:5]
        return UserActionLogSerializer(logs, many=True).data