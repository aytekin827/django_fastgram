import os
from pyexpat import model
import uuid

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')

    def __str__(self):
        return  self.text + 'created by_' + self.user.username

    class Meta:
        ordering = ['created_at']

def image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class Image(BaseModel):
    UPLOAD_PATH = 'user-upload'

    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)
    order = models.SmallIntegerField() #image numbering

    class Meta:
        unique_together = ['content','order']
        ordering = ['order']
        # ordering = ['-order'] 이렇게 -를 주면 내림차순이 된다.

    
class FollowRelation(BaseModel):
    follower = models.OneToOneField(User, related_name='follower', on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='followee')

    def __str__(self):
        return self.follower.username