from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
#from django.urls import reverse_lazy

class LatestPostsFeed(Feed):
    title = 'My blog'
   # link = reverse_lazy('blog:post-list')
    link = '/blog/'

    description = 'New posts of my blog.'
    def items(self):
        return Post.objects.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return truncatewords(item.content, 30)
    
    def item_link ( self, item ) :
        return  "/blog/" + str ( item.id ) + "/"

