from django.conf import settings
import json
from django.shortcuts import redirect
from .models import URL
from .forms import URLForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
from urllib import request as urllibreq
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
import datetime
import json
import boto3
from memento_client import MementoClient
from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from lab1.serializers import URLSerializer

api_key = "ak-5x2p3-1d2h3-rw01p-ww4nh-q49f3"

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/lab3/accounts/login/')
def url_list(request):
    #urls = URL.objects.all()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try: 
                response = requests.get(post)
                temp = BeautifulSoup(response.content,"lxml")
                if temp.title is not None:
                    post.title = temp.title.string
                else: 
                    post.tile = "None"
                post.statusCode = response.status_code
                post.finalDestination = response.url
                dt = datetime.datetime.now()
                mc = MementoClient()
                #uri = post.finalDestination
                memento_uri = mc.get_memento_info(response.url, dt).get("mementos").get("closest")
                post.wayback = memento_uri.get('uri')[0]
                if memento_uri.get("datetime") is not None:
                    post.wayback_date = str(memento_uri.get("datetime"))
                else:
                    post.wayback_date = str(dt)
                s3 = boto3.resource("s3")
                data = json.dumps({"url":response.url, "renderType":"jpeg"}).encode("utf-8")
                headers = {"content-type": "application/json"}
                api_url = "http://PhantomJScloud.com/api/browser/v2/" + api_key + "/"
                req = urllibreq.Request(url=api_url, data=data, headers=headers)
                res = urllibreq.urlopen(req)
                result = res.read()
                s3.Bucket("rachel-lab3").put_object(Key=str(post.wayback_date) + ".jpg", Body=result, ACL="public-read", ContentType="image/jpeg")
                pictureUrl = "https://s3.amazonaws.com/rachel-lab3/" + str(post.wayback_date) + ".jpg"
                post.archive = pictureUrl
            except Exception as e:
                post.statusCode = "404"
                post.finalDestination = "Does not exit"
                post.title = "No title"
                post.wayback = "None"
                post.wayback_date = "None"
                post.archive = "No"
            finally:
                post.save()
                return redirect('url_detail', pk=post.pk)
    else:
        urls = URL.objects.all()
        form = URLForm
    return render(request, 'lab1/url_list.html',{'urls':urls,'form':URLForm})

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/lab3/accounts/login/')
def url_detail(request, pk):
    url = get_object_or_404(URL, pk=pk)
    return render(request, 'lab1/url_detail.html', {'url': url})

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url='/lab3/accounts/login/')
def url_delete(request, pk):
    url = get_object_or_404(URL,pk=pk)
    key = url.archive
    s3 = boto3.client("s3")
    exists = False
    try:
        s3_.get_object(Bucket="rachel-lab3", Key=key)
    except:
        exists = False
    finally:
        if exists is not False:
            exists = True
    # If the img exists within the bucket, delete it from S3
    if exists is True:
        s3.delete_object(Bucket="rachel-lab3", Key=key)
    url.delete() 
    return HttpResponseRedirect('../')


def logout_view(request):
    logout(request)
    return redirect('login') 

@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url="/lab3/accounts/login/")
@api_view(["GET", "DELETE"])
def detail_url_api(request, pk, format=None):
    try:
        url = URL.objects.get(pk = pk)
    except URL.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = URLSerializer(url, many = True)
        return Response(serializer.data)
    elif request.method == "DELETE":
        url.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)


@ratelimit(key="ip", rate="10/m", block=True)
@login_required(login_url="/lab3/accounts/login/")
@api_view(["GET", "POST"])
def url_api(request, format=None):
    if request.method == "GET":
        urls = URL.objects.all()
        serializer = URLSerializer(urls, many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = URLSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)



