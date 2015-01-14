from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from lab2.json_response import *
from lab2.models import *
from django.utils import timezone

__per_page__ = 10


def home(request):
    return render(request, "index.html")


def test_token(request):
    if not "HTTP_TOKEN" in request.environ:
        return None
    token = request.environ["HTTP_TOKEN"]
    tok = OAuthTokens.objects.all().filter(token=token)
    if len(tok) == 0:
        return None
    if tok[0].expired > timezone.now():
        return tok[0].user
    return "expired"


def info(request):
    info = {}
    info["Client count"] = len(Person.objects.all())
    info["PC count"] = len(Computer.objects.all())
    info["Soft count"] = len(Program.objects.all())
    return HttpResponse(make_json(info))


def user_me(request):
    user = test_token(request)
    # user = Person.objects.all()[0]
    if user is None:
        return HttpResponse(make_json_error("Token error!"))
    if user == "expired":
        return HttpResponse(make_json_error("Token expired!"))

    pcs = list(Computer.objects.all().filter(owner=user))
    for i in range(len(pcs)):
        pcs[i] = pcs[i].__dict__
        pcs[i].pop("_state", None)

    resp = {"Username": user.name, "Computers": pcs}
    return HttpResponse(make_json(resp))


def user_id(request, id):
    user = test_token(request)

    if user is None:
        return HttpResponse(make_json_error("Token error!"))

    if user == "expired":
        return HttpResponse(make_json_error("Token expired!"))

    user = Person.objects.all().filter(id=id)
    if len(user) == 0:
        return HttpResponse(make_json_error("Invalid id!"))
    user = user[0]
    pcs = list(Computer.objects.all().filter(owner=user))

    for i in range(len(pcs)):
        pcs[i] = pcs[i].__dict__
        pcs[i].pop("_state", None)
    resp = {"Username": user.name, "Computers": pcs}
    return HttpResponse(make_json(resp))


def pc_soft_list(request, id, pc_id):
    user = test_token(request)
    if user is None:
        return HttpResponse(make_json_error("Token error!"))
    if user == "expired":
        return HttpResponse(make_json_error("Token expired!"))


    user = Person.objects.all().filter(id=id)
    if len(user) == 0:
        return HttpResponse(make_json_error("Invalid id!"))
    user = user[0]
    pcs = Computer.objects.all().filter(owner=user, id=pc_id)

    if len(pcs) == 0:
        return HttpResponse(make_json_error("Invalid PC id!"))
    pagination = {}
    if "page" in request.GET:
        page = int(request.GET["page"])
        first = page * __per_page__
        second = first + __per_page__
        pagination["per_page"] = __per_page__
        pagination["total_count"] = len(pcs[0].programs.all())
        pagination["cur_page"] = page
        soft = pcs[0].programs.all()[first:second]
    else:
        soft = pcs[0].programs.all()

    pcs = pcs[0]
    soft = list(soft)

    for i in range(len(soft)):
        soft[i] = soft[i].__dict__
        try:
            soft[i].pop("_state", None)
            soft[i].pop("date_of_install")
        except:
            print ""

    pcs = pcs.__dict__
    pcs["_state"] = ""

    resp = {"Username": user.name, "Computer": pcs, "Soft": soft}
    if "page" in request.GET:
        resp["pagination"] = pagination

    return HttpResponse(make_json(resp))