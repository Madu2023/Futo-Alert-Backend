from django.db import models
import uuid
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from users.models import User
from comments.models import Comment


class ReplyManager(models.Manager):
    """
    A Method to get a single post by id
    """
    def get_object_by_id(self, id):
        try:
            instance = self.get(id=id)
            return instance
        except(ObjectDoesNotExist, ValueError, TypeError):
            raise ValidationError("Reply Object Does Not Exist")



class Replies(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, blank=False, editable=False, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    polarity = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.author.name
    
    
    objects = ReplyManager()
    
    