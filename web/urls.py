from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^catalog/', views.catalog, name="catalog"),
    url(r'^join/', views.join, name="join"),
    url(r'^buy/', views.buy, name="buy"),
    # status things
    url(r'^status/waiting/', views.status_waiting, name="status_waiting"),
    url(r'^status/in-progress/', views.status_in_progress, name="status_in_progress"),
    url(r'^status/purchase-history/', views.status_purchase_history, name="status_purchase_history"),

    url(r'^payment/', views.payment, name="payment"),
    url(r'^cart/', views.cart, name="cart"),
    url(r'^design/', views.design, name="design"),
    url(r'^profile/', views.profile, name="profile"),
    url(r'^withdraw/', views.withdraw, name="withdraw"),
    url(r'^admin/', views.admin, name="admin"),
]
