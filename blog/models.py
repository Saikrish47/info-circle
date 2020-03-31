from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.encoding import smart_str
from ckeditor_uploader.fields import RichTextUploadingField


class BlogPostQuerySet(models.QuerySet):

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(department__department_name__icontains=query) |
                    Q(catagory__catagory_name__icontains=query) 
                    # Q(user__username__icontains=query)
                    )

        return self.filter(lookup)


        # lookup = (
        #             Q(title__icontains=query) |
        #             Q(department__icontains=query) |
        #             Q(catagory_name__icontains=query) |
        #             Q(text__icontains=query)
                   
        #             )

        # return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)


    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)


class Department(models.Model):
    department_name = models.CharField(max_length=200)


    def __str__(self):
        return self.department_name
    
class Catagory(models.Model):
    catagory_name = models.CharField(max_length=200)


    def __str__(self):
        return self.catagory_name
    

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    department = models.ForeignKey('blog.Department',on_delete=models.CASCADE,blank=True, null=True)
    catagory = models.ForeignKey('blog.Catagory',on_delete=models.CASCADE,blank=True, null=True)

    title = models.CharField(max_length=200)
    text = RichTextUploadingField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    publish_date= models.DateTimeField(blank=True, null=True)

    objects = BlogPostManager()

    def publisher(self):
        self.publish_date = timezone.now()
        self.save()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)


    def get_absolute_url(self):
        # return f"/blog/post_detail{self.pk}"

        return reverse('blog/post_detail', kwargs = {'pk':self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    register = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='register')

    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

   

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog/post_detail', kwargs = {'pk':self.pk})
        # return f"/blog/post_list"

    def get_like_url(self):
        return reverse("blog/post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.author)

class SignUp(models.Model):

    email = models.EmailField()

    def __str__(self):
            return smart_str(self.email)
