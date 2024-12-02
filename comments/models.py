from django.db import models
import uuid
from post.models import Post
from users.models import User
from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class CommentManager(models.Manager):
    """
    A Manager used in getting an object by id
    """
    def get_comment_object_by_id(self, id):
        try:
            instance = self.get(id=id)
            return instance
        except(ObjectDoesNotExist, ValueError, TypeError):
            raise ValidationError("Comment Object Does Not Exist")
        

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, db_index=True, blank=False, editable=False, default=uuid.uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    active = models.BooleanField(default=True)
    polarity = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.comment} on {self.post}"
    
    
    objects = CommentManager()
        
