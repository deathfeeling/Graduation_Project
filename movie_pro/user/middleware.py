from django.http import HttpResponseRedirect
from django.urls import reverse



def block_sms_middleware(get_resp):

    def middleware(request, *args, **kwargs):
        # 请求时要做的事情
        path_now = request.path
        unchecked_address = ['/user/login/', '/user/register/', '/user/captcha/']
        if path_now not in unchecked_address:
            token = request.session.get('token')
            if not token:
                return HttpResponseRedirect(reverse('user:login'))
        resp = get_resp(request, *args, **kwargs)

        return resp
    return middleware