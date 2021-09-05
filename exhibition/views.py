from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q


class CategoryManage:
    def category_page(request, slug):
        category = Category.objects.get(slug=slug)

        return render(
            request,
            'exhibition/user/user_exhibition_list.html',
            {
                'exhibition_list': Exhibition.objects.filter(category=category),
                'categories': Category.objects.all(),
                'category_name': category,
            }
        )


class MaterialManage:
    def meterial_page(request, slug):
        material = Material.objects.get(slug=slug)

        return render(
            request,
            'exhibition/user/user_exhibition_detail.html',
            {
                'piece_list': Piece.objects.filter(material=material),
                'materials': Material.objects.all(),
                'material_name': material,
            }
        )


class ShareManage:
    def exhibition_share(request, pk):
        if request.user.is_authenticated:
            exhibition = get_object_or_404(Exhibition, pk=pk)
            share = ExhibitionShare(exhibition=exhibition, user=request.user)
            share.save()
            return redirect(exhibition.get_absolute_url())
        else:
            return PermissionDenied

    def piece_share(request, pk):
        if request.user.is_authenticated:
            piece = get_object_or_404(Piece, pk=pk)
            share = PieceShare(piece=piece, user=request.user)
            share.save()
            return redirect(piece.get_absolute_url())
        else:
            return PermissionDenied
