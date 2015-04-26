from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^catalog/$', views.catalog, name="catalog"),
    # url(r'^catalog/(?P<search_word>[\w|\W]+)/$', views.search, name="search"),
    url(r'^join/(?P<shirt_id>[\w|\W]+)/$', views.join, name="join"),
    url(r'^buy/(?P<shirt_id>[\w|\W]+)/$', views.buy, name="buy"),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^login/', views.login, name="login"),
    url(r'^comment/(?P<comment_shirt_id>[\w|\W]+)/$', views.comment, name="comment"),
    # url(r'^register/$', views.register, name="re")
    # status things
    url(r'^status/waiting/', views.status_waiting, name="status_waiting"),
    url(r'^status/in-progress/', views.status_in_progress, name="status_in_progress"),
    url(r'^status/purchase-history/', views.status_purchase_history, name="status_purchase_history"),

    url(r'^payment/(?P<shirt_id>[\w|\W]+)/$', views.payment, name="payment"),
    url(r'^cart/', views.cart, name="cart"),
    url(r'^design/', views.design, name="design"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^withdraw/', views.withdraw, name="withdraw"),
    url(r'^admin/', views.admin, name="admin"),
]
