from django.urls import path
from . import views # 같은 폴더 내의 views.py를 import
from django.conf import settings
from django.conf.urls.static import static

app_name = 'opencv_webapp'

urlpatterns = [
    path('', views.first_view, name='first_view'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('detect_face/', views.detect_face, name='detect_face'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
