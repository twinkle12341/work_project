from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from app01.models import UserInfo


def login(request):
    data = UserInfo.objects.all()
    return render(request, "login.html", {'data': data})

def add_user(request):
    if request.method == "GET":
        return render(request, "add_user.html")
    name = request.POST.get("name")
    password = request.POST.get("password")
    age = int(request.POST.get("age"))
    UserInfo.objects.create(name=name, password=password, age=age)
    return redirect("/login/")


def delete_user(request):
    number = request.GET.get('id')
    UserInfo.objects.filter(id=number).delete()
    return redirect("/login/")


def alter_user(request):
    if request.method == 'GET':
        data = UserInfo.objects.filter(id=request.GET.get('id')).first()
        return render(request, 'alter_user.html', {'data': data})
    else:
        number = request.GET.get('id')
        name = request.POST.get("name")
        password = request.POST.get("password")
        age = int(request.POST.get("age"))
        UserInfo.objects.filter(id=number).update(name=name, password=password, age=age)
        print(number)
        return redirect("/login/")





