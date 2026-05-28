from django.shortcuts import render, get_object_or_404
from .models import BlogGroup,Post
from django.core.paginator import Paginator
from django.db.models import F


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs_app/post_list.html', {'page_obj':page_obj})

def post_detail(request, slug):
    post = get_object_or_404(Post.published, slug=slug)
    Post.objects.filter(id=post.id).update(views=F('views') + 1)  # F افزایش تعداد بازدید به کمک
    return render(request, 'blogs_app/post_detail.html', {'post':post})

# فیلتر بر اساس دسته‌بندی
def group_posts(request, slug):
    group = get_object_or_404(BlogGroup, slug=slug, is_active=True)
    posts = group.posts.filter(is_published=True)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs_app/group_posts.html', {'group':group, 'page_obj':page_obj})
