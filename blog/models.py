from __future__ import unicode_literals

from django.db import models

class Article(models.Model):
    name = models.CharField(max_length=200)
    photo=models.ImageField(upload_to='photos',default='user1.jpg')
    age = models.CharField(max_length=200)
    birth = models.CharField(max_length=200)
    certificate = models.CharField(max_length=200)
    certificate_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Edu(models.Model):
    article = models.ForeignKey(Article)
    school = models.CharField(max_length=200)
    infos = models.CharField(max_length=200)


class Work(models.Model):
    article = models.ForeignKey(Article)
    time = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    infos = models.CharField(max_length=200)


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)