from django.shortcuts import render
from django.db.models import Q
from blog.models import Post

def searchposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)
            posts = Post.objects.filter(lookups).distinct()

            context = {
                'posts':posts,
                'submitbutton':submitbutton
            }
            return render(request, 'search/search.html',context)
        else:
            return render(request, 'search/search.html')
    else:
        return render(request,'search/search.html')