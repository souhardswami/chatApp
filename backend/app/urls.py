from django.urls import path, re_path


from . import views



app_name = 'app'
urlpatterns = [
    path("",views.home,name="main"),
    path("user/<str:name>",views.user,name="main"),
    path("user/<str:name>/createroom",views.createroom,name="createroom"),
]
