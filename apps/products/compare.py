class CompareProduct:
    def __init__(self, request):
        self.session=request.session  # اول ریکوست سشن رو به این کلاس اضافه میکنم
        compare_product=self.session.get('compare_product')  # با متد گت میام بررسی میکنم ببینم سشنی با این اسم هست یا نه که برای اولین بار وجود نداره compare_product و بعد اسم سشنم رو میزارم مثلا
        if not compare_product:
            compare_product=self.session['compare_product']=[]   # اگر خالیه یعنی اولین بار هست و نال هست بیا این لیست خالی رو بهش نسبت بده پس اولین دور که این متد فراخوانی میشه یه سشن خالیه
        self.compare_product=compare_product  # و حالا میتونم هرکاری با این شسن بکنم اد کنم به لیست و غیره
        self.count=len(self.compare_product)

# _______________________________________________________________________________
    def __iter__(self):
        compare_product=self.compare_product.copy()
        for item in compare_product:
            yield item

# _______________________________________________________________________________
# مثلا هربار که تورو متد ادش رو صدا زدم تو ذهنت داشته باش یه پروداکت آیدی براش میفرستم که عدد و باید به اینت تبدیلش کنم چون سشن فقط به رشته ذخیره میکنه
# و اگر داخلش نبود بیا اضافه کن این سش رو داخلش
    def add_to_compare_product(self, productId):
        ptoductId=int(productId)
        if productId not in self.compare_product:
            self.compare_product.append(productId)
            self.count=len(self.compare_product)   # و نهایتا بعد از اینکه بهش اضافه کردم تعداد عناصر لیست رو حساب میکنم و میریزمش تو کانت
            self.session.modified=True   # سشن هم که همیشه مادیفای باید بعدش ترو کنیم تا تغییرات اعمال بشه

# _______________________________________________________________________________
# و تورو هم هربار صدات زدم یه پروداکت آیدی بهت میدم پاکش کن
    def delete_from_compare_product(self, productId):
        self.compare_product.remove(int(productId))
        self.count=len(self.compare_product)  # و هربار که پاک کردم میتونم تعداد سشنم رو دوباره حساب کنم
        self.session.modified=True

# _______________________________________________________________________________
# و هر بار بخوام کل سشن لیستم رو پاک کنم این تابع رو صدا میکنم
    def clean_compare_product(self):
        del self.session['compare_product']
        self.session.modified=True
