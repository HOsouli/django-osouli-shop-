from django.shortcuts import render,redirect,get_object_or_404
from .forms import CommentForm
from django.views import View
from apps.products.models import Product
from apps.comment_scoring_favorites.models import Comment
from django.contrib import messages
from .models import Scoring, Favorite
from django.http import HttpResponse
from django.db.models import Q

class CommentView(View):
    def get(self, request, *args, **kwargs):
        productId=request.GET.get('productId')
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        initial_dict = {
            'product_id':productId,
            'comment_id':commentId,
            'product': product
        }
        form = CommentForm(initial = initial_dict)
        return render(request, 'csf_app/partials/create_comment.html', {'form':form,'slug':slug})

    def post(self, request, *args, **kwargs):
        slug=kwargs['slug' ]
        product=get_object_or_404(Product, slug=slug)

        form=CommentForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            parent=None  # اگر اولین شخصی بود که نظر خودش رو صبت کرده پس والد نداره(یعنی جواب گامنتی رو نداده)
            if cd['comment_id']:
                parentId=cd['comment_id']
                parent=Comment.objects.get(id=parentId)  # کامنتی که مربوط به والد هست رو پیدا کردم

            # درج کامنت
            Comment.objects.create(
                product=product,  # برای این محصول
                commenting_user=request.user,  # توسط این کاربر
                comment_text=cd['comment_text'],  # متنش
                comment_parent=parent  # والدش هم نال هست (اولین نظر دهنده)
            )
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('products:product_details', slug=slug)

        messages.error(request, 'خطا در ارسال نظر', 'danger')
        return redirect('products:product_details', slug=slug)

# __________________________________________________________________________
def add_score(request):
    productId=request.GET.get('productId')
    score=request.GET.get('score')

    product=Product.objects.get(id=productId)
    Scoring.objects.create(
        product=product,
        scoring_user=request.user,
        score=score
    )
    return HttpResponse('امتیاز شما با موفقیت ثبت شد')

# __________________________________________________________________________
# درج علاقه یک کالا در دیتا بیس
def add_to_favorite(request):
    productId=request.GET.get('productId')
    product=Product.objects.get(id=productId)
    flag=Favorite.objects.filter(
                            Q(favorite_user_id=request.user.id) &
                            Q(product_id=productId)).exists()  # ها نیست favorite قبل از اینکه داخل دیتا بیس علاقه درجش کنی ببین وجود داشته ببین این یوزر جاری کالایی که الان داره تو علاقه ها اد میشه قبلا تو جدول
    # اگر داخل دیتا بیس نبود تو جدول درجش کن
    if not flag:
        Favorite.objects.create(
                            product=product,
                            favorite_user=request.user
        )
        return HttpResponse('این کالا به لیست علایق شما اضافه شد')
    return HttpResponse('این کالا قبلا در لیست علایق شما قرار گرفته')

# __________________________________________________________________________
# این تابع هرجا صدااش بزنیم یه صفحه اچ تی ام ال جدا هست که دلیست علاقه مندی های کاربری که لاگ این کرده رو نشون میده بدرد پنل کاربری خیلی میخوره
class UserFavoriteView(View):
    def get(self, request, *args, **kwargs):
        user_favorite_products=Favorite.objects.filter(favorit_user_id=request.user.id)
        return render(request, 'csf_app/user_favorit.html', {'user_favorite_products':user_favorite_products})


