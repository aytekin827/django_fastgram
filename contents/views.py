from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

from .models import Image, Content, FollowRelation

class HomeView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        user = self.request.user
        followees = FollowRelation.objects.filter(follower=user).values_list('followee__id', flat=True)
        lookup_user_ids = [user.id] + list(followees)
        # select_relate, prefetch_relate는 쿼리최적화에 관련된 내용
        context['contents'] = Content.objects.select_related('user').prefetch_related('image_set').filter(
            user__id__in = lookup_user_ids
        )
        # print(lookup_user_ids)
        return context


class RelationView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = 'relation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user 
     
        followee = FollowRelation.objects.get(follower=user)
        context['followees'] = followee.followee.all()

        followers = FollowRelation.objects.all().filter(followee__username__in = [user])
        context['followers'] = followers
        return context