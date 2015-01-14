__author__ = 'zdvitas'
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from lab2.models import *
from lab2.json_response import *
import os
import httplib
import urllib
import datetime


def test_client_id(cl_id, secret=None):
    if secret is None:
        client_id = OAuthApplications.objects.all().filter(id=cl_id)
    else:
        client_id = OAuthApplications.objects.all().filter(id=cl_id, secret_id=secret)
    if len(client_id) == 1:
        return True
    else:
        return False


def test_code(cl_id, secret, code, uri):
    if test_client_id(cl_id, secret):
        obj = OAuthCode.objects.all().filter(url=uri, code=code)
        if len(obj) == 1:
            user = obj[0].user
            obj.delete()
            return user
        return None


def make_code(client_id, url, user):
    code = os.urandom(16).encode('hex')
    obj = OAuthCode.objects.all().filter(client_id=client_id)
    if len(obj) == 1:
        obj.delete()
    obj = OAuthCode(client_id=client_id, code=code, url=url, user=user)
    obj.save()
    return code


def check_login(post):
    user = Person.objects.all().filter(login=post["login"], password=post["password"])
    if len(user) == 0:
        return None
    return user[0]


def auth(request):

    if not ('client_id' in request.GET and "redirect_url" in request.GET and "state" in request.GET):
        return HttpResponse(make_json_error("Missing parameters"))

    redirect_url = request.GET["redirect_url"]
    client_id = request.GET["client_id"]
    state = request.GET["state"]

    if not test_client_id(client_id):
        return HttpResponse(make_json_error("Invalid client_id"))

    if request.method == "POST":
        user = check_login(request.POST)
        if user is not None:

            code = make_code(client_id, redirect_url, user)
            params = urllib.urlencode({'client_id': client_id, 'code': code, 'state': state})
            return redirect(redirect_url + "?" + params)

    return render(request, "main.html")


def make_access_token(client_id, user):
    token = os.urandom(16).encode('hex')
    expired = datetime.datetime.now() + datetime.timedelta(1)
    refresh_token = os.urandom(5).encode('hex')

    tok = OAuthTokens.objects.all().filter(client=client_id)
    for i in tok:
        i.delete()

    tok = OAuthTokens(client=client_id, token=token, expired=expired, user=user, refresh_token=refresh_token)
    tok.save()
    return tok


@csrf_exempt
def access_token(request):
    if request.method != "POST":
        return HttpResponse(make_json_error("Invalid HTTP method! Need POST!"))

    if not ('client_id' in request.GET and "redirect_url" in request.GET and 'client_secret' in request.GET
            and 'code' in request.GET):
        return HttpResponse(make_json_error("Missing parameters"))

    redirect_url = request.GET["redirect_url"]
    client_id = request.GET["client_id"]
    code = request.GET["code"]
    secret = request.GET["client_secret"]

    user = test_code(client_id, secret, code, redirect_url)
    client_id = OAuthApplications.objects.all().filter(id=client_id)[0]
    if user is None:
        return HttpResponse(make_json_error("Invalid query!"))

    token = make_access_token(client_id, user)
    return HttpResponse(str(token))


def test_refresh(client_id, secret, refresh):
    app = OAuthApplications.objects.all().filter(secret_id=secret, id=client_id)
    if len(app) == 0:
        return None
    tok = OAuthTokens.objects.all().filter(client=client_id, refresh_token=refresh)
    if len(tok) == 0:
        return None
    return tok[0].user


@csrf_exempt
def refresh_token(request):
    if request.method != "POST":
        return HttpResponse(make_json_error("Invalid HTTP method! Need POST!"))

    if not ('client_id' in request.GET and "redirect_url" in request.GET and 'client_secret' in request.GET
            and 'refresh_token' in request.GET):
        return HttpResponse(make_json_error("Missing parameters"))

    redirect_url = request.GET["redirect_url"]
    client_id = request.GET["client_id"]
    code = request.GET["refresh_token"]
    secret = request.GET["client_secret"]

    user = test_refresh(client_id, secret, code)
    client_id = OAuthApplications.objects.all().filter(id=client_id)[0]

    if user is None:
        return HttpResponse(make_json_error("Invalid query!"))

    token = make_access_token(client_id, user)
    return HttpResponse(str(token))