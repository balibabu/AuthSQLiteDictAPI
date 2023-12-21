from django.urls import path
from . import views


urlpatterns = [
    path('', views.execute_sql, name='execute_sql'),
    path('dict/', views.sql_dictionary, name='sql_dictionary'),
]
    