from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


# Create your models here.

class Post(models.Model):
     author_post = models.ForeignKey('auth.User')
     title = models.CharField(max_length=200)
     text = models.TextField()
     create_date = models.DateTimeField(default = timezone.now())
     # blank required it will show a message /null it means it allow to be empty
     published_date = models.DateTimeField(blank=True, null=True)
#it is different it refer to the time right now
     def publish(self):
         self.published_date = timezone.now()
         self.save()

     def approve_comments(self):
         # i will have a comment: var that i will filter them
        return self.comments.filter(approved_comment=True)
#
#django look for this  when somebody commit the name is reserve
     def get_absolute_url(self):
#go to this page after u commit with pk that equal to the post u made link page with postS
         return reverse("post_detail", kwargs={'pk':self.pk})

     def __str__(self):
        return self.title



# comments models
class Comment(models.Model):
    # how to connect each comment with post
    #related_name:reserved word (m2m)and ForeignKey relation starting from the (model,related_name)
    post = models.ForeignKey('clone_app.Post',related_name='comments')
    author_comments= models .CharField(max_length=200)
    text= models.TextField()
    create_date = models.DateTimeField(default =timezone.now())
    approved_comment= models.BooleanField(default=False)


    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        # it tell the web page wher to go next
# if u make commit i will take u to the list comments page
        return reverse('post_list')

    def __str__(self):
       return self.text
