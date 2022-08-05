import uuid
from django.db import models
from django.db.models.base import Model
from django.utils.html import format_html
from django.utils.text import slugify
from core.models import ImageUploderPath, Semester

from django.dispatch import receiver
from .slugify import unique_slug_generator


# Create your models here.
class MemberHierarchyLevel(models.Model):
    priority=models.SmallIntegerField(verbose_name='Priority of Current Roles',help_text='smaller the number is the higer the priority gets',)
    name=models.CharField(max_length=500,verbose_name='Level name')
    class Meta:
        ordering=['priority']
        verbose_name=" Member HierarchyLevel"
    def __str__(self) -> str:
        return self.name.capitalize()

class ClubRoles(models.Model):
    title=models.CharField(max_length=500,verbose_name='Title of Club Roles & Responsibilities')

    class Meta:
        verbose_name=' Club Roles & Responsibilities'

    

    def __str__(self) :
        return self.title.capitalize()

class MemberViews(models.Model):
    slug=models.SlugField(max_length=255, blank=True,null=True,unique=True,db_index=True,help_text='Don\'t need to fill this, because this field will be automatically generate')
    title=models.CharField(max_length=250,verbose_name='Page title')
    roles=models.ManyToManyField(to=ClubRoles,verbose_name='Which which member in selected roles will be will be showen in the the page.')
    class Meta:
        verbose_name='Members view'

    def __str__(self) :
        return self.title.capitalize()
    def save(self, *args,**kwargs):
        if self.slug is None:
            self.slug=slugify(str(self.title).lower()+str((uuid.uuid1(4)))[0:8],allow_unicode=False)
        return super(MemberViews,self).save(*args,**kwargs)


@receiver(models.signals.pre_save, sender=MemberViews)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

class Position(models.Model):
    role=models.ForeignKey(to=ClubRoles,null=True,on_delete=models.SET_NULL,related_name='members',db_index=True)

    priority=models.ForeignKey(to=MemberHierarchyLevel,on_delete=models.RESTRICT,verbose_name='HierarchyLevel')
    semesters=models.ForeignKey(to=Semester,on_delete=models.RESTRICT,verbose_name='Club year',db_index=True)

    class Meta:
        ordering=['semesters','priority']
        verbose_name=" Position"

    def __str__(self) -> str:
        return f'{self.role} ({self.priority}) ({self.semesters})'

bloodGroopChoices=(
    ('A (+ve)','A (+ve)'),
    ('A (-ve)','A (-ve)'),
    ('AB (+ve)','AB (+ve)'),
    ('AB (-ve)','AB (-ve)'),
    ('B (+ve)','B (+ve)'),
    ('B (-ve)','B (-ve)'),
    ('O (+ve)','O (+ve)'),
    ('O (-ve)','O (-ve)'),

    )

class Skill(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    
class Department(models.Model):
    dept_name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.dept_name

    

class Members(models.Model):
    name=models.CharField(max_length=500,verbose_name='Member Full name')
    is_alumni=models.BooleanField(default=False)
    discription=models.TextField(blank=True,null=True,verbose_name="Description")

    university_id=models.CharField(max_length=20,null=True,blank=True)
    department=models.ForeignKey(to=Department,on_delete=models.SET_NULL,null=True)

    email=models.EmailField(max_length=500)
    phone=models.CharField(max_length=11,verbose_name='phoneNumber',blank=True,null=True)

    bloodGroup=models.CharField(max_length=10,choices=bloodGroopChoices,default='unknown')
    skill=models.ManyToManyField(to=Skill,related_name='members')


    facebook_profile_url=models.URLField(max_length=500,null=True,blank=True)
    linkin_url=models.URLField(max_length=500,null=True,blank=True)
    portfolio_url=models.URLField(max_length=500,null=True,blank=True)

    priority=models.ForeignKey(to=MemberHierarchyLevel,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="HierarchyLevel")
    semesters=models.ForeignKey(to=Semester,related_name='current_members',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='Club Year')

    positions=models.ManyToManyField(to=Position)

    picture = models.ImageField(verbose_name='Member picture  (1:1 ratio is recommended)',
                             upload_to=ImageUploderPath('members/').uploadTo, null=True, blank=True)
    created=models.DateField(blank=True,null=True,db_index=True,auto_now_add=True)
    join_at=models.DateField(verbose_name='Joined Date')




    class Meta:
        ordering=['semesters','priority']
        verbose_name='Member'

    def __str__(self) -> str:
        return f'{self.name.title()}'
    
    def name_slugify(self):
        return slugify(self.name)

    def save(self):
        super(Members,self).save()

    def preview_picture(self):
        _html=""
        try:
            _html=f"<img src='{self.picture.url}' style='width:100px;'  atr='pic'/>"
        except:
            pass
        return format_html(_html)

    def delete(self, using=None, keep_parents=False):
        try:

            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)
        except:
            pass 

        super().delete()

        
    preview_picture.short_description = 'Member Picture (Preview)'
        

        # try:
        #     position=self.positions.all().first()
        #     if(position):
        #         print(position)
        #         self.priority=position.priority
        #         self.semesters=position.semesters
        # except:
        #     print('[exception] Exception found in saved method in Members class')

        # return super(Members,self).save() 

        

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# @receiver(post_save, sender=Members)
# def save_member(sender, instance,**kwargs) :
#     try:
#         position=instance.positions.all().first()
#         if(position):
            
#             instance.priority=position.priority
#             instance.semesters=position.semesters

#             print(position)
#     except:
#         print('[exception] Exception found in saved method in Members class') 

    




class RegMember(models.Model):

    name=models.CharField(max_length=500,verbose_name='Member Full name')
    university_id=models.CharField(max_length=20)
    department=models.ForeignKey(to=Department,on_delete=models.RESTRICT,related_name='reg_member')

    
    phone=models.CharField(max_length=11,verbose_name='phoneNumber')

    bloodGroup=models.CharField(max_length=10,choices=bloodGroopChoices,default='unknown')
    skill=models.ManyToManyField(to=Skill,related_name='reg_members')

    email=models.EmailField(max_length=150)
    facebook_profile_url=models.URLField(max_length=150,null=True,blank=True)
    linkin_url=models.URLField(max_length=150,null=True,blank=True)
    portfolio_url=models.URLField(max_length=500,null=True,blank=True)

    picture = models.ImageField(verbose_name='Member picture (1:1 ratio is recommended)',
                             upload_to=ImageUploderPath('members/').uploadTo, null=True, blank=True)

    # cv = models.FileField(upload_to="")                         
    created=models.DateField(auto_now=True)
    joined=models.BooleanField(default=False)

    class Meta:
        ordering=['-created']

        verbose_name="Newly Register Members"

    def __str__(self) -> str:
        return self.name

    def serilize(self):
        return{
            'name':self.name,
            'university_id':self.university_id,
            'department':self.department,
            'bloodGroup':self.bloodGroup,
            'phone':self.phone,
            'email':self.email,
            'facebook_profile_url':self.facebook_profile_url,
            'linkin_url':self.linkin_url,
            'picture':self.picture,
        }
    
    def preview_picture(self):
        _html=''
        try:

            _html=f"<img src='{self.picture.url}' style='width:100px;'  atr='pic'/>"
        except:
            pass 

        return format_html(_html)


    preview_picture.short_description = 'Member Picture (Preview)'


    def delete(self, using=None, keep_parents=False):
        try:
            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)

        except:
            pass 

        super().delete()




