from django.db import models


class SearchTermModel(models.Model):
    search_term = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.search_term}"
