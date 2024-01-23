from app1 import views
from django.urls import path

urlpatterns = [
    path("login",views.user_login,name='login'),
    path("signup",views.user_signup),
    path("add_todo/",views.add_todo),
    path("",views.home ,name='home'),
    path("logout",views.signout),
    path("delete-todo/<int:id>",views.delete_todo),
    path("change-status/<int:id>/<str:status>",views.change_todo),
    path("update-todo/<int:id>",views.update_todo,name='update_todo'),
     path("",views.display),
]