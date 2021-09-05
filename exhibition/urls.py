from django.urls import path
from . import views, views_user, views_manage, views_single, views_crolling, views_recommend, views_search, \
    views_comment

urlpatterns = [
    path('', views_single.SinglePage.landing_page),
    path('about/', views_single.SinglePage.about_page),
    path('login/', views_single.SinglePage.login_page),
    path('test/', views_single.SinglePage.test_page),
    path('reset/', views_crolling.reset_exhibitions),
    path('profile/', views_user.UserDetail.profile_page),
    # path('artist/', views_single.SinglePage.test_page),
    path('initial/', views_user.InitialPreference.preference_page),
    path('initial_submit/', views_user.InitialPreference.preference_init),
    path('recommend/', views_recommend.Recommend.get_recommend_page),

    path('preference/', views.LikePieceList.as_view()),
    path('preference/piece/', views.LikePieceList.as_view()),
    path('preference/exhibition/', views.LikeExhibitionList.as_view()),

    path('search/', views_search.search_page),
    path('search/result/piece/<str:q>/', views_search.PieceSearch.as_view()),
    path('search/result/exhibition/<str:q>/', views_search.ExhibitionSearch.as_view()),

    path('exhibition/', views_user.ExhibitionList.as_view()),
    path('exhibition/<int:pk>/', views_user.PieceList.as_view()),
    path('exhibition/category/<str:slug>/', views.CategoryManage.category_page),
    path('exhibition/<int:pk>/new_guestbook/', views_comment.GuestbookManage.create_guestbook),
    path('exhibition/delete_guestbook/<int:pk>/', views_comment.GuestbookManage.delete_guestbook),
    path('exhibition/<int:pk>/new_like/', views.LikeManage.exhibition_like),
    path('exhibition/<int:ak>/dislike/<int:pk>/', views.LikeManage.exhibition_dislike),

    path('exhibition/piece/<int:pk>/', views_user.PieceDetail.as_view()),
    path('exhibition/piece/<int:pk>/new_comment/', views_comment.CommentManage.create_comment),
    path('exhibition/piece/delete_comment/<int:pk>/', views_comment.CommentManage.delete_comment),
    path('exhibition/piece/<int:pk>/new_like/', views.LikeManage.piece_like),
    path('exhibition/piece/<int:ak>/dislike/<int:pk>/', views.LikeManage.piece_dislike),

    path('info/', views_single.SinglePage.manage_page),
    path('manage/<str:pk>/', views_manage.ExhibitionListForArtist.as_view()),
    path('manage/exhibition/<int:pk>/', views_manage.PieceListForArtist.as_view()),
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
