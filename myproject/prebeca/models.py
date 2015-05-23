from django.db import models

# Create your models here.


class Event(models.Model):
    id_madrid = models.IntegerField()
    title = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    price = models.FloatField()
    price_descrip = models.CharField(max_length=32)
    date = models.DateTimeField()
    duration = models.FloatField()
    longdur = models.BooleanField()
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=164)


class User(models.Model):
    name = models.CharField(max_length=32)
    page = models.CharField(max_length=32)
    description = models.CharField(max_length=150, default="Sin descripcion")
    letter_size = models.CharField(max_length=32, default="11pt")
    letter_color = models.CharField(max_length=32, default="FFF")
    back_color = models.CharField(max_length=32, default="000")
    back_image = models.CharField(max_length=32, default="madrid4.png")
    title = models.CharField(max_length=32, default="'Roboto', sans-serif")
    title_color = models.CharField(max_length=32, default="FFF")


class Image(models.Model):
    imagen = models.ImageField(upload_to='templated-linear/documents')
    user = models.ForeignKey(User)


class User_Event(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    date = models.DateTimeField()


class Date_Act(models.Model):
    date = models.DateTimeField()


class Score(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    score = models.IntegerField()
    date = models.DateTimeField()


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    comment = models.TextField()
    date = models.DateTimeField()
