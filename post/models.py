from django.db import models
import uuid
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.conf import settings
import cv2


class PostManager(models.Manager):
    """
    A defined Method to get a post by its unique id
    """
    def get_object_by_id(self, id):
        try:
            instance = self.get(id=id)
            return instance
        except(ObjectDoesNotExist, ValueError, TypeError):
            raise ValidationError("Post Object Does Not Exist")
        




class Post(models.Model):
    id = models.UUIDField(primary_key=True, db_index=True, editable=False, default=uuid.uuid4, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True)
    active = models.BooleanField(default=True)
    polarity = models.BooleanField(default=True)
    edited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.author.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = cv2.imread(self.image.path)
            size = (300, 300)
            image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            post_image = cv2.imwrite(self.image.path, image)
            return post_image
        else:
            pass
    
    
    objects = PostManager()
    
    
    