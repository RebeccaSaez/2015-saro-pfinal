from django.contrib import admin
from models import User, Event, User_Event, Date_Act, Score, Comment, Image

# Register your models here.

admin.site.register(User)
admin.site.register(Event)
admin.site.register(User_Event)
admin.site.register(Date_Act)
admin.site.register(Score)
admin.site.register(Comment)
admin.site.register(Image)
