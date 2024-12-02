from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import cv2
from post.models import Post
from django.conf import settings
from django.urls import reverse

class UserManager(BaseUserManager):
    """
    A method to create a user and get a user
    """
    def get_user_by_id(self, id):
        try:
            instance = self.get(id=id)
            return instance
        except (ObjectDoesNotExist, TypeError, ValueError):
            raise ValidationError("Object Does Not Exist")
        
    def create_user(self, username, email, phone_number, password, **kwargs):
        """
        A method to create a user
        """ 
        if username is None:
            raise ValidationError("User Must Have A Username")
        if email is None:
            raise ValidationError("User Must Have An Email")
        if phone_number is None:
            raise ValidationError("User Must Have A Phone Number")   
        if password is None:
            raise ValidationError("User Must Have A Password")
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, phone_number, password, **kwargs):
        """
        A method to create a user
        """ 
        if username is None:
            raise ValidationError("User Must Have A Username")
        if email is None:
            raise ValidationError("User Must Have An Email")
        if phone_number is None:
            raise ValidationError("User Must Have A Phone Number")   
        if password is None:
            raise ValidationError("User Must Have A Password")
        user = self.create_user(username=username, email=self.normalize_email(email), phone_number=phone_number, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
            


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True, blank=False, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=256, db_index=True, unique=True)
    first_name = models.CharField(max_length=256, db_index=True)
    last_name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField(max_length=256, db_index=True, unique=True)
    phone_number = PhoneNumberField(blank=False, unique=True)
    bio = models.TextField()
    image = models.ImageField(upload_to='users_images', blank=True)
    post_polarity = models.PositiveIntegerField(default=0)
    post_likes = models.ManyToManyField(Post, related_name='liked_by')
    post_love = models.ManyToManyField(Post, related_name='loved_by')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')
    comment_polarity = models.PositiveIntegerField(default=0)
    reply_polarity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
  
    
   
    
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name} {self.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = cv2.imread(self.image.path)
            size = (100, 100)
            image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, image)
        else:
            return None   
     
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']
    
    def like_post(self, post):
        """
        A method to like a post
        """
        return self.post_likes.add(post)
    
    def unlike_post(self, post):
        """
        A method to unlike a post
        """
        return self.post_likes.remove(post)
    
    def check_post_like(self, post):
        """
        A method to unlike a post
        """
        return self.post_likes.filter(pk=post.pk).exists()
    
    def love_post(self, post):
        """
        A method to love a post
        """
        return self.post_love.add(post)
    
    def unlove_post(self, post):
        """
        A method to unlove a post
        """
        return self.post_love.remove(post)
    
    def check_post_love(self, post):
        """
        A method to check if a user already love a post
        """
        return self.post_love.filter(pk=post.pk).exists()
    
    def user_follow(self, user):
        """
        A method to follow a user
        """
        return self.followers.add(user)
    
    def user_unfollow(self, user):
        """
        A method to unfollow a user
        """
        return self.followers.remove(user)
    
    def user_followers_count(self):
        """
        A method to count all users followers
        """
        return self.followers.count()
    
    def user_check_follow(self, user):
        """
        A method to check if a user already following a user
        """
        return self.followers.filter(pk=user.pk).exists()
    
    
    objects = UserManager()