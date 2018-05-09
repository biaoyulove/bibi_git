from django.urls import path
from king_admin import views


urlpatterns = {
    path('index/', views.index),
    path('<str:app_name>/<str:table_name>/', views.display_table_obj, name="table_obj"),
    path('<str:app_name>/<str:table_name>/<int:obj_id>/change/', views.table_obj_change, name="table_obj_change"),
    path('<str:app_name>/<str:table_name>/add/', views.table_obj_add, name="table_obj_add"),
    path('<str:app_name>/<str:table_name>/<int:delete_id>/delete/', views.table_obj_delete, name="obj_delete"),
}
