from django import forms

class CommentForm(forms.Form):
    # هستن که وجود دارن داده رو میتونن نگهداری کنن اما کاربر نمیتونه اونو ببینه تو صفحه وب HiddenInput وقتی یه نظری داده میشه رو چه کالاییه یا رو چه کامنتیه پس اینجا نیاز به دوتا فیلد دارم آیدیه نظر و آیدیه محصول اما از جنس
    product_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    comment_text = forms.CharField(
                            label='دیدگاه شما',
                            error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                            widget=forms.Textarea(attrs={'class':'form-control','placeholder':'متن نظر','rows':'4'})
    )

