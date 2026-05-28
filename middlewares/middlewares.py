import threading

# ورودی به کمک تردم رکوئست رو برگردونه get_response و این تکه کد رو بهش اضافه میکنیم توجه کن که داخل پروژه ریشه باشه که این کلاس از تردها استفاده میکنه و این کلاس امکان رو به من میده که بتونم توسط middlewares اگر تو پروژه ما نیاز پیدا کردیم که داخل ماژول مدلمون رکوئست داشته باشیم مثلا برای اینکه بدونیم کاربر جاری لاگ این شده از قبل، همجین فایلی درست میکنیم داخل پوشه
# middleware پروژه باید اضافه بشه داخل بخش  settings.py بعد اینکه این کد رو نوشتی به
class RequestMiddleware:
    def __init__(self, get_response, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local

    def __call__(self, request):
        self.thread_local.current_request = request
        response = self.get_response(request)
        return response
