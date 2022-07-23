from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Image, Content

class HomeView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user
        # followees = 
        # lookup_user_ids = [user.id] + list(followees)
        # user와 imageset을 조인하는 
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set')

        return context