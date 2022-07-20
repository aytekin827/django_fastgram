from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login


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
        if not username:
            return self.response(message='아이디를 입력해주세요', status=400)
        password = request.POST.get('password','')
        if not password:
            return self.response(message='패스워드를 입력해주세요.', status=400)
        email = request.POST.get('email','')
        if not email:
            return self.response(message='이메일를 입력해주세요.', status=400)
        try:
            validate_email(email)
        except ValidationError:
            self.response(message='올바른 이메일을 입력해주세요', status=400)

        try:
            user = User.object.create_user(username, password, email)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id':user.id})


class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return self.response(message='입력 정보를 확인해주세요')
        login(request, user)

        return self.response

        
        