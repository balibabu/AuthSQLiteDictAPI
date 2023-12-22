from django.urls import path
from . import views,views2


urlpatterns = [
    path('', views.execute_sql, name='execute_sql'),
    path('dict/', views.sql_dictionary, name='sql_dictionary'),
    path('permit/', views2.permission, name='assign_permission'),
]
    