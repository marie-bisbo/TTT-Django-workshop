from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("submit", views.SubmitViewSet, basename="submit_base")

urlpatterns = [
    path('', include(router.urls)),
]
