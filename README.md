# Setting up a project

## Installing Django / Pre-requisites

Start by installing Django. Run:

```
pipenv install django
pipenv install djangorestframework
pipenv install requests
```

This also sets up your virtual environment, jump into it with `pipenv shell`.

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

 Add your app to the `settings.py` file. Under INSTALLED_APPS add the name of your app as a string `appname`('greeter'). Don't forget to add a comma at the end! While you're here, add in `rest_framework` too as we'll be using this later.

As well as this, create an app named 'frontend', this is where we'll be hosting the actual display of our website. The greeter app will be used to handle script logic. (Make sure to repeat the steps about adding the app to `settings.py`)

## Hooking up URLs

We first need to create a `urls.py` file in frontend, this is going to act as a sort-of router for web requests.

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

This will map the default location of our app to the `index()` in our `views.py`. Views are essentially Python functions or classes that return a web response back after use.

The base URL router will need to be pointed towards the `urls.py` of our frontend app so that it can serve it. Add the following line to the `urlpatterns` array in our base `urls.py`:
`path('', include('frontend.urls')),` (You'll need to add `include` to your imports from `django.urls` for this step).

To ensure your URL mapping is working fine, try defining index in your `views.py` as the following.


```
from django.shortcuts import render


def index(request):
    return render(request, 'frontend/index.html')
```

This code will return a file from `frontend/index.html` within the templates folder. Templates are essentially where we store our `HTML` files to be rendered, for our sake we'll want to make one within our frontend app (templates/frontend). The additional frontend is used to namespace `HTML` files within as Django will look in all available templates folders for files otherwise, leading to possible conflicts.

To ensure that Django can see your template, add the following line to the `TEMPLATES` array in `oursite/settings.py`: `os.path.join(BASE_DIR, "frontend/templates")`

We'll want to create an index.html in our newly created directory then, we'll want to take an input and have a button to submit it, the following will do fine:

```
<input></input>
<button>Submit</button>
```

Use the command `python manage.py createsuperuser` to create an admin user capable of accessing 127.0.0.1/admin (Which is a GUI we can use to view our data from)

### API

We're going to want to setup a URL where API calls will be redirected to and handled. To this end, add the following line to your `urls.py` in oursite: `path("api/", include("greeter.urls"))`. Similar to our frontend example, we're now going to want to create a `urls.py` in greeter which will tell Django what to do with any /api requests.

```
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("submit", views.SubmitViewSet, basename="submit_base")

urlpatterns = [
    path('', include(router.urls)),
]
```

Here we're telling our URLs file that it should redirect any calls to /url/submit to SubmitViewSet in `views.py`.
If we create a basic view in `greeter/views.py`, we should be able to access the API url we've defined. Paste the below into `views.py`.

```
from rest_framework import viewsets

class SubmitViewSet(viewsets.ViewSet):
    def create(self, request):
        return joke(request.data["searchTerm"])
```

We should now be able to access `127.0.0.1/api` (Which should show us a list of our API operations, in this case just 'submit') and even further `127.0.0.1/api/submit` which lets us post JSON to our application.

If we go to `127.0.0.1/api/submit` and feed it a JSON string (e.g {"searchTerm": "test"}), we should see response text shown from the application. Our API is communicating with our tool!

### Hooking up the API to the frontend

We'll want to use Axios to handle our API calls from the frontend. We're going to need to setup npm in our frontend directory (oursite/frontend) to achieve this (If you don't have node, shame on you, use `brew install node`):

* `npm init` - You can just hit enter through the requisitioned details here, they're not important for our use-case
* `npm install axios`

As a sanity check you should now have a `node_modules` folder in the frontend directory as well as a package.json + package-lock.json.
