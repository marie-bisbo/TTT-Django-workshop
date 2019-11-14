from rest_framework import viewsets
from .greeter import joke


class SubmitViewSet(viewsets.ViewSet):
    def create(self, request):
        return joke(request.data["searchTerm"])
