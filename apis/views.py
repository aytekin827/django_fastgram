from os import stat
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from contents.models import Content, Image, FollowRelation



class BaseView(View):
    # staticmethod는 인스턴스를 만들지 않아도 해당 매서드를 사용할 수 있게끔 해줌
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(data=result, status=status)


class UserCreateView(BaseView):
    @method_decorator(csrf_exempt) 
    # ajax로 post요청을 보낼때 csrf 보안 절차를 건너뛰기 위한 데코레이터
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)

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
        # print(email)
        try:
            validate_email(email)
        except ValidationError:
            return self.response(message='올바른 이메일을 입력해주세요', status=400)

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)
        return self.response({'user.id':user.id})


class UserLoginView(BaseView):
    @method_decorator(csrf_exempt) 
    # ajax로 post요청을 보낼때 csrf 보안 절차를 건너뛰기 위한 데코레이터
    def dispatch(self, request, *args, **kwargs):
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)

        user = authenticate(request, username=username, password=password)
        if user == None:
            return self.response(message='입력 정보를 확인해주세요', status=400)
        login(request, user)

        return self.response()


class UserLogoutView(BaseView):
    def get(self, request):
        logout(request)
        return self.response()


class ContentCreateView(BaseView):
    def post(self, request):
        text = request.POST.get('text','').strip()
        content = Content.objects.create(user=request.user, text=text)
        for idx, file in enumerate(request.FILES.values()):
            Image.objects.create(content=content, image=file, order=idx)
        return self.response({})


class RelationCreateView(BaseView):
    @method_decorator(csrf_exempt) 
    # ajax로 post요청을 보낼때 csrf 보안 절차를 건너뛰기 위한 데코레이터
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            user_id = request.POST.get('id','')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            relation = FollowRelation.objects.create(follower=request.user)

        try:
            if user_id == request.user.id:
                #자기 자신은 팔로우 안되게끔
                raise IntegrityError
            relation.followee.add(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.', status=400)
        
        return self.response({})


class RelationDeleteView(BaseView):
    @method_decorator(csrf_exempt) 
    # ajax로 post요청을 보낼때 csrf 보안 절차를 건너뛰기 위한 데코레이터
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            user_id = request.POST.get('id','')
        except ValueError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            relation = FollowRelation.objects.get(follower=request.user)
        except FollowRelation.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            if user_id == request.user.id:
                #자기 자신은 언팔로우 안되게끔
                raise IntegrityError
            relation.followee.remove(user_id)
            relation.save()
        except IntegrityError:
            return self.response(message='잘못된 요청입니다.', status=400)
        
        return self.response({})