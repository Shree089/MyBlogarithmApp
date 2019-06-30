from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from blog.models import Post
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_project import settings

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



def PostDetailView(request, pk):
    post = get_object_or_404(Post, id=pk)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked= True
    context = {
        'post':post,
        'is_liked':is_liked,
        'total_likes': post.total_likes()
    }
    return render(request, 'blog/detail.html', context)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

def send_email(request):
    send_mail(
        'Welcome on Board',
        'Blogarithm welcomes you!!!',
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently = False
    )
    return render(request, 'blog/send_email.html')

def like_post(request):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())