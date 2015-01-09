__author__ = 'zdvitas'

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from lab2.models import *
from lab2.json_error import *


def test_client_id(cl_id):

    client_id = OAuthApplications.objects.all().filter(client_id=cl_id)
    if len(client_id) == 1:
        return True
    else:
        return False


def make_code():
    return


def auth(request):


    if not ('client_id' in request.GET and "redirect_url" in request.GET):
        return HttpResponse(make_json_error("Missing parameters"))


    redirect_url = request.GET["redirect_url"]
    client_id = request.GET["client_id"]
    url = ''



    return render(request,"main.html")