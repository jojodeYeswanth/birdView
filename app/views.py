import os
import time

import cv2
from app.models import Bird, Images, Cage, Videos
from birdview import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators import gzip
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image
from django.core.files import File
from .forms import LoginForm, SignUpForm, AddBirdForm, AddCageForm


class index(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Bird
    context_object_name = 'bird_list'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {'segment': 'index', "bird_list": Bird.objects.filter(user=self.request.user),
                   "last_bird": Bird.objects.filter(user=self.request.user).last(),
                   "last_cage": Cage.objects.filter(user=self.request.user).last()}
        return context


@login_required(login_url="/login/")
def profile(request):
    context = {'segment': 'profile'}
    html_template = loader.get_template('user-profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def AddBird(request):
    if request.method == 'POST':
        form = AddBirdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            instance = form.save()
            return render(request, 'cage-option.html', {'bird_id': instance.bird_id})
            # return redirect('cageoption')
    else:
        form = AddBirdForm()
    return render(request, 'add-bird.html', {'form': form})


@login_required(login_url="/login/")
def AddCage(request):
    if request.method == 'POST':
        form = AddCageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save()
            return redirect('home')
    else:
        form = AddCageForm()
    return render(request, 'add-cage.html', {'form': form})


class cageoption(TemplateView):
    template_name = 'cage-option.html'


class BirdProfileView(CreateView):
    model = Bird
    context_object_name = 'bird_list'
    template_name = 'birds-profile.html'

    def get_context_data(self, **kwargs):
        context = {'segment': 'birds', "bird_list": Bird.objects.filter(user=self.request.user)}
        return context


class BirdImageView(CreateView):
    model = Bird
    context_object_name = 'image_list'
    template_name = 'image-list.html'

    def get_context_data(self, **kwargs):
        context = {'segment': 'images', "image_list": Images.objects.filter(user=self.request.user)}
        return context


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg, 'segment': 'login'})


def register_user(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created'
            success = True
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form": form, "msg": msg, "success": success, 'segment': 'register'})


def get_frame():
    camera = cv2.VideoCapture(0)
    while True:
        _, img = camera.read()
        imgencode = cv2.imencode('.jpg', img)[1]
        stringData = imgencode.tostring()
        yield b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n'
    del (camera)


def indexscreen(request):
    try:
        template = "detect-video.html"
        return render(request, template, {'segment': 'live'})
    except HttpResponseServerError:
        print("error")


@gzip.gzip_page
def dynamic_stream(request, stream_path="video"):
    try:
        return StreamingHttpResponse(get_frame(), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return "error"


def image_capture(request):
    camera = cv2.VideoCapture(0)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    path = 'C:/pyenv/birdview-master/media/captured'
    _, img = camera.read()
    img_name = "{}_{}.jpeg".format(request.user, timestr)
    cv2.imwrite(os.path.join(path, img_name), img)
    completepath = 'C:/pyenv/birdview-master/media/captured/' + img_name

    image = Images()
    image.title = request.user.username + "_" + timestr
    image.document.save(request.user.username + "_" + timestr + ".jpeg", File(open(completepath, 'rb')))
    image.user = request.user
    image.save()

    del (camera)
    return render(request, 'detect-video.html', {'segment': 'live'})


@login_required(login_url="/login/")
def video_capture(request):
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    timestr = time.strftime("%Y%m%d_%H%M%S")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    print("capturing")
    out = cv2.VideoWriter(request.user.username + "_" + timestr + '.avi', fourcc, 20.0, size)
    while True:
        _, frame = cap.read()
        out.write(frame)
        if time.time() > (time.time() + 14):
            break

    cap.release()
    out.release()

    video = Videos()
    # video.video_file.save(request.user.username + "_" + timestr + '.avi', File(open(completepath, 'rb')))

    video.video_file.file = out
    video.video_file.name = request.user.username + "_" + timestr + '.avi'
    video.user = request.user
    video.title = request.user.username + "_" + timestr
    video.save()

    del cap
    return render(request, 'detect-video.html', {'segment': 'video'})
