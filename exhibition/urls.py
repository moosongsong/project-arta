from django.urls import path
from . import views

urlpatterns = [
    path('', views.SinglePage.landing_page),
    path('about/', views.SinglePage.about_page),
    path('login/', views.SinglePage.login_page),
    path('test/', views.SinglePage.test_page),

    path('preference/', views.LikePieceList.as_view()),
    path('preference/piece/', views.LikePieceList.as_view()),
    path('preference/exhibition/', views.LikeExhibitionList.as_view()),

    path('search/', views.SinglePage.search_page),
    path('search/result/piece/<str:q>/', views.PieceSearch.as_view()),
    path('search/result/exhibition/<str:q>/', views.ExhibitionSearch.as_view()),

    path('exhibition/', views.ExhibitionList.as_view()),
    path('exhibition/<int:pk>/', views.PieceList.as_view()),
    path('exhibition/category/<str:slug>/', views.CategoryManage.category_page),
    path('exhibition/<int:pk>/new_guestbook/', views.GuestbookManage.create_guestbook),
    path('exhibition/delete_guestbook/<int:pk>/', views.GuestbookManage.delete_guestbook),
    path('exhibition/<int:pk>/new_like/', views.LikeManage.exhibition_like),
    path('exhibition/<int:ak>/dislike/<int:pk>/', views.LikeManage.exhibition_dislike),

    path('exhibition/piece/<int:pk>/', views.PieceDetail.as_view()),
    path('exhibition/piece/<int:pk>/new_comment/', views.CommentManage.create_comment),
    path('exhibition/piece/delete_comment/<int:pk>/', views.CommentManage.delete_comment),
    path('exhibition/piece/<int:pk>/new_like/', views.LikeManage.piece_like),
    path('exhibition/piece/<int:ak>/dislike/<int:pk>/', views.LikeManage.piece_dislike),

    # path('manage/'),
    path('manage/exhibition/', views.ExhibitionListForArtist.as_view()),
    path('manage/exhibition/<int:pk>/', views.PieceListForArtist.as_view()),
    # path('manage/exhibition/<int:pk>/update/'),
    # path('manage/exhibition/<int:pk>/delete/'),
    # path('manage/exhibition/register/'),

    # path('manage/piece/'),
    # path('manage/piece/<int:pk>'),
    # path('manage/piece/register/<int:pk>'),
    # path('manage/piece/update/<int:pk>'),
    # path('manage/piece/delete/<int:pk>'),


    # 사용 보류
    # path('exhibition/<int:pk>/share/', views.ShareManage.exhibition_share),
    # path('exhibition/piece/<int:pk>/share/', views.ShareManage.piece_share),
]
