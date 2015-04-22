from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'shirtstart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^', include('web.urls')),
]
