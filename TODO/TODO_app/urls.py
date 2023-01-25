from django.urls import path
from .views import TaskList, TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLogin,RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',CustomLogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),

    path('',TaskList.as_view(), name='TaskList'),
    path('task/<int:pk>',TaskDetail.as_view(), name='TaskDetail'),
    path('task-create',TaskCreate.as_view(), name='task-create'),
    path('update-task/<int:pk>', TaskUpdate.as_view(), name='update-task'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
]
