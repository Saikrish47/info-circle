from django.contrib import admin
from blog.models import Post,Comment,SignUp,Department,Catagory
from import_export import resources

from import_export.admin import ImportExportModelAdmin


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment


class CommentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resources_class = CommentResource
    search_fields = ['author','post__title','post__id',]

    list_display = ['author','post',]






# Register your models here.
admin.site.register(Comment,CommentAdmin)

admin.site.register(SignUp)

admin.site.register(Post)

admin.site.register(Department)

admin.site.register(Catagory)
