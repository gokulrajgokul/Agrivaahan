from django.urls import path,include, re_path
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from Agrivehicles import views
from django.views.static import serve

urlpatterns = [
   
    path('admin/',admin.site.urls),
    path('',include('Agrivehicles.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home')
] 
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)




if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Serve media manually when DEBUG = False (for local development)
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
 


handler404 = 'Agrivehicles.views.custom_404'


 
 