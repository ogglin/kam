# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import subprocess

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from app import models


def shell_cmd(cmd, param):
    if '-L' in param:
        proc = subprocess.check_output([cmd, param])
    else:
        print('[cmd, param]')
        subprocess.call([cmd, param])
        proc = subprocess.check_output(['iptables', '-L'])
    # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # o, e = proc.communicate()
    # s = str(proc.returncode)
    return proc


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def profile(request, uid):
    user = models.User.objects.filter(id=uid)
    context = {"user": user[0], }
    try:

        html_template = loader.get_template('profile.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def rule(request, v):
    err = ''
    if v == 'list':
        proc = shell_cmd('iptables', '-L').decode().split('\n')
        context = {"variant": v, "shell": proc, }
    elif v == 'add':
        if request.GET['ip']:
            ip = request.GET['ip']
            if request.GET['time']:
                time = request.GET['time']
            else:
                time = 3
            shell_cmd('iptables', '-I FORWARD -s ' + ip + ' -j ACCEPT')
        else:
            err = "Не указан IP"
        proc = shell_cmd('iptables', '-L').decode().split('\n')
        context = {"variant": v, "shell": proc, "error": err}
    elif v == 'delete':
        if request.GET['ip']:
            ip = request.GET['ip']
            shell_cmd('iptables', '-D FORWARD -s ' + ip + ' -j ACCEPT')
        else:
            err = "Не указан IP"
        proc = shell_cmd('iptables', '-L').decode().split('\n')
        context = {"variant": v, "shell": proc, "error": err}
    else:
        context = {"variant": v, }
    try:
        html_template = loader.get_template('rules.html')
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
