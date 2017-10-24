from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from clone_app.models import Post,Comment
from clone_app.forms import PostForm,CommentForm
from  django.urls  import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                   DetailView,CreateView,
                                   UpdateView,DeleteView)

# Create your views here.

# now we create classes not a def
class AboutView(TemplateView):
    template_name ='about.html'



class PostListView(ListView):
    model = Post
# generic views
    def get_queryset(self):
# __lte less than the current time, -publish :organize them disendent
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')




# i click it take me to another detailed view
class PostDetailView(DetailView):
    model=Post


class CreatePostView(LoginRequiredMixin,CreateView):
    # if he log in where to go
    login_url ='/login/'
    redirect_field_name='clone_app/post_detail.html'
    form_class = PostForm
    model =  Post
    # we use decorators usually but here it is a claass



class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/login/'
    redirect_field_name ='clone_app/post_detail.html'
    form_class=PostForm
    model= Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    #where u should go it will not activate until u delete
    success_url =reverse_lazy('post_list')
    # go back to the home page


class DraftListView(LoginRequiredMixin,ListView):
    login_url ='/login/'
    redirect_field_name='clone_app/post_list.html'
    model=Post
# i neeed to make sure there is no date for publish
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')



#########################################################3
########################################

# one more for publishthe post
@login_required
def post_publish(request,pk):
    post= get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)




@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # here i link the comment to the post object
            comment.post =post
            comment.save()
            return redirect('post_detail',pk=post.pk)
        # some one has actuaaly field in the form
    else:
       form =CommentForm()
    return render (request,'clone_app/comments_form.html',{'form':form})


# for comment approved_comment
@login_required
def comment_approve(request,pk):
    comment =get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment= get_object_or_404(Comment,pk=pk)
# now you will delete the comment but u wont to save the pk for the post
    post_pk = comment.post.pk
    comment.delete()
    return  redirect('post_detail',pk=post_pk)
