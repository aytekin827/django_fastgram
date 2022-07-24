from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.shortcuts import redirect

from contents.views import HomeView, RelationView


class NonUserTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            print('로그인이 되어 홈페이지로 이동합니다')
            return redirect('contents_home')
        return super().dispatch(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include('apis.urls')),
    path('', HomeView.as_view(), name='contents_home'),
    path('login/', NonUserTemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', NonUserTemplateView.as_view(template_name='register.html'), name='register'),
    path('relation/', RelationView.as_view(template_name='relation.html'), name='contents_relation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
