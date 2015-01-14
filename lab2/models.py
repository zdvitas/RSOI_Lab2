# -*- coding: utf-8 -*-
# coding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
import json

@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    login = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class OAuthApplications(models.Model):
    name = models.CharField(max_length=50)
    secret_id = models.CharField(max_length=10)


class OAuthTokens(models.Model):
    client = models.ForeignKey(OAuthApplications)
    token = models.CharField(max_length=40)
    expired = models.DateTimeField()
    user = models.ForeignKey(Person)
    refresh_token = models.CharField(max_length=40)

    def __str__(self):
        return json.dumps({"access_token": self.token, "expired": 86400, "refresh_token": self.refresh_token,
                "user_id": self.user.id})
        # return "?access_token="+self.token+"&exired=86400&user_id="+str(self.user_id)+"&refresh_token=%s" % self.token


class OAuthCode(models.Model):
    code = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    client = models.ForeignKey(OAuthApplications)
    user = models.ForeignKey(Person)


@python_2_unicode_compatible
class Program(models.Model):
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=20)
    customer = models.CharField(max_length=150)
    date_of_install = models.DateTimeField()

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Computer(models.Model):
    owner = models.ForeignKey(Person)
    count = models.IntegerField()
    cabinet = models.IntegerField(blank=True)
    type = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=20, blank=True)
    mac = models.CharField(max_length=30, blank=True)
    processor = models.CharField(max_length=50, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(blank=True)
    notes = models.TextField(blank=True)
    programs = models.ManyToManyField(Program)

    def __str__(self):
        dic = self.__dict__
        # try:
        #     # dic.pop("_state", None)
        # except:
        #     i = 10

        return json.dumps(dic)




