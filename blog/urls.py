from django.urls import path
from . import views

urlpatterns = [ # IP주소/blog/
    #path('', views.index),
    path('', views.PostList.as_view()),
    #path('<int:pk>/', views.single_post_page)
    path('<int:pk>/', views.PostDetail.as_view())
]