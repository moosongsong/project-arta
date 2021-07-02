from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
import datetime
from exhibition.models import Exhibition, Piece, ExhibitionLike, Material


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
        else:
            exhibition_list = Exhibition.objects.filter(user=self.request.user).order_by('end_at')

        return exhibition_list

    def get_context_data(self, **kwargs):
        open_mode = self.kwargs['pk']
        context = super(ExhibitionListForArtist, self).get_context_data()
        if open_mode in ['all', 'open', 'close', 'ready']:
            context['category_name'] = open_mode
        else:
            context['category_name'] = 'all'

        return context


# 전시회의 작품들을 출력하는 클래스
class PieceListForArtist(ListView):
    model = Piece
    paginate_by = 8
    template_name = 'exhibition/ARTA_artist_exhibition_show.html'

    def get_queryset(self):
        exhibition_id = self.kwargs['pk']
        piece_list = Piece.objects.filter(exhibition_id=exhibition_id).order_by('order')
        return piece_list

    def get_context_data(self, **kwargs):
        context = super(PieceListForArtist, self).get_context_data()
        pk = self.kwargs['pk']
        exhibition = Exhibition.objects.get(pk=pk)
        if self.request.user.is_authenticated:
            user = self.request.user
            like = ExhibitionLike.objects.filter(user=user, exhibition_id=pk)
            context['like_list'] = like
            if user == exhibition.user:
                context['is_your_exhibition'] = True
            else:
                context['is_your_exhibition'] = False

        context['exhibition'] = get_object_or_404(Exhibition, pk=pk)
        context['materials'] = Material.objects.all()
        context['total'] = Piece.objects.filter(exhibition=exhibition).count()
        return context
