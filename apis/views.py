from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import IntegrityError


class BaseView(View):
    # staticmethod는 인스턴스를 만들지 않아도 해당 매서드를 사용할 수 있게끔 해줌
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status)


class UserCreateView(BaseView):
    @method_decorator(csrf_exempt) 
    # ajax로 post요청을 보낼때 csrf 보안 절차를 건너뛰기 위한 데코레이터
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')

        user = User.object.create_user(username, password, email)

        return self.response({'user.id':user.id})