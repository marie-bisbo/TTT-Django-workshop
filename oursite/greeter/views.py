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
