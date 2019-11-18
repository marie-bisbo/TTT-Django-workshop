from rest_framework import serializers
from .models import SearchTermModel


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTermModel

    def create(self, search_term) -> SearchTermModel:
        return SearchTermModel(search_term=search_term)
