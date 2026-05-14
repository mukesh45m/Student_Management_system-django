from django.urls import path
from .  import views

urlpatterns=[
    
    path('',views.main,name='main'),
    path('home/',views.home,name='home'),
    path('add/',views.add,name='add'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('add_marks/<int:id>/',views.add_marks,name='add_marks'),
    path('student/<int:id>/',views.student_detail,name='student_detail'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
    ]