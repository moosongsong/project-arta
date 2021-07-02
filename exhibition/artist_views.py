from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
import datetime
from exhibition.models import Exhibition


# 작가의 전시회의 목록을 출력하는 클래스
class ExhibitionListForArtist(ListView):
    model = Exhibition
    paginate_by = 4
    template_name = 'exhibition/ARTA_artist_exhibition_list.html'

    def get_queryset(self):
        global exhibition_list
        open_mode = self.kwargs['pk']
        if open_mode == 'all':
            exhibition_list = Exhibition.objects.filter(user=self.request.user).order_by('end_at')
        elif open_mode == 'open':
            exhibition_list = Exhibition.objects.filter(user=self.request.user, end_at__gte=datetime.datetime.now(),
                                                        start_at__lte=datetime.datetime.now()).order_by('end_at')
        elif open_mode == 'close':
            exhibition_list = Exhibition.objects.filter(user=self.request.user,
                                                        end_at__lt=datetime.datetime.now()).order_by('end_at')
        elif open_mode == 'ready':
            exhibition_list = Exhibition.objects.filter(user=self.request.user,
                                                        start_at__gt=datetime.datetime.now()).order_by('end_at')
        return exhibition_list

    def get_context_data(self, **kwargs):
        open_mode = self.kwargs['pk']
        context = super(ExhibitionListForArtist, self).get_context_data()
        if open_mode == 'all' or open_mode == 'open' or open_mode == 'close' or open_mode == 'ready':
            context['category_name'] = open_mode
        else:
            context['category_name'] = 'all'
            return redirect('/manage/all/')

        return context
