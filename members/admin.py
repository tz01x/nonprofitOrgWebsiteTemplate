from datetime import datetime
from django import forms
from django.contrib import admin
from django.contrib.admin.decorators import action
from django.core.checks import messages
from django_summernote.admin import SummernoteModelAdmin
from django.http.response import HttpResponseRedirect
from django.utils.html import format_html

from django.utils.safestring import  mark_safe

from django.shortcuts import redirect, render,get_object_or_404
from core.send_mail import SendMail
from members.forms import MemberAdminForm, RegMemberForm
# Register your models here.
from .models import *
from csvexport.actions import csvexport

def broadcast_email(self,request,qs):


    # All requests here will actually be of type POST 
    # so we will need to check for our special key 'apply' 
    # rather than the actual request type
    # print(request.POST)
    if 'apply' in request.POST:
        # The user clicked submit on the intermediate form.
        # Perform our update action:

        subject=request.POST.get('email_subject','')
        body=mark_safe( request.POST.get('email_body',''))


        qs=qs.exclude(email=None)
        
        SendMail().sendorBrodcast_WithoutTemplate(request=request,to=list(qs.values_list('email', flat=True)),subject=subject,email_body=body)
        
        # Redirect to our admin view after our update has 
        # completed with a nice little info message saying 
        # our models have been updated:
        self.message_user(request,
                            "email send {} ".format(qs.count()))


        return HttpResponseRedirect(request.get_full_path())


    return render(request,
                    'members/admin/reg_member_intermediate.html',
                    context={'orders':qs,'get_back_url':request.get_full_path(),'form':EmailForm()})


# admin.site.register(P)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass 

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass 


@admin.register(MemberHierarchyLevel)
class MemberHierarchyLevelAdmin(admin.ModelAdmin):
    pass 




@admin.register(ClubRoles)
class ClubRolesAdmin(admin.ModelAdmin):
    pass 

@admin.register(MemberViews)
class MemberViewsAdmin(admin.ModelAdmin):
    # exclude=['slug'] 
    pass 


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass 


@admin.register(Members)
class MembersAdmin(SummernoteModelAdmin):
    list_filter=['created','is_alumni','priority','semesters','skill','bloodGroup']
    search_fields=('name','university_id','department','email')
    actions=(broadcast_email,)


    list_display=('__str__','priority','semesters','created')

    
    readonly_fields=('preview_picture','priority','semesters',)

    form=MemberAdminForm
    change_form_template = 'members/admin/change_form.html'

    # def __init__(self ,*arg,**kwargs):
    #     super(MembersAdmin,self).__init__(*arg,**kwargs)

    #     self.actions=[]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}
        extra["skill_qs"] = Skill.objects.all()

        return super(MembersAdmin, self).change_view(request, object_id,
                        form_url, extra_context=extra)

    # def changelist_view(self, request, extra_context=None):
    #     response = super(MembersAdmin, self).changelist_view(request, extra_context)
    #     extra_context = {
    #         'myvar': 'whateveryouwant'
    #     }
    #     try:
    #         response.context_data.update(extra_context)
    #     except Exception as e:
    #         pass
    #     return response

from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

class EmailForm(forms.Form):
    email_subject=forms.CharField(max_length=1000)
    email_body = SummernoteTextFormField()


@admin.register(RegMember)
class RegMemberAdmin(admin.ModelAdmin):

    list_filter=['joined','created','department','skill','bloodGroup',]
    search_fields=('name','university_id','email')


   

    form=RegMemberForm

    readonly_fields=['university_id','bloodGroup','department','picture','preview_picture','name','phone','email','bloodGroup','skill','facebook_profile_url','linkin_url']
    list_display=['__str__','email','preview_picture','joined']
    actions=['add_AS_Member',csvexport,broadcast_email]

    def add_AS_Member(self,request,qs):
        qs=qs.filter(joined=False)

        for reg_u in qs:
            reg_u.joined=True

            reg_u.save()

            obj=Members(**reg_u.serilize())
            obj.join_at=datetime.now()
            obj.save()
            obj.skill.set(reg_u.skill.all())
            
        self.message_user(request,
                            "{} members added".format(qs.count()))

    


        

        
            
        
    

    
