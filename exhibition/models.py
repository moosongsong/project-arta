from django.db import models
from django.contrib.auth.models import User
import os


class ExhibitionMode(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, null=False)

    def get_absolute_url(self):
        return f'/exhibition/mode/{self.slug}/'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True, null=False)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def get_absolute_url(self):
        return f'/exhibition/category/{self.slug}/'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Material(models.Model):
    name = models.CharField(max_length=50, null=False)
    image = models.ImageField(upload_to='material_images/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/piece/material/{self.slug}/'


class Exhibition(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    explain = models.TextField(null=False, blank=False)
    poster = models.ImageField(upload_to='exhibition/%Y/%m/%d/', blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(null=True, blank=True)
    click_count = models.IntegerField(default=0)

    mode = models.ForeignKey(ExhibitionMode, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return f'[{self.pk}]{self.name}'

    def get_absolute_url(self):
        return f'/exhibition/{self.pk}/'


class ExternalExhibition(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, null=False, blank=False)
    location_address = models.CharField(max_length=1000, null=True, blank=True)
    location_x = models.FloatField(null=False, blank=True, default=0.0)
    location_y = models.FloatField(null=False, blank=True, default=0.0)
    web_url = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'out : {self.exhibition.name}'

    def get_absolute_url(self):
        return f'/exhibition/{self.pk}/'


class Piece(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    explain = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='piece/%Y/%m/%d/', null=False, blank=False)
    size = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True, null=False)
    make_at = models.DateField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True, default=0)
    click_count = models.IntegerField(null=True, blank=True, default=0)

    material = models.ForeignKey(Material, null=True, on_delete=models.SET_NULL, blank=True)
    exhibition = models.ForeignKey(Exhibition, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/exhibition/piece/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.image.name)


class GuestBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True, null=False)

    def get_absolute_url(self):
        return f'/exhibition/{self.exhibition.pk}/'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True, null=False)

    def get_absolute_url(self):
        return f'/exhibition/piece/{self.piece.pk}/'


class InitialLike(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class ExhibitionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return f'/exhibition/{self.exhibition.pk}/'


class PieceLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return f'/exhibition/piece/{self.piece.pk}/'


class ExhibitionClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True, blank=True)


class PieceClick(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True)


class ExhibitionShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    exhibition = models.ForeignKey(Exhibition, on_delete=models.SET_NULL, null=True, blank=True)


class PieceShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True)
