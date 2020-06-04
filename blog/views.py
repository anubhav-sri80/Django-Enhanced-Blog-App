from django.shortcuts import render,get_object_or_404 #we can return template insted of httpResponse
from .models import Post
from .forms import  CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.views.generic import ListView,DetailView, CreateView,UpdateView,DeleteView
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

  
def PostListView(request,tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    #context ={
     #   'posts':Post.objects.all(),
      #  'tag': tag,
       # 'page':page
    #}

     
    return render(request,'blog/home.html',{'page': page,
                                            'posts': posts,
                                            'tag': tag})

#class PostListView(ListView):
 #   model= Post
  #  template_name ='blog/home.html'
   # context_object_name='posts'
    #ordering = ['-date_posted']
    #paginate_by = 3

    

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

#class PostDetailView(DetailView):
 #   model = Post
    #---
def post_detail(request,post_id):

    post = get_object_or_404(Post ,id=post_id, )


    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST,)
        if comment_form.is_valid():
        # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
           # new_comment.name=request.user
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return render(request,
        'blog/post_detail.html',{'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form},)
    else:
        comment_form = CommentForm(instance=request.user)

        # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags','-date_posted')[:4]
        
        
        return render(request,
        'blog/post_detail.html',
        {'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts}
        )


class PostCreateView(LoginRequiredMixin,CreateView):
    model= Post
    fields=['title','content']
    success_url='/'
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post =self.get_object()
        if self.request.user == post.author:
            return True
        return False    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model= Post
    success_url='/'
    
    def test_func(self):  #current post is author of same logged in user
        post =self.get_object()
        if self.request.user == post.author:
            return True
        return False  


def about(request):
    return render(request,'blog/about.html',{'title':'About'})