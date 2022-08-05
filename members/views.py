
from django.shortcuts import get_object_or_404, render
import os

from rest_framework import views

from core.models import Semester
from members.forms import RegMemberForm
from .models import ClubRoles, MemberViews, Members, Position

# def gen_data(semester,priority):
#     # pos=Position.objects.filter(semesters=semester,priority__id=priority)
#     # if pos.count()!=0:
#     #     yield (pos,pos.members_set.all())
#     # yield (None,None)

#     print(Position.objects.filter(semesters=semester,priority__id=priority).exists)
#     return None,None



def simpleMembersView(request,slug,clubyear_slug=None):
    
    view=get_object_or_404(MemberViews,slug=slug)
    

    curr_semester_slug=None
    if clubyear_slug is None:
        semester=Semester.objects.first()
    else:
        semester=get_object_or_404(Semester,slug=clubyear_slug)
    
    qs=None
    try:
        curr_semester_slug=semester.slug

        # for each postion for an specfic semester 
        qs = Position.objects.filter(semesters=semester,role__in=view.roles.all())

    except Exception as e:
        # print(e)
        # qs=None 
        pass 
         
    url_path='/members/'+view.slug+'/'
    return render(request=request,template_name='members/members.html',
                    context={
                        'objects':qs,
                        'current_semester':semester,
                        'semesters':Semester.objects.all(),
                        'title':view.title,
                        'current_slug':view.slug,
                        'url_active':'Governing Body',
                        'curr_semester_slug':curr_semester_slug,
                        'url_path':url_path,
                        
                        })



def alumni_view(request):
    title="Alumni"
    qs=Members.objects.filter(is_alumni=True).order_by('join_at')
    contex={
        'title':title,
        'objects':qs,
    }
    

    return render(request,'members/hallOfFame.html',contex)