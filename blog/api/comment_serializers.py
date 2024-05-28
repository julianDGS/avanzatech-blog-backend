from rest_framework import serializers
from blog.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'comment': instance.comment,
            'created_at': instance.created_at,
            'post': {'id': instance.post.id, 'title': instance.post.title},
            'user': {'id': instance.user.id, 'nickname': instance.user.nickname, 'email': instance.user.email},
        }