# Setting up a project

## Installing Django

Start by installing django. Run:

```pipenv install django```

This also sets up your virtual environment.

## Starting a new project

To start a new django project, run the following inside your virtual environment:

```django-admin startproject [project name]```

You should now have a folder with the name of your project containing another folder with the same name alongside a file `manage.py`. The nested folder with your project name should contain the following:

* \_\_init__.py
* settings.py
* urls.py
* wsgi.py

`manage.py` contains various management functions used in setting up Django. You should NEVER have to edit this file, so don't.

If you use one of these: `python manage.py runserver`, you can verify that the Django installation is correctly installed. Navigate to `127.0.0.1:8000` and you should see Django splashscreen with a rocket flying

## Creating an app

At this point you want to start a new "app." This is how django manages the different parts of your site. Run:

```python manage.py startapp [name of app]```

 This will create a folder with the name of the app inside your main project directory, which in turn contains a directory called migrations. This should contain:

 * \_\_init__.py
 * admin.py
 * apps.py
 * models.py
 * tests.py
 * views.py

 Add your app to the `settings.py` file. Under INSTALLED_APPS add the name of your app as a string `[appname.apps.AppnameConfig]`('greeter.apps.GreeterConfig'). Don't forget to add a comma at the end!

## Hooking up URLs

We first need to create a `urls.py` file in greeter, this is going to act as a sort-of router for web requests.

```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

This will map the index of our greeter app to the `index()` in our `views.py`.

[EXPLAIN VIEWS]

The base URL router will need to be pointed towards the `urls.py` of our greeter app so that it can serve it. Add the following line to the `urlpatterns` array in our base `urls.py`:
`path('', include('greeter.urls')),` (You'll need to add `include` to your imports from `django.urls` for this step).

To ensure your URL mapping is working fine, try defining index in your `views.py` as the following and verifying the text is displayed when you navigate to `127.0.0.1:8000`

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the greeter index.")
```