from django.urls import path
from blog import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 投稿の詳細ページ．<int:pk>によって，どの投稿の詳細ページかを把握
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    # 新規投稿用のページ．
    path('post/new', views.CreatePostView.as_view(), name='post_new'),
    # 投稿内容確認用のページ
    path('post/confirm', views.ConfirmPostView.as_view(), name='post_confirm'),
    # 投稿完了用のページ
    path('post/regist', views.RegistPostView.as_view(), name='post_regist'),
    # 投稿編集用のページ
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='post_edit'),
    # 投稿編集確認用のページ
    path('post/<int:pk>/confirm', views.ConfirmPostEditView.as_view(), name='post_edit_confirm'),
    # 投稿削除用のページ
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
]