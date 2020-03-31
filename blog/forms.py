from django import forms
from .models import Post, Comment ,SignUp, Department, Catagory
from django.conf import settings



class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
                                 attrs={'class':'speech-input', 'x-webkit-speech': 'x-webkit-speech'}))
  
    class Meta:
        model = Post
        fields = ('author','department','catagory', 'title', 'text',)

        widgets = {

          
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            # 'text': forms.Textarea(attrs={'class': 'editable medium-editor-texture postcontent'})

        }



class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(
                                 attrs={'class':'speech-input','x-webkit-speech': 'x-webkit-speech'}))
    class Meta:
        model = Comment
        # exclude = ['author']
        fields = ('text',)
        #
        widgets = {

            # 'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            # "text": forms.Textarea(attrs={'x-webkit-speech': 'x-webkit-speech'}),

        }

        labels = {
            "text":("Remarks")

        }



class SignUpForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
                                 attrs={'class':'speech-input','x-webkit-speech': 'x-webkit-speech'}))
    class Meta:
        model = SignUp
        fields = '__all__'

        widgets = {

            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'email': forms.TextInput(attrs={'class': 'textinputclass'}),

        }

class DepartmentForm(forms.ModelForm):
    department_name = forms.CharField(widget=forms.TextInput(
                                 attrs={'class':'speech-input','x-webkit-speech': 'x-webkit-speech'}))
    class Meta:
        model = Department
        fields = '__all__'

        widgets = {

            'department_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            

        }
        labels = {
            "department_name":("Department")

        }

class CatagoryForm(forms.ModelForm):
    catagory_name = forms.CharField(widget=forms.TextInput(
                                 attrs={'class':'speech-input','x-webkit-speech': 'x-webkit-speech'}))
    class Meta:
        model = Catagory
        fields = '__all__'

        widgets = {

            'catagory_name': forms.TextInput(attrs={'class': 'textinputclass'}),
            

        }
        labels = {
            "catagory_name":("Catogory")

        }
