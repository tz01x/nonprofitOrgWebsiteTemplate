
from django import forms
from django.db import models
from django.db.models import fields
from django.forms.widgets import TextInput

from .models import( BlogAndArticle, Comments,LastNews,Semester, WhyJoin)
class BlogAndArticleAdminForm(forms.ModelForm):
    # viewcount=forms.IntegerField(disabled=True,required=False,help_text='view count can\'t be alter ')
    class Meta:
        model=BlogAndArticle
        fields='__all__'
    
    def clean(self):
        cleaned_data = super(BlogAndArticleAdminForm,self).clean()

        category=cleaned_data.get("category")
        artical_t=cleaned_data.get('article_type')

        print(category,artical_t)
        if category is not None and category.article_type != artical_t :
            self.add_error('category','This Article Type does not match with category')

        

class LastNewsAdminForm(forms.ModelForm):
    # viewcount=forms.IntegerField(disabled=True,required=False,help_text='view count can\'t be alter ')
    class Meta:
        model=LastNews
        fields='__all__'


class SemesterAdminForm(forms.ModelForm):
    id=forms.IntegerField(widget=forms.HiddenInput,required=False)
    class Meta:
        model=Semester
        exclude=['prioritys_combain',]
    def clean(self):
        
        cleaned_data = super(SemesterAdminForm,self).clean()

        priority=cleaned_data.get("priority")
        semester_year=cleaned_data.get("semester_year")
        id=cleaned_data.get('id')
        if Semester.objects.filter(semester_year=semester_year,priority=priority).exclude(id=id).count()!=0:
            self.add_error('priority',f"not unique for {semester_year}")




class CreateCommentForm(forms.ModelForm):

    class Meta:
        model=Comments
        exclude=['replay']
    

    
class WhyJoinAdminForm(forms.ModelForm):
    reason=forms.CharField(widget=forms.Textarea(),help_text='Max character 500')
    class Meta:
        model=WhyJoin
        fields='__all__'