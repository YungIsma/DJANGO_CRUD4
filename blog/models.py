from django.conf import settings
from django.db import models
from django.utils import timezone
from wagtail import models as wagtail_models
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index



# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")  # Поле для загрузки изображений
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class HomePage(wagtail_models.Page):
    intro = RichTextField(blank=True)

    content_panels = wagtail_models.Page.content_panels + [
        FieldPanel('intro')
    ]

class BlockPage(wagtail_models.Page):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    text = RichTextField(blank=True)

    search_fields = wagtail_models.Page.search_fields +[
        index.SearchField('intro'),
        index.SearchField('text'),
    ]

    content_panels = wagtail_models.Page.content_panels +[
        FieldPanel('author'),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('text'),
    ]