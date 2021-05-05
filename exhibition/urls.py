from django.urls import path
from . import views

urlpatterns = [
    # path('', views.SinglePage.landing_page),
    path('', views.ExhibitionList.as_view()),
    path('about/', views.SinglePage.about_page),
    path('credit/', views.SinglePage.credit_page),
    path('login/', views.SinglePage.login_page),

    path('preference/', views.LikePieceList.as_view()),
    path('preference/piece/', views.LikePieceList.as_view()),
    path('preference/exhibition/', views.LikeExhibitionList.as_view()),
    path('search/', views.SearchPage.search_page),
    path('search/result/piece/<str:q>/', views.PieceSearch.as_view()),
    path('search/result/exhibition/<str:q>/', views.ExhibitionSearch.as_view()),

    path('exhibition/', views.ExhibitionList.as_view()),
    path('exhibition/', views.ExhibitionList.as_view()),
    path('exhibition/<int:pk>/', views.PieceList.as_view()),
    path('exhibition/category/<str:slug>/', views.CategoryManage.category_page),
    path('exhibition/<int:pk>/new_guestbook/', views.GuestbookManage.new_guestbook),
    path('exhibition/delete_guestbook/<int:pk>/', views.GuestbookManage.delete_guestbook),
    path('exhibition/<int:pk>/new_like/', views.LikeManage.exhibition_like),
    path('exhibition/<int:ak>/dislike/<int:pk>/', views.LikeManage.exhibition_dislike),
    path('exhibition/<int:pk>/share/', views.ShareManage.exhibition_share),

    path('exhibition/piece/<int:pk>/', views.PieceDetail.as_view()),
    path('exhibition/piece/<int:pk>/new_comment/', views.CommentManage.new_comment),
    path('exhibition/piece/delete_comment/<int:pk>/', views.CommentManage.delete_comment),
    path('exhibition/piece/<int:pk>/new_like/', views.LikeManage.piece_like),
    path('exhibition/piece/<int:ak>/dislike/<int:pk>/', views.LikeManage.piece_dislike),
    path('exhibition/piece/<int:pk>/share/', views.ShareManage.piece_share),

]
