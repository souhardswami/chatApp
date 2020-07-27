from django.urls import path, re_path


from . import views



app_name = 'app'
urlpatterns = [
    path("",views.main,name="main"),
]
