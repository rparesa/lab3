from django.shortcuts import redirect
from .models import URL
from .forms import URLForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
import datetime
from memento_client import MementoClient


@login_required(login_url='/accounts/login/')
def url_list(request):
    urls = URL.objects.all()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try: 
                response = requests.get(post)
                temp = BeautifulSoup(response.content,"lxml")
                post.title = temp.title.string
                post.finalDestination = response.url
                post.statusCode = response.status_code
                dt = datetime.datetime.now()
                mc = MementoClient()
                uri = post.finalDestination
                memento_uri = mc.get_memento_info(uri, dt).get("mementos").get("closest")
                post.uri = memento_uri.get('uri')[0]
                post.datetime = str(memento_uri.get('datetime'))
            except:
                post.statusCode = "None"
                post.finalDestination = "Does not exit"
                post.title = "No title"
                pass
            finally:           
                post.save()
                return redirect('url_detail', pk=post.pk)
    else:
        form = URLForm
    return render(request, 'lab1/url_list.html',{'urls':urls,'form':URLForm})

@login_required(login_url='/accounts/login/')
def url_detail(request, pk):
    url = get_object_or_404(URL, pk=pk)
    return render(request, 'lab1/url_detail.html', {'url': url})

@login_required(login_url='/accounts/login/')
def url_delete(request, pk):
    url = get_object_or_404(URL,pk=pk)
    url.delete() 
    return HttpResponseRedirect('../')


def logout_view(request):
    logout(request)
    return redirect('login') 
