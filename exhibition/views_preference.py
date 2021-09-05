from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q


class LikeManage:
    def exhibition_like(request, pk):
        if request.user.is_authenticated:
            exhibition = get_object_or_404(Exhibition, pk=pk)
            older_like = ExhibitionLike.objects.filter(exhibition=exhibition, user=request.user)

            if older_like:
                return redirect(exhibition.get_absolute_url())

            like = ExhibitionLike(exhibition=exhibition, user=request.user)
            like.save()
            return redirect(like.get_absolute_url())
        else:
            return PermissionDenied

    def exhibition_dislike(request, ak, pk):
        like = get_object_or_404(ExhibitionLike, pk=pk)
        exhibition = like.exhibition
        if request.user.is_authenticated and request.user == like.user:
            like.delete()
            return redirect(exhibition.get_absolute_url())
        else:
            return PermissionDenied

    def piece_like(request, pk):
        if request.user.is_authenticated:
            piece = get_object_or_404(Piece, pk=pk)
            older_like = PieceLike.objects.filter(piece=piece, user=request.user)
            if older_like:
                return redirect(piece.get_absolute_url())

            like = PieceLike(piece=piece, user=request.user)
            like.save()
            return redirect(like.get_absolute_url())
        else:
            return PermissionDenied

    def piece_dislike(request, ak, pk):
        like = get_object_or_404(PieceLike, pk=pk)
        if request.user.is_authenticated and like.user == request.user:
            like.delete()
            return redirect(like.get_absolute_url())
        else:
            return PermissionDenied


class LikePieceList(ListView):
    model = PieceLike
    template_name = 'exhibition/common/preference.html'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        piece_like_list = PieceLike.objects.filter(user=user).order_by('pk')
        return piece_like_list

    def get_context_data(self, **kwargs):
        context = super(LikePieceList, self).get_context_data()
        context['mode'] = '작품'
        return context


class LikeExhibitionList(ListView):
    model = ExhibitionLike
    template_name = 'exhibition/common/preference.html'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        exhibition_like_list = ExhibitionLike.objects.filter(user=user).order_by('pk')
        return exhibition_like_list

    def get_context_data(self, **kwargs):
        context = super(LikeExhibitionList, self).get_context_data()
        context['mode'] = '전시회'
        return context
