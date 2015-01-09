__author__ = 'zdvitas'

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


def test_client_id():

    return True


def make_code():
    return


def auth(request):

    client_id = ""
    if not ('client_id' in request.GET and "redirect_url" in request.GET):
        return HttpResponse("Missing parameters")


    redirect_url = request.GET["redirect_url"]
    client_id = request.GET["client_id"]
    url = ''
    return redirect(redirect_url)