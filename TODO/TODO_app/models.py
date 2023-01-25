from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

       # A user can have many tasks, we are using the builtin User model bcz we want to take record which user is creating a profile and adding the tasks. A user model gives the name,email and password of the user.
       user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
       title = models.CharField(max_length = 200)
       desc = models.TextField(null = True, blank = True )
       complete = models.BooleanField(default=False)
       create = models.DateTimeField(auto_now_add = True)

       def __str__(self):
              return self.title

       # When the task is completed it will move to the bottom of the list
       class Meta:
              ordering = ['complete']

