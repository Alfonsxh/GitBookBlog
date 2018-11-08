# Django入门篇

## 项目与应用

> `项目`是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。
> `应用`是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者简单的投票程序。

在Django中，使用`startproject`来创建项目，使用`startapp`来创建应用。

```shell
django-admin startproject mysite      # 创建项目

python manage.py startapp polls        # 创建应用
```

此时，整个项目的结构为

```shell
$ tree ./mysite/
./mysite/           # 项目文件夹
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py     # Django 项目的配置文件。
│   ├── urls.py     # Django 项目的 URL 声明
│   └── wsgi.py     # 作为项目运行在 WSGI 兼容的Web服务器上的入口
└── polls           # 应用文件夹
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 为单个应用设置urls

在Django中，每个应用也可以含有各自的`URLconf`进行url映射。

为了创建`URLconf`，需要在应用`polls`中创建一个`urls.py`文件，此时目录结构应为如下所示。

```shell
$ tree ./polls/
./polls/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

在`polls/urls.py`文件中添加如下代码：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

在`mysite/urls.py`文件的`urlpatterns`列表中插入一个`include()`，如下：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

此时，可以通过访问``