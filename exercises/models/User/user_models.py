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
        user.username = json['username'] if "username" in json else user.username
        user.first_name = json['firstName'] if "firstName" in json else user.firstName
        user.last_name = json['lastName'] if "lastName" in json else user.lastName
        user.email = json['email'] if "email" in json else user.email
        user.pwd = json['pwd'] if "pwd" in json else user.pwd

        return user