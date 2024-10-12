from django.db import models

from falco.models import TimeStamped


class Book(TimeStamped):
    lookup_field = "slug"
    path_converter = "str"

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    published_at = models.DateField()
    cover_art = models.FileField(upload_to="covers")
    author = models.ForeignKey("books.Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Author(TimeStamped):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
