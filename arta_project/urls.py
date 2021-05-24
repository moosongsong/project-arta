from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('exhibition.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'documents_root':settings.MEDIA_ROOT}),
    # 디버깅 모드 해제할때 필요
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
