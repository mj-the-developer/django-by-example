from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    total_likes = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]


    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.pk, self.slug])
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)
