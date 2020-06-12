from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Reference

class LatestReferencesFeed(Feed):
    title = 'My Reference'
    link = reverse_lazy('reference:reference_list')
    description = 'New references of my reference.'

    def items(self):
        return Reference.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)