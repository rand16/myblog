from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=255, label="タイトル")
    content = forms.CharField(label="内容", widget=forms.Textarea())
