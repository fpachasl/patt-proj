from rest_framework import serializers

from apps.users.serializers import UserSerializer
from .models import Comment, CommentAttachment



class CommentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentAttachment
        fields = ['id', 'file', 'uploaded_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='comment_user', read_only=True)
    attachments = CommentAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_date', 'user', 'task', 'attachments']