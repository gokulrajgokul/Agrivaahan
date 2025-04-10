from django.urls import path,include
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('admin/',admin.site.urls),
     path('',include('Agrivehicles.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)