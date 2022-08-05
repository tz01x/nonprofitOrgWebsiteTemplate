from .models import MemberViews, Position
from core.models import Semester
from django.core.cache import cache
def get_related_pages_of_members(request):
    
    member_views=cache.get('member_views')
    if member_views is None:
        member_views=MemberViews.objects.all()
        cache.set('member_views',member_views)

    return {'member_views':member_views}



def get_members_positions(request):
    
    members_positions=cache.get('members_positions')
    if members_positions is None:
        members_positions=Position.objects.all()
        cache.set('members_positions',members_positions)

    return {'members_positions':members_positions}
