from django.urls import path
from crm import views


urlpatterns = {
    path('', views.index, name="index"),
    # path('customers/', views.customer_list, name="customer_list"),
}
