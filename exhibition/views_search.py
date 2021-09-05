from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q


# 검색페이지를 출력하는 메소드
def search_page(request):
    return render(
        request,
        'exhibition/common/search.html',
    )


# 전시회 검색 페이지
class ExhibitionSearch(ListView):
    model = Exhibition
    template_name = 'exhibition/common/search_result.html'
    paginate_by = 8

    def get_queryset(self):
        q = self.kwargs['q']
        piece_list = Exhibition.objects.filter(
            Q(name__contains=q) | Q(explain__contains=q) | Q(category__name__contains=q)).distinct().order_by('pk')
        return piece_list

    def get_context_data(self, **kwargs):
        context = super(ExhibitionSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q}'
        return context


# 그림 검색 페이지
class PieceSearch(ListView):
    model = Piece
    template_name = 'exhibition/common/search_result.html'
    paginate_by = 8

    def get_queryset(self):
        q = self.kwargs['q']
        piece_list = Piece.objects.filter(
            Q(name__contains=q) | Q(author__contains=q) | Q(material__name__contains=q)).distinct().order_by('pk')
        return piece_list

    def get_context_data(self, **kwargs):
        context = super(PieceSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'{q}'
        return context
