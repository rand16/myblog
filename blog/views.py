from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, DetailView, CreateView
from .models import Post
from .forms import PostForm
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from urllib.parse import urlencode

# Create your views here.
class IndexView(TemplateView):
    # TemplateViewを使用
    ## テンプレートファイルの連携
    template_name = "blog/index.html"

    ## 変数を渡す
    def get_context_data(self, **kwargs):
        # super()で親クラスであるTemplateViewのメソッドget_context_data()を呼び出している
        context = super().get_context_data(**kwargs)
        # id順にPostを整理したもの
        post_data = Post.objects.order_by('-id')
        context["post_data"] = post_data
        return context
    
class PostDetailView(DetailView):
    # DetailViewを使用
    ## モデルクラスを指定することで，対象のデータベースのテーブルと連携する
    model = models.Post
    ## 指定したオブジェクト名をテンプレートに渡す
    context_object_name = "post_data"
    ## テンプレートファイルの連携
    template_name = "blog/post_detail.html"

    '''
    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        # idを指定することで，特定のデータを取得できる
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'blog/post_detail.html', {
            'post_data': post_data
        })
    '''
    
class CreatePostView(LoginRequiredMixin, CreateView):
    ## テンプレートファイルの連携
    template_name = "blog/post_form.html"
    ## フォームのクラス
    form_class = PostForm
    ## モデルのクラス
    model = Post
    ## 成功時に飛ぶURL
    ##success_url = reverse_lazy('blog:index')

    # 最初に呼ばれる関数
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'blog/post_form.html', {
            'form': form
        })
    
    '''
    # 「確認する」ボタンが押された場合
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if form.is_valid():
            # リダイレクト先のパスを取得
            redirect_url = reverse_lazy('post_confirm')
            # パラメータのdictをurlencodeする．複数のパラメータを含める
            parameters = urlencode({'title':form.cleaned_data['title'],'content':form.cleaned_data['content']})
            # URLにパラメータを付与
            url = f'{redirect_url}?{parameters}'
            return redirect(url)

        return render(request, 'blog/post_form.html', {
            'form': form
        })  
    '''

    
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
    
    # 「確認する」ボタンが押された場合
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if form.is_valid():
            # リダイレクト先のパスを取得
            redirect_url = reverse_lazy('post_confirm')
            # パラメータのdictをurlencodeする．複数のパラメータを含める
            parameters = urlencode({'title':form.cleaned_data['title'],'content':form.cleaned_data['content']})
            # URLにパラメータを付与
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
        
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
    
class ConfirmPostView(LoginRequiredMixin, View):
    # 最初に呼ばれる関数
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            form = PostForm(
                request.POST or None,
                initial= {
                    'title': request.POST['title'],
                    'content': request.POST['content']
                }
            )
            post_data = Post()
            post_data.title = request.POST['title']
            post_data.content = request.POST['content']
            return render(request, 'blog/post_form_confirm.html', {
                'form': form,
                'post_data': post_data
            })
        else:
            return render(request, 'blog/post_form.html', {
                'form': form
            })

class RegistPostView(LoginRequiredMixin, View):
    # 最初に呼ばれる関数
    def post(self, request, *args, **kwargs):
        if request.POST.get('next', '') == 'create':
            post_data = Post()
            post_data.author = request.user
            post_data.title = request.POST['title']
            post_data.content = request.POST['content']
            post_data.save()
            return render(request, 'blog/post_complete.html')
        elif request.POST.get('next', '') == 'back':
            form = PostForm(
                request.POST or None,
                initial= {
                    'title': request.POST['title'],
                    'content': request.POST['content']
                }
            )
            return render(request, 'blog/post_form.html', {
                'form': form
            })