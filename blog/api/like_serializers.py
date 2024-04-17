from rest_framework import serializers
from blog.models import Like

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'post': {'id': instance.post.id, 'title': instance.post.title},
            'user': {'id': instance.user.id, 'nickname': instance.user.nickname, 'email': instance.user.email}
        }