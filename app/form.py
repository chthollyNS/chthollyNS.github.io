from django import forms

class AddForm(forms.Form):
    username=forms.CharField(min_length=3,label='用户名')
    password=forms.CharField(min_length=3,label='密码')





# class AuthorForm(ModelFrom):
#     class Meta