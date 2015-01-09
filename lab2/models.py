# -*- coding: utf-8 -*-
# coding: utf-8
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class OAuthApplications(models.Model):
    name = models.CharField(max_length=50)
    secret_id = models.CharField(max_length=10)
    client_id = models.CharField(max_length=10)


class OAuthTokens(models.Model):
    user = models.ForeignKey(Person)
    token = models.CharField(max_length=20)
    expired = models.DateTimeField()

class OAuthCode(models.Model):
    code = models.CharField(max_length=20)
    url = models.CharField(max_length=255)
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
        return self.name + "||" + self.owner.name + "||" + str(self.year)



