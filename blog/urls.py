from django.urls import path, include
from . import views

#app_name = 'blog'

urlpatterns = [ # IP주소/blog/
    #path('', views.index),
    path('', views.PostList.as_view()),
    #path('<int:pk>/', views.single_post_page)
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('<int:pk1>/comment/<int:pk2>/new_commentofcomment/', views.new_commentofcomment),
    path('update_coc/<int:pk>/',views.CommentOfCommentUpdate.as_view()),
    path('delete_coc/<int:pk>/',views.delete_coc),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('delete_post/<int:pk>/', views.delete_post),
    path('search/<str:q>/', views.PostSearch.as_view()),
#    path('test/', include('rest_framework.urls', namespace='rest_framework_category')),
]




