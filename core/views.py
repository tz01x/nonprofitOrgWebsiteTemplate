from datetime import timedelta
from re import A

from django.core.checks import messages
from django.http.response import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render,get_object_or_404
from django.urls.base import reverse
from core.forms import CreateCommentForm
from core.send_mail import SendMail
from core.serializer import EventSerializer
from members.forms import RegMemberForm
from django.db.models import F,Count
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hitcount.views import HitCountDetailView

from members.models import MemberViews
from .models import (ARTICLE_TYPE, Announcement, Category, ClubEvent, 
                    ClubInfo,BlogAndArticle, Comments, 
                    GetinTouch, Images,
                    LastNews,Affiliates,
                    NewsLetter, Semester, 
                    TermsAndCondition, WhatWedid, 
                    WhyJoin)
from .utils.testingRatelimiter import ratelimit
# from ratelimit.decorators import ratelimit
from .utils.blacklist_ratelimited import blacklist_ratelimited
# import ratelimit

# Create your views here.

class CreateCommentOption:
    EVENTS="EVENTS"
    BLOGS="BLOGS"

def testview(request):
    qs=BlogAndArticle.objects.all()
    return render(request,'core\Latest Blog.html',{'object_list':qs})
    
def termsAndConditions(request):
    object=TermsAndCondition.objects.get()

    return render(request,
        'TermsAndConditions.html',
        {
            'object':object,

        })

@ratelimit(key='ip', rate='100/m', block=False)
@blacklist_ratelimited(timedelta(minutes=30))
def createComment(request,commentFor,slug):


    if request.method!='POST':
        return  redirect('core:index')

    obj=None
    if commentFor==CreateCommentOption.EVENTS:
        obj=get_object_or_404(ClubEvent,slug=slug)
    elif commentFor==CreateCommentOption.BLOGS:
        obj=get_object_or_404(BlogAndArticle,slug=slug)
    
    if obj is None:
        return Http404()

    form = CreateCommentForm(request.POST)

    if form.is_valid():
        comment=form.save()
        obj.comments.add(comment)
    
    if 'next' in request.POST:
        return redirect(request.POST.get('next','core:index'))
    else:
        return redirect('core:index')
    
@ratelimit(key='ip', rate='100/m', block=False)
@blacklist_ratelimited(timedelta(minutes=30))
def addReplay(request,pk):

    if request.method !='POST':
        return HttpResponseBadRequest()

    obj=get_object_or_404(Comments,pk=pk)

    form= CreateCommentForm(request.POST)
    if form.is_valid():
        new_obj=form.save()
        obj.replay.add(new_obj)
        obj.save()
    return redirect(request.POST.get('next','core:index'))


        


    
    



@ratelimit(key='ip', rate='100/m', block=False)
@blacklist_ratelimited(timedelta(minutes=30))
def subscribeToNewsLetter(request):



    if request.method=='POST' and 'next' in request.POST and 'email' in request.POST:

        email=request.POST.get('email',None)

        if email:
            NewsLetter.objects.create(email=email)

        return redirect(request.POST.get('next','core:index'))
    return redirect('core:index')



# @ratelimit(key='user_or_ip', rate='50/m', block=False)
# @blacklist_ratelimited(timedelta(minutes=30))       
def getintouch(request):

    if request.method == 'POST' and 'fullname' in  request.POST and 'email' in request.POST and 'discription' in request.POST:
        try:
            GetinTouch.objects.create(
                fullname=request.POST.get('fullname',''),
                email=request.POST.get('email',''),
                discription=request.POST.get('discription',''),
            )
          


        except:
            pass 

    return redirect('core:index')






def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@cache_page(60 * 2)
def index(request):
    
    blogsAndarticles=BlogAndArticle.objects.filter(
            article_type=ARTICLE_TYPE.get_types().get('article')
        ).order_by('-created')[:5]

    # lastnews=LastNews.objects.all().order_by('-created')[:5]
    lastnews=Announcement.objects.all()[:5]
    affiliates=Affiliates.objects.all()
    whyjoins=WhyJoin.objects.all()

    whatwedid=WhatWedid.objects.all()

    events=ClubEvent.objects.values('id','slug',
        'title','picture',
        'created').order_by('-created')[:5]

    


    context={
       
        'blogsAndarticles':blogsAndarticles,
        'lastnews':lastnews,
        'affiliates':affiliates,
        'whyjoins':whyjoins,
        'whatwedid':whatwedid,
        'events':events,
        
    }
    
    return render(request,template_name='./core/index.html',context=context)

@ratelimit(key='ip', rate='100/m', block=False)
@blacklist_ratelimited(timedelta(minutes=30))
def signup_page(request):
    form=RegMemberForm()

    club=ClubInfo.objects.get()
    if request.method=='POST' and club.registation_form_open:
        form=RegMemberForm(request.POST,request.FILES)
        if(form.is_valid()):
            obj=form.save()
            SendMail().sendorBrodcast_WithTemplate(request,obj.email,f'[{club.name}]Registration has complect','reg_complect_email.html',{'username':obj.name,'clubname':club.name})

            return redirect('core:reg_complect')
            
        
    context={
        'form':form,

    }
    
    return render(request,template_name='./core/signup.html',context=context)

def reg_complect(request):
    return render(request,'core/reg_complect.html')

def articles_and_publication(request,article_t):
    page = request.GET.get('page', 1)
    category=request.GET.get('catagory')
    title=request.GET.get('title')
    object_list=BlogAndArticle.objects.filter(article_type=article_t).order_by('-created')
    if category is not None:
        object_list=BlogAndArticle.objects.filter(category__name__startswith=category)
    if title is not None:
        object_list=BlogAndArticle.objects.filter(title__icontains=title)
    popular_obj=object_list.order_by('-hit_count_generic__hits').first()
    # one to may relation
    categorys=Category.objects.filter(article_type=article_t).annotate(num_of_blogandarticle=Count('blogandarticle'))
    paginator = Paginator(object_list, 12)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    ctx={
        'object_list':object_list,
        'popular_obj':popular_obj,
        'categorys':categorys
    }
    return ctx
    # print(popular_obj)
    # return render(request,template_name='core/article_list.html',context=ctx)

def publication(request):
    article_t=ARTICLE_TYPE.get_types().get('publication')
    ctx=articles_and_publication(request,article_t)
    ctx={
        **ctx,
        'banner_title':'Publication'
    }
    return render(request,template_name='core/article_list.html',context=ctx)

def articles(request):
    article_t=ARTICLE_TYPE.get_types().get('article')
    ctx=articles_and_publication(request,article_t)
    ctx={
        **ctx,
        'banner_title':'Article'
    }
    return render(request,template_name='core/article_list.html',context=ctx)

class BlogAndArticleDetails(HitCountDetailView):
    model = BlogAndArticle
    context_object_name = "object"
    # template_name = "./core/activityDtails.html"
    template_name = "./core/blog-details.html"
    count_hit = True

    def get_object(self):
        slug = self.kwargs.get("slug")
        
        return get_object_or_404(
            BlogAndArticle,
            slug=slug,
        )
    def get_context_data(self, **kwargs):
        context = super(BlogAndArticleDetails, self).get_context_data(**kwargs)
        obj=self.get_object()

        createComment_url=reverse('core:createComment',kwargs={'commentFor':CreateCommentOption.BLOGS,'slug':self.kwargs.get("slug")})
        # categorys=Category.objects.filter(article_type=obj.article_type).annotate(num_of_blogandarticle=Count('blogandarticle'))
        
        similar_object=BlogAndArticle.objects.filter(article_type=obj.article_type,category= obj.category).exclude(id=obj.id)[:3]
        
        banner_title="Article/Details"
        url_active='article'

        for t in ARTICLE_TYPE.get_types():
            if ARTICLE_TYPE.get_types()[t]==obj.article_type:
                banner_title=t.capitalize()+"/Details"
                url_active=t
                break
        

        
        context.update({
        # 'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        'createComment_url':createComment_url,
        # 'categorys':categorys,
        'similar_object':similar_object,
        'banner_title':banner_title,
        'url_active':url_active
        })
        return context



def gallaryView(request,curr_semester_slug=None):
    imgs=Images.objects.all()
    semesters=Semester.objects.all()
    
    if curr_semester_slug is None:
        try:
            curr_semester_slug=semesters.first().slug
        except :
            curr_semester_slug=None
    ctx={
        'imagesList':imgs,
        'semesters':semesters,
        'curr_semester_slug':curr_semester_slug,
    }
    return render(request,template_name='./core/gallery.html',context=ctx)

# https://www.figma.com/file/8JmADeuWZkLSmlF2L2vG4h/Betel-Leaf-RACEWU?node-id=105%3A19

class EventDetails(HitCountDetailView):

    model = ClubEvent
    context_object_name = "object"
    template_name = "./core/activityDtails.html"
    count_hit = True

    def get_object(self):
        
        slug = self.kwargs.get("slug")
        
        return get_object_or_404(
            ClubEvent,
       
            slug=slug
        )
    def get_context_data(self, **kwargs):
        context = super(EventDetails, self).get_context_data(**kwargs)
        createComment_url=reverse('core:createComment',kwargs={'commentFor':CreateCommentOption.EVENTS,'slug':self.kwargs.get("slug")})

        context.update({
        # 'popular_obj': ClubEvent.objects.order_by('-hit_count_generic__hits').first(),
        'createComment_url':createComment_url,
        'url_active':'event',
        'banner_title':'Events/Details',
        'url_active':'event',

        })

        return context

def eventView(request,slug):

    
    semester=get_object_or_404(Semester,slug=slug)
    object_list=ClubEvent.objects.filter(semester=semester).order_by('-created')

    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 10)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    ctx={
        
        'url_active':'event',
        'activitys_name':f'Events from '+semester.readable_name,
        'object_list':object_list,
        'popular_obj': ClubEvent.objects.order_by('-hit_count_generic__hits').first(),
    }
    return render(request=request,template_name='./core/events.html/',context=ctx)



def newsListView(request):

   
    object_list= LastNews.objects.all().order_by('-created')


    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 10)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    ctx={
        'banner_title':'News',
        'url_active':'news',
        'activitys_name':f'News',
        'object_list':object_list,
        'popular_obj': LastNews.objects.order_by('-hit_count_generic__hits').first(),
    }
    return render(request=request,template_name='./core/news.html/',context=ctx)

class NewsDetailsView(HitCountDetailView):

    model = LastNews
    context_object_name = "object"
    template_name = "./core/activityDtails.html"
    count_hit = True

    def get_object(self):
        
        slug = self.kwargs.get("slug")
        
        return get_object_or_404(
            LastNews,
       
            slug=slug
        )
    def get_context_data(self, **kwargs):
        context = super(NewsDetailsView, self).get_context_data(**kwargs)
        # createComment_url=reverse('core:createComment',kwargs={'commentFor':CreateCommentOption.EVENTS,'slug':self.kwargs.get("slug")})
        similar_object=LastNews.objects.filter().exclude(slug=self.kwargs.get('slug'))[:3]
        context.update({
        # 'popular_obj': ClubEvent.objects.order_by('-hit_count_generic__hits').first(),
        # 'createComment_url':createComment_url,
        'url_active':'news',
        'banner_title':'News/Details',
        'similar_object':similar_object
        

        })

        return context

    
# api view

from rest_framework import generics
from rest_framework.permissions import AllowAny

class GalleryListAPIView(generics.ListAPIView):
    # PAGE_SIZE is 20 ; config from settings.py 
    # queryset = ClubEvent.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        curr_semester_slug=self.kwargs.get('curr_semester_slug')
        if curr_semester_slug is None:
            curr_semester_slug=Semester.objects.first().slug
        
        queryset = ClubEvent.objects.filter(semester__slug=curr_semester_slug).order_by('-date') 
        return queryset

    # def get_context_data(self,**kwargs):
    #     context= super(GalleryListAPIView,self).get_context_data(**kwargs)
    #     semesters=Semester.objects.all()
    #     context.update({
    #         'semesters':semesters
    #     }) 
    #     return context


def csrf_failure(request,reason=""):
    ctx = {'message': 'please re-enable cookie in you brower'}
    return render(request,'403_csrf_failer.html', ctx)

    
