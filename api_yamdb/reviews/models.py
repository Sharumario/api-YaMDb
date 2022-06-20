from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Titles(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    description = models.TextField(null=True)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ManyToManyField(
        Genres, through='GenreTitle'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genres, null=True, on_delete=models.SET_NULL
    )
    title = models.ForeignKey(
        Titles, null=True, on_delete=models.SET_NULL
    )
