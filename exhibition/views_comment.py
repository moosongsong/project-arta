from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q


# 댓글 관리 클래스
class CommentManage:
    # 댓글 생성
    def create_comment(request, pk):
        if request.user.is_authenticated:
            piece = get_object_or_404(Piece, pk=pk)

            if request.method == 'POST':
                comment = Comment(content=request.POST.get('content'), piece=piece, user=request.user)
                comment.save()
                messages.success(request, "댓글이 등록되었습니다.")
                return redirect(comment.get_absolute_url())
            else:
                return redirect(piece.get_absolute_url())
        else:
            return PermissionDenied

    # 댓글 삭제
    def delete_comment(request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        piece = comment.piece
        if request.user.is_authenticated and request.user == comment.user:
            comment.delete()
            messages.success(request, "댓글이 삭제되었습니다.")
            return redirect(piece.get_absolute_url())
        else:
            raise PermissionDenied


# 방명록 관리 클래스
class GuestbookManage:
    # 방명록 생성
    def create_guestbook(request, pk):
        if request.user.is_authenticated:
            exhibition = get_object_or_404(Exhibition, pk=pk)

            if request.method == 'POST':
                guestbook = GuestBook(content=request.POST.get('content'), exhibition=exhibition, user=request.user)
                guestbook.save()
                messages.success(request, "방명록이 등록되었습니다.")
                return redirect(guestbook.get_absolute_url())
            else:
                return redirect(exhibition.get_absolute_url())
        else:
            return PermissionDenied

    # 방명록 삭제
    def delete_guestbook(request, pk):
        guestbook = get_object_or_404(GuestBook, pk=pk)
        exhibition = guestbook.exhibition
        if request.user.is_authenticated and request.user == guestbook.user:
            guestbook.delete()
            messages.success(request, "방명록이 삭제되었습니다.")
            return redirect(exhibition.get_absolute_url())
        else:
            raise PermissionDenied
