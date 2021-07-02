from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
import datetime
from django.contrib.auth.models import User


# 단일 페이지만 출력하는 모듈입니다.
class SinglePage:
    # 랜딩페이지를 출력하는 메소드
    def landing_page(request):
        return render(
            request,
            'exhibition/ARTA_main_page.html'
        )

    # 서비스 소개페이지를 출력하는 메소드
    def about_page(request):
        return render(
            request,
            'exhibition/ARTA_introduction_page.html'
        )

    # 로그인 페이지를 출력하는 메소드
    def login_page(request):
        return render(
            request,
            'exhibition/ARTA_login_kakao_page.html'
        )

    # 검색페이지를 출력하는 메소드
    def search_page(request):
        return render(
            request,
            'exhibition/ARTA_search_page.html',
        )

    # 테스트 페이지를 출력하는 메소드
    def manage_page(request):
        if request.user.is_authenticated:
            return render(
                request,
                'exhibition/ARTA_manage_page.html',
                # {
                #     'category_name': category,
                # }
            )
        else:
            return redirect('/')

    # 테스트 페이지를 출력하는 메소드
    def test_page(request):
        return render(
            request,
            'exhibition/ARTA_artist_exhibition_show.html',
        )
