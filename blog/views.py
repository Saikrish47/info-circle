# ***************for circular post ************
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, get_list_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView, View
# *******************for email notification **************
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.template import RequestContext
#*************************** for pdf *******************************
from django.template.loader import get_template
# from .utils import render_to_pdf
# *****************for models and forms*************************
from .models import Post, Comment, SignUp, Department, Catagory
from .forms import PostForm, CommentForm, SignUpForm, DepartmentForm, CatagoryForm

from itertools import chain






# post >>>>>>>>>
class AboutView(TemplateView):
    template_name = 'blog/about.html'

class PublicListView(ListView):
    model = Post
    fields = 'all'
    template_name = 'blog/public_list.html'

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class PostListView(ListView):
    model = Post
    fields = 'all'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    fields = 'all'
    template_name = 'blog/post_detail.html'



class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    # original
    success_url = reverse_lazy('post_list')

    form_class = PostForm
    model = Post
    #fields = 'all'



class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    # template_name = 'blog/post_detail.html'
    success_url = reverse_lazy('post_list')

    # redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = reverse_lazy('post_list')
    model = Post
    fields = 'all'


class DraftPostView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    # template_name = 'blog/post_draft_list.html'

    model = Post
    fields = 'all'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

    def get_queryset_a(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('-created_date')

class RegisterToggle(RedirectView):
    redirect_field_name = 'blog/post_detail.html'
    
    def get_redirect_url(request, pk):
        pk = self.kwargs.get("pk")
        
        obj = get_object_or_404(Post, pk=pk)
        # url_ = obj.get_absolute_url()
        user = request.user
        if user.is_authenticated():
            if user in obj.register.all():
                obj.register.remove(user)
            else:
                obj.register.add(user)
        # return url_
        return redirect('/post/<pk>', pk=post.pk)



###################################
###################################
def handler404(request,exception):
    return render(request, 'blog/404.html')

def error_500_view(request):
    return render(request,'blog/500.html')

def notfound(request, exception):
    return render(request,'blog/404.html')


# def notification(request):
#     if request.POST:
#         notification  = Post.object.filter(notification_user = request.post, notification_read = False)
#         staff_notification_read = Post.object.filter(notification_user = request_user.post, notification_read = True)

#         return{
#             'notification':notification,
#             'notification_read':notification_read
#         }
#     return Post.object.none()

@login_required
def public_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publisher()
    return redirect('/', pk=pk)


@login_required
def email_form(request):
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        email = form.save(commit = False)
        email.save()

        messages.success(request, 'Thank you , job done')
        return HttpResponseRedirect('/')

    return render(request,'blog/email_form.html',{'form':form })

@login_required
def department_form(request):
    form = DepartmentForm(request.POST or None)

    if form.is_valid():
        department = form.save(commit = False)
        department.save()

        messages.success(request, 'Thank you , job done')
        return HttpResponseRedirect('/')

    return render(request,'blog/department_form.html',{'form':form })

@login_required
def catagory_form(request):
    form = CatagoryForm(request.POST or None)

    if form.is_valid():
        catagory = form.save(commit = False)
        catagory.save()

       
        return HttpResponseRedirect('/')

    return render(request,'blog/catagory_form.html',{'form':form })


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # post.publish() previously mentioned here late modifed for email notify

    if post:
        post.publish()
        mail_qs = SignUp.objects.all().values('email')
        for mail in mail_qs:
            
            to = mail['email']
            print(to)
        subject = 'New Circular '
        message = 'new circular posted now checkout it out'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER,to,]

        send_mail(subject,message,from_email,to_list,fail_silently = True)
        # mail.send()
        # messages.success(request, 'Thank you , job done')
        return HttpResponseRedirect('/')
    return redirect('/', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post:
        post.delete()
        mail_qs = SignUp.objects.all().values('email')
        for mail in mail_qs:
            to = mail['email']
            print(to)
        subject = 'Circular Deleted '
        message = 'A Circular has been deleted'
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER,to,]

        send_mail(subject,message,from_email,to_list,fail_silently = True)
        # mail.send()
        # messages.success(request, 'Thank you , job done')
        return HttpResponseRedirect('/')
    return redirect('/', pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST or None)

   
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            comment.approve()
            return redirect('/', pk=comment.pk)

        else:
            form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

\


# purpose unknown>>>>>>>>>>>
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)



@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    # comment.delete()
    return redirect('/', pk=comment.pk)

# not in use>>>>>>>>>
