from django import forms
from django.contrib.contenttypes import fields
from django.db import models
from django.forms import widgets

from members.models import Department, Members, Position, RegMember, Skill

from django.core.exceptions import ValidationError

class MemberAdminForm(forms.ModelForm):
    skill=forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),widget=forms.SelectMultiple(attrs={'multiple':True}))
    positions=forms.ModelMultipleChoiceField(queryset=Position.objects.all(),widget=forms.SelectMultiple(attrs={'multiple':True}))

    class Meta:
        model=Members
        fields='__all__'
        
    def save(self, commit=True):

        m = super(MemberAdminForm, self).save(commit=False)
        m.save()

    
        self.save_m2m()


        # print(m.positions.all())


        position=m.positions.first()

        m.priority=position.priority

        m.semesters=position.semesters


       

        if commit:
            m.save()

        return m 



class RegMemberForm(forms.ModelForm):
    skill=forms.ModelMultipleChoiceField(queryset=Skill.objects.all(),widget=forms.SelectMultiple({'multiple':True}))

    class Meta:
        model=RegMember
        fields='__all__'

    def clean_email(self):


        
        data = self.cleaned_data['email']
        qs=RegMember.objects.filter(email=data)
        if len(qs)==0:
            return data 
        else:
            raise ValidationError('This email address has already used')

        
            

        # if "fred@example.com" not in data:
        #     raise ValidationError("You have forgotten about Fred!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

        
        
'''
         {%if field.field.name == 'positions'%}
            <select class="" name="{{field.field.name}}" id="id_positions" multiple>
                <!-- members-position is context processor  -->
                {%for pos in members_positions%}
                <option value="{{pos.pk}}" {%if pos in original.positions.all%} selected {%endif%}>{{pos}}</option>
                {%endfor%}
            </select>

            {%endif%}


            {%if field.field.name == 'skill'%}
            <select class="" name="{{field.field.name}}" id="id_skill" multiple>
                <!-- members-position is context processor  -->
                {%for skill in skill_qs%}
                <option value="{{skill.pk}}" {%if pos in original.skill.all%} selected {%endif%}>{{skill}}</option>
                {%endfor%}
            </select>

            {%endif%}

'''