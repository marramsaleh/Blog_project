from clone_app.models import Post, Comment
from django import forms



class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields= ('author_post','title','text')
        widgets ={
         'tilte':forms.TextInput(attrs={'class':'textinputclass'}),
         # conect to css classes
         'text':forms.Textarea(attrs={'class':'editable  medium-editor-textarea postcontent'}),

        }


class CommentForm(forms.ModelForm):

    class Meta():
        model=Comment
        fields =('author_comments','text',)
        widgets ={
          'author_comments':forms.TextInput(attrs={'class':'textinputclass'}),
          'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
