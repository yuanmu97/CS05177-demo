from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from demo import views

urlpatterns = [
    path('', views.Upload.as_view(), name='upload'),
    path('<uuid:id>/', views.Image.as_view(), name='image'),
    path('<uuid:id>/scan/', views.Scan.as_view(), name='scan'),
    path('<uuid:id>/correct/', views.Correct.as_view(), name='correct'),
    path('api/image/', views.ApiImage.as_view()),
    path('api/image/<uuid:id>/', views.ApiImage.as_view()),
    path('api/image/<uuid:id>/rects/', views.ApiRects.as_view()),
    path('admin/', admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
