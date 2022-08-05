
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models.fields import related
from django.urls import reverse
from django.db import models
import os
import uuid
import re
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import format_html, html_safe
from solo.models import SingletonModel
from hitcount.models import HitCountMixin, HitCount
from colorfield.fields import ColorField
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .slugify import unique_slug_generator, unique_slug_generator_with_readable_name
import logging

from django.utils.text import slugify


class ARTICLE_TYPE:
    _types = {
        'article': 'a',
        'publication': 'p'
    }

    @classmethod
    def choices(cls):
        t = []
        for key in cls._types:
            t.append([cls._types[key], key])
        return t

    @classmethod
    def get_types(cls):
        return cls._types

    @classmethod
    def get_key_form_value(cls, val):
        t = {}
        for key in cls._types:
            if cls._types[key] == val:
                return key
        return None


def preview_image_tag(picture):
    _html = ''
    try:
        width = 100
        _html = f"<img src='{picture.url}' style='width:{width}px;'  atr='pic'/>"
    except:
        pass
    return format_html(_html)


class Comments(models.Model):

    username = models.CharField(max_length=500)
    email = models.EmailField()
    message = models.TextField(max_length=1000)
    replay = models.ManyToManyField(to='Comments')

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.username+f" ( {self.message[0:20]}..... ) "

    class Meta:
        verbose_name = 'Comment'


class NewsLetter(models.Model):
    email = models.EmailField()

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Newsletter'


class WhatWedid(models.Model):
    youtube_link = models.URLField(
        blank=True, null=True, verbose_name='Youtube video link')
    title = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.title

    def youtube_link_embed(self):
        if self.youtube_link:
            try:

                txt = self.youtube_link
                x = re.search("v=.{11}", txt)
                if x:
                    return txt[x.start()+2:x.start()+13]
                else:
                    return txt[-11:]
            except:
                return None

        return None

    class Meta:
        verbose_name = "What We Did"


class ImageUploderPath():
    def __init__(self, img_upload_path) -> None:
        self.img_upload_path = img_upload_path

    def uploadTo(self, instance, filename):
        base, ext = os.path.splitext(filename)
        filename = "%s.%s" % (uuid.uuid4(), ext[1:])
        return os.path.join(self.img_upload_path, filename)

    def uploadTo_withBasefile(self, instance, filename):
        base, ext = os.path.splitext(filename)
        filename = "%s_%s.%s" % (base, uuid.uuid4(), ext[1:])
        return os.path.join(self.img_upload_path, filename)


class ClubInfo(SingletonModel):

    # basic info
    name = models.CharField(max_length=500, verbose_name='Club  full name')
    sort_name = models.CharField(
        max_length=100, verbose_name='Club  sort name')
    email = models.EmailField()
    address = models.CharField(max_length=200)
    google_map_link = models.URLField(
        max_length=200, default=None, null=True, blank=True)

    # meta tags for seo
    meta_title = models.CharField(
        max_length=150, help_text='Keep your title length around 60 characters')
    meta_description = models.CharField(
        max_length=250, help_text="Keep it around 160 characters. ")

    description = models.TextField(verbose_name='club description')
    sort_description_for_footer = models.TextField(
        verbose_name='sort description for footer')

    registation_form_open = models.BooleanField(default=True)

    current_member = models.IntegerField(
        verbose_name=' Current Members ', default=0)
    alumni = models.IntegerField(verbose_name=' Alumni ', default=0)
    advisors = models.IntegerField(verbose_name=' Advisors ', default=0)
    # advisors = models.IntegerField(verbose_name=' Advisors ', default=0)

    # socal links

    faebook_url = models.URLField(
        blank=True, null=True, verbose_name="facebook url")
    twitter_url = models.URLField(blank=True, null=True)
    linkend_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    # images

    logo = models.ImageField(verbose_name='Logo main (1:1  ratio is recommended)',
                             upload_to=ImageUploderPath('club_logo/').uploadTo, null=True, blank=True)

    logo_2 = models.ImageField(verbose_name='Logo 2 (1:1  ratio is recommended)',
                               upload_to=ImageUploderPath('club_logo/').uploadTo, null=True, blank=True)

    logo_3 = models.ImageField(verbose_name='Logo 3 (1:1  ratio is recommended)',
                               upload_to=ImageUploderPath('club_logo/').uploadTo, null=True, blank=True)

    landing_picture = models.ImageField(verbose_name='landing  picture 1 (210:71 ratio is recommended) ',
                                        upload_to=ImageUploderPath('landing_picture/').uploadTo, null=True, blank=True)
    landing_picture_two = models.ImageField(verbose_name='landing  picture 2 (210:71 ratio is recommended) ',
                                            upload_to=ImageUploderPath('landing_picture/').uploadTo, null=True, blank=True)
    landing_picture_three = models.ImageField(verbose_name='landing  picture 3 (210:71 ratio is recommended) ',
                                              upload_to=ImageUploderPath('landing_picture/').uploadTo, null=True, blank=True)
    landing_picture_four = models.ImageField(verbose_name='landing  picture 4 (210:71 ratio is recommended) ',
                                             upload_to=ImageUploderPath('landing_picture/').uploadTo, null=True, blank=True)
    landing_picture_five = models.ImageField(verbose_name='landing  picture 5 (210:71 ratio is recommended) ',
                                             upload_to=ImageUploderPath('landing_picture/').uploadTo, null=True, blank=True)

    # theam
    font_links = models.CharField(
        max_length=500, default='<link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@500&display=swap" rel="stylesheet">')
    font_family = models.CharField(
        max_length=100, help_text="Example: 'Open Sans', sans-serif", default="'Open Sans', sans-serif")
    primary_color = ColorField(default='#ED1C24', format='hexa')
    text_p_color = ColorField(default='#FFFFFFFF', format='hexa',
                              verbose_name='text color inside primary color  ')
    primary_lite_color = ColorField(default='#ef3f3f', format='hexa')
    primary_dark_color = ColorField(default='#a50c12', format='hexa')
    secondary_color = ColorField(default='#1C75BC', format='hexa')
    secondary_lite_color = ColorField(default='#1C75BC', format='hexa')
    secondary_dark_color = ColorField(default='#1C75BC', format='hexa')
    text_s_color = ColorField(default='#FFFFFFFF', format='hexa',
                              verbose_name='text color inside secondary colors ')

    gray_color = ColorField(default='#3E3E3E', format='hexa')
    footer_bg_color = ColorField(default='#FF0000', format='hexa')
    footer_text_color = ColorField(default='#3E3E3E', format='hexa')
    footer_text_hover_color = ColorField(default='#3E3E3E', format='hexa')

    def get_font_links(self):
        try:
            return format_html(self.font_links)
        except:
            return ""

    def loadtheam(self):
        _html = '<style>:root {'+f'''
            --primary_liter:{self.primary_lite_color}!important;
            --text_in_primary:{self.text_p_color} !important;
            --primary: {self.primary_color} !important; 
            --primary_darker:{self.primary_dark_color} !important; 
            --secondary: {self.secondary_color} !important;
            --secondary_liter: {self.secondary_lite_color} !important;
            --secondary_darker: {self.secondary_dark_color} !important;
            --text_in_secondary:{self.text_s_color}!important;
            --gray: {self.gray_color} !important;
            --footer_bg:{self.footer_bg_color} !important;
            --footer_text:{self.footer_text_color} !important;
            --footer_text_hover:{self.footer_text_hover_color} !important;
            --font_family: {self.font_family};
            '''+'}</style>'

        return _html

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):

        pics = [self.logo, self.logo_2, self.logo_3,
                self.landing_picture, self.landing_picture_two,
                self.landing_picture_three, self.landing_picture_four,
                self.landing_picture_five]

        for pic in pics:

            if pic in None:
                continue

            try:
                storage = pic.storage

                if storage.exists(pic.name):
                    storage.delete(pic.name)
            except Exception as e:
                logging.ERROR(e)
                pass

        super().delete()

    def logo_preview(self):
        return preview_image_tag(self.logo)

    def logo_2_preview(self):
        return preview_image_tag(self.logo_2)

    def logo_3_preview(self):
        return preview_image_tag(self.logo_3)

    def landing_picture_preview(self):
        return preview_image_tag(self.landing_picture)

    def landing_picture_2_preview(self):
        return preview_image_tag(self.landing_picture_two)

    def landing_picture_3_preview(self):
        return preview_image_tag(self.landing_picture_three)

    def landing_picture_4_preview(self):
        return preview_image_tag(self.landing_picture_four)

    def landing_picture_5_preview(self):
        return preview_image_tag(self.landing_picture_five)

    def get_all_landing_pictures(self):
        nullable_pic = [self.landing_picture, self.landing_picture_two,
                        self.landing_picture_three, self.landing_picture_four,
                        self.landing_picture_four]

        pic = []
        for npic in nullable_pic:
            if npic:
                pic.append(npic)

        return pic

    class Meta:
        verbose_name = "**SITE CONFIG**"


class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    slug = models.SlugField(max_length=255, blank=True,
                            null=True, unique=True, db_index=True,
                            help_text='Don\'t need to fill this, because this field will be automatically generate')

    content = models.TextField(max_length=400,help_text="max charecter length is 400")
    picture = models.ImageField(verbose_name='Picture  ( 1:1 ratio is recommended)', upload_to=ImageUploderPath(
        'announcement/').uploadTo, null=True, blank=True)
    created = models.DateField(
        auto_now=False, auto_now_add=True, db_index=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(str(self.title).lower()+"-" +
                                str((uuid.uuid1(4)))[0:8], allow_unicode=False)
        return super(Announcement, self).save(*args, **kwargs)


    class Meta:
        ordering=['-created']
        verbose_name = "Latest News"
        verbose_name_plural = "Latest News"

class LastNews(models.Model, HitCountMixin):
    title = models.CharField(max_length=200, verbose_name='News Title')
    # description = models.CharField(verbose_name='Short Description',max_length=500)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, db_index=True,
                            help_text='Don\'t need to fill this, because this field will be automatically generate')
    shortDescription = models.CharField(
        verbose_name='Short Description', max_length=500)
    content = models.TextField(
        verbose_name='News content', help_text="Max charecter 800 ")
    picture = models.ImageField(verbose_name='Picture  ( 16:9 ratio is recommended)', upload_to=ImageUploderPath(
        'news/').uploadTo, null=True, blank=True)

    # viewcount=models.IntegerField(verbose_name='Article view count',default=0)
    created = models.DateField(
        auto_now=False, auto_now_add=True, db_index=True)
    # updated when every time model.saved is called
    updated = models.DateField(
        auto_now=True, auto_now_add=False, db_index=True)

    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        try:
            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)
        except:
            pass

        super().delete()

    def get_absolute_url(self):
        return reverse('core:news_details', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(str(self.title).lower()+"-" +
                                str((uuid.uuid1(4)))[0:8], allow_unicode=False)
        return super(LastNews, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

# LastNews.objects.order_by("hit_count_generic__hits")


class Category(models.Model):
    name = models.CharField(max_length=30)
    article_type = models.CharField(
        max_length=1, choices=ARTICLE_TYPE.choices())

    def __str__(self) -> str:
        type_ = ARTICLE_TYPE.get_key_form_value(self.article_type)
        return f'{self.name} ({type_})'

    class Meta:
        verbose_name = "Article and Publication Category"


class BlogAndArticle(models.Model):

    title = models.CharField(max_length=200, verbose_name='Title')
    article_type = models.CharField(
        max_length=1, choices=ARTICLE_TYPE.choices())
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True, db_index=True,
                            help_text='Don\'t need to fill this, because this field will be automatically generate')
    shortDescription = models.CharField(
        verbose_name='Short Description', max_length=500)
    content = models.TextField(verbose_name='Article content')
    picture = models.ImageField(verbose_name='Picture (2.35:1 ratio is recommended)', upload_to=ImageUploderPath(
        'blog_and_article/').uploadTo, null=True, blank=True,)

    # viewcount=models.IntegerField(verbose_name='Article view count',default=0)
    created = models.DateField(auto_now_add=True)
    # updated when evey time model.saved is called
    updated = models.DateField(auto_now=True)

    # Hitcounter will detect IPs and prevent from unreal views. So, views will count once for each specific user.
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    comments = models.ManyToManyField(to=Comments)

    category = models.ForeignKey(
        to=Category, on_delete=models.SET_NULL, blank=True, null=True)

    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        try:
            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)
        except:
            pass

        super().delete()

    def get_absolute_url(self):
        return reverse('core:blogAndArticle', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Article And Publication'

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(str(self.title).lower()+"-" +
                                str((uuid.uuid1(4)))[0:8], allow_unicode=False)
        return super(BlogAndArticle, self).save(*args, **kwargs)


@receiver(pre_save, sender=BlogAndArticle)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Affiliates(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Affiliates name')
    picture = models.ImageField(verbose_name='Picture (1:1 ratio is recommended) ', upload_to=ImageUploderPath(
        'affiliates/').uploadTo, null=True, blank=True)
    created = models.DateField(
        auto_now=False, auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return self.name

    def delete(self, using=None, keep_parents=False):
        try:
            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)
        except:
            pass

        super().delete()


class GetinTouch(models.Model):
    fullname = models.CharField(max_length=500, verbose_name='Fullname')
    email = models.EmailField(verbose_name='Email')
    discription = models.TextField(
        max_length=5000, verbose_name='Short Description')

    created = models.DateField(
        auto_now=False, auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return f"{self.fullname} and {self.email}"

    class Meta:

        ordering = ['created']


def check_semester_year(value):
    digit_len = len(str(value))

    if digit_len == 4:
        return value
    raise ValidationError(
        f'Semester Year field accept integer number of length 4, you given number is  {digit_len}')


class Semester(models.Model):
    # semester_names=((2,'Spring'),(3,'Summer'),(4,'Fall'))
    slug = models.SlugField(max_length=225, blank=True, null=True, unique=True, db_index=True,
                            help_text='Don\'t need to fill this, because this field will be automatically generate')

    # semester_indx=models.IntegerField(choices=semester_names)
    readable_name = models.CharField(
        max_length=100, verbose_name='Readable Name',)
    semester_year = models.IntegerField(validators=[
                                        check_semester_year], help_text='for example, 2022 or 2018 or 2019 .. etc.', verbose_name='year')
    priority = models.IntegerField(
        blank=True, default=1, help_text="Lower the value higher the priority is")
    prioritys_combain = models.IntegerField(
        blank=True, unique=True, help_text="Lower the value higher the priority is")

    @property
    def name(self):
        return self.readable_name

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(str(self.readable_name).lower(
            )+str((uuid.uuid1(4)))[0:5], allow_unicode=False)
        self.prioritys_combain = self.semester_year*10 + self.priority
        return super(Semester, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-prioritys_combain']
        verbose_name = "Club Year"


@receiver(pre_save, sender=Semester)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator_with_readable_name(instance)


class Images(models.Model):
    img = models.ImageField(verbose_name='Image',
                            upload_to=ImageUploderPath('event/images/').uploadTo_withBasefile, width_field='width', height_field='height')
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    event = models.ForeignKey(
        'ClubEvent', related_name='images', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.event.title + "/img/"

    def delete(self, using=None, keep_parents=False):
        try:

            storage = self.img.storage

            if storage.exists(self.img.name):
                storage.delete(self.img.name)
        except:
            pass

        super().delete()


class ClubEvent(models.Model):
    slug = models.SlugField(max_length=225, blank=True, null=True, unique=True, db_index=True,
                            help_text='Don\'t need to fill this, because this field will be automatically generate')

    date = models.DateField()
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL,
                                 null=True, related_name='clubevents', verbose_name='Club year')
    title = models.CharField(max_length=200)
    shortDescription = models.CharField(
        max_length=250, help_text='sort description about the event')
    content = models.TextField(verbose_name='Event description')
    picture = models.ImageField(verbose_name='Event banner (2.35:1 ratio is recommended)',
                                upload_to=ImageUploderPath('event/banner/').uploadTo, null=True, blank=True)

    created = models.DateField(
        auto_now=False, auto_now_add=True, db_index=True)

    # Hitcounter will detect IPs and prevent from unreal views. So, views will count once for each specific user.
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )

    comments = models.ManyToManyField(to=Comments)

    def current_hit_count(self):
        return self.hit_count.hits

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(str(self.title).lower() +
                                str((uuid.uuid1(4)))[0:8])
        return super(ClubEvent, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        try:

            storage = self.picture.storage

            if storage.exists(self.picture.name):
                storage.delete(self.picture.name)
        except:
            pass

        super().delete()

    def get_absolute_url(self):
        return reverse('core:event', kwargs={'slug': self.slug})


@receiver(pre_save, sender=ClubEvent)
def auto_slug_generator(sender, instance, **kwargs):
    """
    Creates a slug if there is no slug.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class WhyJoin(models.Model):
    reason = models.CharField(max_length=500, help_text="Max charecter is 500")

    def __str__(self) -> str:
        return f'{self.reason[:100]}.....'

    class Meta:
        verbose_name = "Why Join Us!"
        verbose_name_plural = "Why Join Us!"


class TermsAndCondition(SingletonModel):
    name = models.CharField(max_length=100, default="Terms & Condition")
    content = models.TextField()

    def __str__(self):
        return self.name
