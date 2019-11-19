# The Power of Django

## Why do we need something like Django?

There are currently a plethora of web development frameworks out there to choose from. Generally, you would choose to use one of them to standardise the process, as
well as make use of the inbuilt features that (hopefully at least) make certain things faster to do and easier to manage. This is why you'll find that starting a project
with a web development framework sets you up with an initial load of stuff. This includes libraries and templates for interactin with different aspects of your website.  

## Why Django? 

Django is a really popular web development framework, for a number of reasons. The first thing to note is that it's built on python. It also comes with a lot of the aforementioned stuff.
 The main aim of django is to be fast and simple, as well as secure. It is also well maintained, so you can generally expect it to be running smoothly. 
Django has been used to build quite a few big websites, including Instagram, Spotify and NASA. 

Keep in mind that Django mostly handles backend functionality of web applications. That is, the databases that store information, the logic and generally how things work. On the 
other side is frontend development, the side that a user sees and which dictates how things look. Whilst you can create a front end with just Django, it is more common to use a separate
tool such as Vue to handle this. 

So Django is by no means your only option when it comes to backend web development, but it's fast, simple (after a bit of a learning curve), well documented and well maintained. These
are all good reasons to consider Django if you ever plan on developing a web app.      

# Setting up a project

## Installing Django / Pre-requisites

Start by installing Django. Run:

```
pipenv install django
pipenv install djangorestframework
pipenv install requests
```

Alternatively, run:

`make install`

which will run the same commands. 

This also sets up your virtual environment, jump into it with `pipenv shell`.

## Starting a new project

To start a new django project, run the following inside your virtual environment:

```django-admin startproject [project name]```

You should now have a folder with the name of your project containing another 
folder with the same name alongside a file `manage.py`. The nested folder with your project name should contain the following:

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

We'll want to create an index.html in our newly created directory then, we'll want to take an input and have a button to submit it, the following will do fine for now:

```
<!DOCTYPE html>
<html>

<body>
    <p>Tell me a joke</p>
    <input id="searchTermInput"></input>
    <button onclick="submitJokeRequest()">Submit</button>
    <p>Here's your joke:
        <span id="joke"></span>
    </p>
</body>

</html>
```

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

We'll want to use Axios to handle our API calls from the frontend. To this end we're going to edit our index.html a bit to pull a web version of axios to use (In reality we'd probably want to `npm install axios` and import it from our node_modules, however this is a bit of a faff without a web framework in place so we're going to use a very rudimentary API implementation instead).
Update your index.html with the following `<head>` tag (importing `axios`) as well as the `<script>` tag at the bottom (Setting the behaviour of our button).

```
<!DOCTYPE html>
<html>

<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/axios/0.18.0/axios.min.js"></script>
</head>

<body>
    <p>Tell me a joke</p>
    <input id="searchTermInput"></input>
    <button onclick="submitJokeRequest()">Submit</button>
    <p>Here's your joke:
        <span id="joke"></span>
    </p>
    <script>
        axios.defaults.xsrfCookieName = 'csrftoken';
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';

        function submitJokeRequest() {
            var inputValue = document.getElementById("searchTermInput").value;
            this.axiosSubmit(inputValue).then(data => {
                document.getElementById("joke").innerHTML = data;
            });
        }

        function axiosSubmit(searchTerm) {
            const url = '/api/submit/';
            const data = {
                'searchTerm': searchTerm
            };
            return axios.post(url, data)
                .then(response => response.data)
                .catch((e) => {
                    console.log(e);
                });
        }
    </script>
</body>

</html>
```

If you reload the website and type a search term into our input field and hit enter, you should be met with a hilarious joke. To break down what's going on:

* When we hit our button, we call the method `submitJokeRequest()`
* This in turn pulls the value of our input field and passes it to `axiosSubmit()`
* `axiosSubmit()` forms a `json` from the searchTerm and posts it to `/api/submit/`, this being mapped to `SubmitViewSet` earlier by us
* `SubmitViewSet` is set to call the `joke()` method in `greeter.py` and thus calls this with the `json` that we passed to it and returns the result to `axiosSubmit()`
* `axiosSubmit()` returns this value via `response.data` to `submitJokeRequest()` which then updates our `<span>` element with the data (joke) returned.

### Storing data

As an additional point, you may be interested in saving the data your users have input into Django's database (SQLite by default). The process for this is fairly straight forwards as the following should hopefully demonstrate.

1. The first thing we'll want to do is define a model for our data, this is the format (like an object) our data will be stored into in the database, add the following class to `models.py` in our greeter app (`def __str__` determines how the data will be output in our frontend within the Django admin page, to be seen later)
:


```
class SearchTermModel(models.Model):
    search_term = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.search_term}"

```


2. Following this we'll want to define a serializer; the serializer is responsible for placing our data into a model and saving it. Add the following code in a new file named `serializers.py` within the greeter app:

```
from rest_framework import serializers
from .models import SearchTermModel

class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTermModel

    def create(self, search_term) -> SearchTermModel:
        return SearchTermModel(search_term=search_term)
```

3. Finally, we'll want to update our `views.py` so that it not only returns a call to our `joke()` method, but also uses our serializer to save our input data into a model for our database. Update our `SubmitViewSet` to the following:

```
from rest_framework import viewsets
from .greeter import joke
from .serializers import SearchTermSerializer


class SubmitViewSet(viewsets.ViewSet):
    def create(self, request):
        search_term_serializer = SearchTermSerializer()
        search_term_object = search_term_serializer.create(
            search_term=request.data["searchTerm"]
        )
        search_term_object.save()
        return joke(request.data["searchTerm"])

```

4. To register our changes, we'll need to run the following commands: `python manage.py makemigrations` followed by `python manage.py migrate` (Explanation from Marie here about migrations)

That's it! Our website is now setup to save our user's input search terms into a `SearchTermModel` facilitated by our `SearchTermSerializer`. There is one quick additional step we'll want to make if we want a frontend interface with which to view our saved data. Add the following lines into greeter app's `admin.py`:

```
from .models import SearchTermModel

admin.site.register(SearchTermModel)
```

These lines simply tell the Django's admin interface to display `SearchTermModels` on its frontend. We'll need an admin user to access this display which can be done easily with the following command: `python manage.py createsuperuser`

After navigating to `127.0.0.1/admin` and logging in with your created user, you should see an additional tab named Greeter with a 'Search term models' option within. Following that link, you should see your search terms saved from the frontend input (The way they are displayed is determined by our `__str__` method we wrote earlier!)

# Django Migrations

## What do migrations look like

What happens when you makemigrations and migrate? When you run makemigrations, you will find that django generates a file in a folder called migrations, 
that looks something like this:

```
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTermModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_term', models.CharField(max_length=500)),
            ],
        ),
    ]
 ```
 
 When you then run the migrate command, you get a notification that your migrations are being applied, hopefully followed by a green ok. 
 
 ## When do you have to think about migrations 
  
 You will have found that when you first run your project on the server with runserver, you are informed of a number of unapplied migrations. 
 You can run `pipenv run python manage.py migrate --list` to see them.  
 These arise from built in Django functionality, and you don't have to worry about them straight away. 
 Migrations appear when you create and alter what Django calls models. Models store information about data that you're storing in your django project.
  It generally works like a regular class would, and so you would generally follow the same principles in creating one. Your model should be an
   objects with certain attributes, for example you could have a Brainlabber model with a name, a job and an avatar. Models are described in detail in the 
   [django documentation](https://docs.djangoproject.com/en/2.2/topics/db/models/).   
   
 ## What are migrations
 
 Migrations are actually database migrations. To store data, django uses a database, by default sqlite3, but this can be changed if needed.
 But django recognised that working directly with the database with something like SQL would be cumbersome for most, and so they made things easier.
  The way it works is that when you create or alter a model and makemigrations, django turns this into the file we saw above, which calls on some inbuilt
  django functionality that can read your model fields and turn them into SQL, and when you then apply those migrations, it applies these changes to the database.
  Each model is a table, with each of the fields in your model as a column, and each instance of your model is then subsequently added as a row. 
  
  The process of making migrations and then migrating is analogous to adding files to the staging area and then commiting them in git. 
  
  The process of migrations can make data management a lot easier, however be aware that there are situations when you need to be careful. Read the [django documentation](https://docs.djangoproject.com/en/2.2/topics/migrations/) on migrations
  for more details.
  
  # Serializers
  
  ## What are serializers
  
  ```text
"Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or 
other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data."
```

Serializers are not built into Django, but can be imported through the Django Rest Framework, which we installed at the start. See the [documentation](https://www.django-rest-framework.org/api-guide/serializers/) for full details. 

## Why use serializers

When you create a model in django, you usually save instances of this model to a database, which you can access and interact with. However the format in which your data exists
is not necessarily the best format to work with. Serializing the data means you can convert complex datatypes such as the ones that arise in databases, into native Python datatypes that can
be rendered into something like JSON.   
  
 # Interacting with your models and database - the django interactive console
  
