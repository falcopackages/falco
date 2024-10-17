from django.db import models
from django.utils.text import slugify

from falco.models import TimeStamped


class Book(TimeStamped):
    lookup_field = "slug"

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    published_at = models.DateField()
    on_going = models.BooleanField(default=True)
    cover_art = models.FileField(upload_to="covers", blank=True)
    author = models.ForeignKey("books.Author", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Author(TimeStamped):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
