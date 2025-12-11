# apps/projects/serializers.py
from rest_framework import serializers

from apps.company.models import Company
from apps.company.serializer import CompanySerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer
from .models import AreaLeader, Project, ProjectArea, ProjectAreaMember, ProjectLeader, ProjectPriority, ProjectState, ProjectType

class ProjectPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPriority
        fields = ['id', 'name', 'description']

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ['id', 'name', 'description']

class ProjectStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectState
        fields = ['id', 'name', 'description']

# Serializers de relaciones
class ProjectLeaderSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    leader_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source="leader"
    )
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        write_only=True,
        source="project"
    )

    class Meta:
        model = ProjectLeader
        fields = ['id', 'leader', 'leader_id', 'project_id', 'is_main']

class ProjectAreaMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='user')

    class Meta:
        model = ProjectAreaMember
        fields = ['id', 'area', 'user', 'user_id', 'role']

class AreaLeaderSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)  # para lectura
    leader_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="leader"
    )

    class Meta:
        model = AreaLeader
        fields = ['id', 'area', 'leader', 'leader_id', 'role_name']

class ProjectAreaSerializer(serializers.ModelSerializer):
    members = ProjectAreaMemberSerializer(many=True, read_only=True)
    leaders = AreaLeaderSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectArea
        fields = ['id', 'project', 'name', 'description', 'members', 'leaders']

class ProjectSerializer(serializers.ModelSerializer):
    project_type = serializers.PrimaryKeyRelatedField(queryset=ProjectType.objects.all())
    project_state = serializers.PrimaryKeyRelatedField(queryset=ProjectState.objects.all())
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    priority = serializers.PrimaryKeyRelatedField(queryset=ProjectPriority.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'
        
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
        
# SERIALIZER PRINCIPAL: el más completo
class ProjectDetailSerializer(serializers.ModelSerializer):
    project_type = ProjectTypeSerializer()
    project_state = ProjectStateSerializer()
    priority = ProjectPrioritySerializer()
    company = CompanySerializer()
    leaders = ProjectLeaderSerializer(many=True, read_only=True)
    areas = ProjectAreaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'start_date', 'end_date',
            'project_state', 'project_type', 'priority', 'company',
            'leaders', 'areas', 
        ]