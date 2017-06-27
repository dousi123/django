# -*- coding: utf-8 -*-

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from datetime import datetime
from .models import Article, Edu, Work, User

import pdb


# 首页
def index(request):
    username = request.session.get('username', 'visitor')
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    template = loader.get_template('blog/index.html')
    context = {
        'latest_article_list': latest_article_list,
        'user': username
    }
    return HttpResponse(template.render(context, request))


# 添加简历的表单
class ArticleFormForAddArticle(forms.Form):
    name = forms.CharField(max_length=200)
    age = forms.CharField(max_length=200)
    birth = forms.CharField(max_length=200)
    certificate = forms.CharField(max_length=200)
    certificate_id = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)


# 添加简历
def addArticle(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('/login') 
    if request.method == 'POST':
        form = ArticleFormForAddArticle(request.POST)
        if form.is_valid():
            articleSQL = Article()
            articleSQL.name = form.cleaned_data['name']
            articleSQL.age = form.cleaned_data['age']
            articleSQL.birth = form.cleaned_data['birth']
            articleSQL.certificate = form.cleaned_data['certificate']
            articleSQL.certificate_id = form.cleaned_data['certificate_id']
            articleSQL.phone = form.cleaned_data['phone']
            articleSQL.email = form.cleaned_data['email']
            articleSQL.pub_date = datetime.now()
            articleSQL.save()
            return HttpResponseRedirect('/blog')
        else:
            return render(request, 'blog/addArticle.html', {'uf':form})
    else:
        form = ArticleFormForAddArticle()
    return render(request, 'blog/addArticle.html', {'uf':form})


# 教育相关的表单
class EduForm(forms.Form):
    school = forms.CharField(max_length=200)
    infos = forms.CharField(max_length=200)


# 工作相关的表单
class WorkForm(forms.Form):
    time = forms.CharField(max_length=200)
    company = forms.CharField(max_length=200)
    infos = forms.CharField(max_length=200)


# 简历详细内容及教育、工作/添加教育、工作的表单
def showArticle(request, article_id):
    article = Article.objects.get(id=article_id)
    edu_all = Edu.objects.filter(article=article)
    if request.method == 'POST':
        form = EduForm(request.POST)
        if not request.session.get('username'):
            return HttpResponseRedirect('/login')
        if form.is_valid():
            eduSQL = Edu()
            eduSQL.article = article
            eduSQL.school = form.cleaned_data['school']
            eduSQL.infos = form.cleaned_data['infos']
            eduSQL.save()
    else:
        form = EduForm()
    return render(request, 'blog/showArticle.html', {'uf':form, 'article':article, 'edu_all':edu_all})


# 删除简历
def delArticle(request, article_id):
    Article.objects.get(id=article_id).delete()
    return HttpResponseRedirect('/blog')

# 删除教育经历
def delEdu(request, edu_id):
    Edu.objects.get(id=edu_id).delete()
    return HttpResponseRedirect('/blog')

# 登陆相关的表单
class UserForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)


class UserFormForRegister(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    passwordAgain = forms.CharField(max_length=200)   


class UserFormForChange(forms.Form):
    password = forms.CharField(max_length=200)
    newPassword = forms.CharField(max_length=200)
    newPasswordAgain = forms.CharField(max_length=200)   


# 登陆
def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']           
            try:
                userSQL = User.objects.get(username=username, password=password) 
            except User.DoesNotExist:
                error = '用户名或密码错误'
                return render(request, 'blog/login.html', {'error':error}) 
            else:
                request.session['username'] = username
                return HttpResponseRedirect('/blog')
        else:
            return render(request, 'blog/login.html', {'uf':form})
    else:
        uf = UserForm()
    return render(request, 'blog/login.html', {'uf':uf})


# 注册
def register(request):
    if request.method == 'POST':
        form = UserFormForRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            passwordAgain = form.cleaned_data['passwordAgain']
            if password == passwordAgain:
                userSQL = User()
                userSQL.username = username
                userSQL.password = password
                userSQL.save()
                request.session['username'] = username
                return HttpResponseRedirect('/blog')
            else:
                error = '两次密码输入不相同'
                return render(request, 'blog/register.html', {'error':error})
        else:
            return render(request, 'blog/register.html', {'uf':form})
    else:
        uf = UserFormForRegister()
    return render(request,'blog/register.html', {'uf':uf})


# 修改密码
def changePassword(request):
    username = request.session.get('username', 'visitor')
    if(username == 'visitor'):
        return HttpResponse('not logged on')
    if request.method == 'POST':
        form = UserFormForChange(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            newPassword = form.cleaned_data['newPassword']
            newPasswordAgain = form.cleaned_data['newPasswordAgain']
            try:
                userSQL = User.objects.get(username=username, password=password)
            except User.DoesNotExist:
                error = '密码错误'
                return render(request, 'blog/changePassword.html', {'error':error})
            else:
                if newPassword == newPasswordAgain:
                    userSQL.password = newPassword
                    userSQL.save()
                    ok = '修改密码成功'
                    return render(request, 'blog/changePassword.html', {'ok':ok})
                else:
                    error = '两次密码输入不相同'
                    return render(request, 'blog/changePassword.html', {'error':error})
        else:
            return render(request, 'blog/changePassword.html', {'uf':form})
    else:
        uf = UserFormForChange()
    return render(request,'blog/changePassword.html', {'username':username, 'uf':uf})


# 登出
def logout(request):
    if request.session.get('username'):
        del request.session['username']
    return HttpResponse('logout ok!')