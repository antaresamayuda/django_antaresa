from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reference_posts')
    description = models.TextField()
    link = models.URLField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('reference:post_detail', kwargs={ 'pk': self.id, 'slug': self.slug })

