from django.db import models

from user.models import User

class BaseAbstractModel(models.Model):
    
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BlogPost(BaseAbstractModel):
    
    title = models.CharField("title", max_length=250)
    content = models.TextField("content")
    user = models.ForeignKey(User, verbose_name="Users", on_delete=models.DO_NOTHING)
    likes = models.ManyToManyField(User, verbose_name=("Likes"), related_name='liked_posts', through='Like')
    
    @property
    def excerpt(self):
        return self.content[:200]

    class Meta:
        db_table = "blog_posts"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return f'title: {self.title}, user: {self.user.email}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog_post_likes'
        constraints = [
            models.UniqueConstraint(fields=['post', 'user'], name='unique_post_user')
        ]

    def __str__(self) -> str:
        return self.post.__str__()