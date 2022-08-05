from core.models import ClubInfo, Semester, TermsAndCondition
from django.core.cache import cache
def get_all_semesters(request):

    semester_list=cache.get('semester_list')
    if semester_list is None:
        # print('semester list not cache ')
        semester_list=Semester.objects.all()
        
        cache.set('semester_list',semester_list)

    return {'semester_list':semester_list}

def get_club_info(request):

    clubinfo=cache.get('clubinfo')
    if clubinfo is None:
        try:
            clubinfo=ClubInfo.objects.get()
        
            cache.set('clubinfo',clubinfo)
        except:
            pass 

    return {'clubinfo':clubinfo}

def get_termsandcondition(request):

    termsandcondition=cache.get('termsandcondition')
    if termsandcondition is None:
        try:

            termsandcondition=TermsAndCondition.objects.get()
        
            cache.set('termsandcondition',termsandcondition.name)
        except:
            cache.set('termsandcondition',None) 

    return {'termsandcondition':termsandcondition}

