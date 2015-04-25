from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'shirtstart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^', include('web.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)