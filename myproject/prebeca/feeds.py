from django.contrib.syndication.views import Feed
from models import Event, User_Event, User
import datetime


class UserFeed(Feed):
    title = "Eventos del usuario"
    description = "Eventos seleccionados"
    link = "/rebeca"
    pubDate = datetime.datetime.now()

    def get_object(self, request, user):
        self.us = User.objects.get(name=user)

    def items(self):
        return User_Event.objects.filter(user=self.us).order_by('date')

    def item_title(self, item):
        return item.event.title

    def item_link(self, item):
        return item.event.url

    def item_description(self, item):
        return item.event.description

    def item_category(self, item):
        return item.event.type

    def item_guid(self, item):
        return str(item.event.id_madrid)

    def item_date(self, item):
        return item.event.date

    def item_pubdate(self, item):
        return item.date


class AllFeed(Feed):
    title = "Eventos Madrid"
    description = "Todos los eventos de la Comunidad de Madrid"
    link = "/css"
    pubDate = datetime.datetime.now()

    def items(self):
        return Event.objects.order_by('date')

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.url

    def item_description(self, item):
        return item.description

    def item_category(self, item):
        return item.type

    def item_guid(self, item):
        return str(item.id_madrid)

    def item_date(self, item):
        return item.date
