from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from demo import views

urlpatterns = [
    path('', RedirectView.as_view(url='/static/index.html', permanent=True)),
    path('api/image/', views.ApiImage.as_view()),
    path('api/image/<uuid:id>/', views.ApiImage.as_view()),
    path('admin/', admin.site.urls),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
