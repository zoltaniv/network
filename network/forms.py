from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        widgets = {"text": forms.Textarea(attrs={
            "autofocus": True, # Do not work!!!
            "placeholder": "Input your post here",
            "rows": 5,
            "cols": 55,
            "style": "resize: none;"
        })}