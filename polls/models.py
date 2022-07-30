import uuid

from django.contrib.auth.models import User
from django.db import models


class Polls(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=255,help_text='Required')
    slug = models.CharField(max_length=255,help_text='Required',blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    class Meta:
        verbose_name= 'Poll'
        verbose_name_plural = 'Polls'
    
    def __str__(self):
        return self.title
    
class Option(models.Model):
    option = models.CharField(max_length=250,help_text='Required',null=True,blank=True)
    option_count = models.IntegerField(default=0,blank=True,null=True)
    polls = models.ForeignKey(Polls,on_delete= models.CASCADE,related_name='options_set')

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'
    
    def __str__(self):
        return self.option

class Vote(models.Model):
    poll = models.ForeignKey(Polls,on_delete=models.CASCADE,blank=True,null=True,related_name='postid')
    user = models.ManyToManyField(User,related_name='userid',default=None,blank=True)
    option = models.ForeignKey(Option,on_delete=models.CASCADE,default=None,blank=True,null=True,related_name='options_vote')

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.option.option[:15]} - { self.user.username }'