from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare, InitialLike, ExternalExhibition
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
import datetime
from django.contrib.auth.models import User


# 전시회의 목록을 출력하는 클래스
class ExhibitionList(ListView):
    model = Exhibition
    paginate_by = 4
    template_name = 'exhibition/user/user_exhibition_list.html'

    def get_queryset(self):
        # exhibition_list = Exhibition.objects.filter(end_at__gte=datetime.datetime.now(),
        #                                             start_at__lte=datetime.datetime.now()).order_by('end_at')
        exhibition_list = Exhibition.objects.order_by('end_at')
        return exhibition_list

    def get_context_data(self, **kwargs):
        context = super(ExhibitionList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['category_name'] = '전체'
        return context


# 전시회의 작품들을 출력하는 클래스
class PieceList(ListView):
    model = Piece
    paginate_by = 8
    template_name = 'exhibition/user/user_exhibition_detail.html'

    def get_queryset(self):
        exhibition_id = self.kwargs['pk']
        piece_list = Piece.objects.filter(exhibition_id=exhibition_id).order_by('author')
        return piece_list

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        exhibition = Exhibition.objects.get(pk=pk)

        context = super(PieceList, self).get_context_data()
        exhibition.click_count = exhibition.click_count + 1
        exhibition.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            like = ExhibitionLike.objects.filter(user=user, exhibition_id=pk)
            context['like_list'] = like
            click = ExhibitionClick(user=user, exhibition_id=pk)
            click.save()
            if user == exhibition.user:
                context['is_your_exhibition'] = True
            else:
                context['is_your_exhibition'] = False

        try:
            ex_id = ExternalExhibition.objects.get(exhibition_id=exhibition.id)
            context['is_external'] = True
            context['external'] = ex_id
        except:
            context['is_external'] = False

        context['exhibition'] = get_object_or_404(Exhibition, pk=pk)
        context['materials'] = Material.objects.all()
        context['total'] = Piece.objects.filter(exhibition=exhibition).count()
        return context


# 작품의 내용을 출력하는 클래스
class PieceDetail(DetailView):
    model = Piece
    template_name = 'exhibition/user/user_piece_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PieceDetail, self).get_context_data()
        pk = self.kwargs['pk']
        piece = Piece.objects.get(pk=pk)
        piece.click_count = piece.click_count + 1
        piece.save()
        if self.request.user.is_authenticated:
            user = self.request.user
            like = PieceLike.objects.filter(user=user, piece_id=pk)
            context['like_list'] = like
            click = PieceClick(user=user, piece_id=pk)
            click.save()

        return context


# 초기 카테고리를 선택하는 클래스
class InitialPreference:
    # 초기 선호 카테고리를 선택하는 페이지 호출
    def preference_page(request):
        if request.user.is_authenticated:
            flag = InitialLike.objects.filter(user=request.user)
            if flag:
                messages.add_message(request, messages.ERROR, "초기 설정은 바꿀 수 없습니다.")
                return redirect("/info/")
            else:
                category = Category.objects.all()
                return render(
                    request,
                    'exhibition/user/initial_preference.html',
                    {
                        'categories': category,
                    }
                )
        else:
            return redirect('/')

    # 초기 선호 카테고리에 대한 처리
    def preference_init(request):
        if request.user.is_authenticated and request.method == "GET":
            selected = request.GET.getlist('init_like')
            print(selected)
            for element in selected:
                temp = InitialLike(user=request.user, category_id=int(element))
                temp.save()
            messages.add_message(request, messages.SUCCESS, "초기 설정이 완료되었습니다.")
        return redirect('/initial/')


class UserDetail:
    def profile_page(request):
        user = request.user
        if user.is_authenticated:
            return render(
                request,
                'exhibition/common/profile.html',
                {
                    'user': user,
                }
            )
        else:
            return redirect('/info/')
