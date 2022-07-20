from django.http import JsonResponse
from django.views import View


class BaseView(View):
    # staticmethod는 인스턴스를 만들지 않아도 해당 매서드를 사용할 수 있게끔 해줌
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status)