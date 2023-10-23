from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(View):
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        # id順にPostを整理したもの
        post_data = Post.objects.order_by('-id')
        # renderでindex.htmlを呼び出し，そのリクエストにpost_dataを含める
        return render(request, 'blog/index.html', {
            'post_data': post_data
        })
    
class PostDetailView(View):
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        # idを指定することで，特定のデータを取得できる
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_detail.html', {
            'post_data': post_data
        })
    
class CreatePostView(LoginRequiredMixin, View):
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    
    # 投稿ボタンをクリックしたときに呼ばれる関数
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            # form.cleaned_dataでフォームの入力内容を取得できる
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            # データベースに保存
            post_data.save()
            # 詳細画面にリダイレクト
            return redirect('post_detail', post_data.id)
        
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    
class PostEditView(LoginRequiredMixin, View):
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        # idを指定することで，特定のデータを取得できる
        post_data = Post.objects.get(id=self.kwargs['pk'])
        # formに編集するデータの情報を埋め込む
        form = PostForm(
            request.POST or None,
            initial= {
                'title': post_data.title,
                'content': post_data.content
            }
        )
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    
    # 投稿ボタンをクリックしたときに呼ばれる関数
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.author = request.user
            # form.cleaned_dataでフォームの入力内容を取得できる
            post_data.title = form.cleaned_data['title']
            post_data.content = form.cleaned_data['content']
            # データベースに保存
            post_data.save()
            # 詳細画面にリダイレクト
            return redirect('post_detail', self.kwargs['pk'])
        
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    
class PostDeleteView(LoginRequiredMixin, View):
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        # idを指定することで，特定のデータを取得できる
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_delete.html', {
            'post_data': post_data
        })
    
    # 削除ボタンをクリックしたときに呼ばれる関数
    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')