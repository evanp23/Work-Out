from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    pwd = models.CharField(max_length=20)
    date_joined = models.DateTimeField("date joined")

    class Meta:
        ordering=['username']
    
    def jsonToUser(user, json):
        user.username = json['username']
        user.first_name = json['firstName']
        user.last_name = json['lastName']
        user.email = json['email']
        user.pwd = json['pwd']

        return user