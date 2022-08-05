from django.contrib import admin
from django.db.models import fields
from solo.admin import SingletonModelAdmin
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
from .forms import BlogAndArticleAdminForm, LastNewsAdminForm, SemesterAdminForm, WhyJoinAdminForm
from .models import *
from members.admin import broadcast_email


admin.site.register(Announcement)
admin.site.register(Category)

@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    actions = (broadcast_email,)


@admin.register(WhyJoin)
class WhyJoinAdmin(admin.ModelAdmin):
    form=WhyJoinAdminForm
    
admin.site.register(WhatWedid)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    readonly_fields = ('replay',)
    list_filter = ('created',)
    list_display = ('__str__', 'created')
    search_fields = ('message', 'email', 'username')

@admin.register(TermsAndCondition)
class TermsAndConditionAdmin(
        SingletonModelAdmin, 
        SummernoteModelAdmin):

        pass

them_fields=(
                    'font_links',
                    'font_family',
                    'primary_color',
                    'text_p_color',
                    'primary_lite_color',
                    'primary_dark_color',
                    'secondary_color',
                    'secondary_lite_color',
                    'secondary_dark_color',
                    'text_s_color',
                    'gray_color',
                    'footer_bg_color',
                    'footer_text_color',
                    'footer_text_hover_color',
                )
@admin.register(ClubInfo)
class ClubInfoAdmin(
        SingletonModelAdmin, 
        SummernoteModelAdmin):
    save_on_top = True
    summernote_fields = ('description', 'sort_description_for_footer')
    fieldsets = (
        ('Standard info', {
            'fields': ('name', 'sort_name', 'email',
                        'address', 'google_map_link','meta_title',
                        'meta_description',
                        'description', 'sort_description_for_footer',
                        'registation_form_open')
        }),
        (
            'Social links', {
                'fields': (
                    'faebook_url',
                    'twitter_url',
                    'linkend_url',
                    'instagram_url',
                )
            }
        ),
        ('Member Count', {
            'fields': ('current_member',
                       'alumni',
                       'advisors',)
        }),

        ('Prictures', {
            'fields': (
                # _preview are readonly field 
                'logo','logo_preview',
                'logo_2','logo_2_preview',
                'logo_3','logo_3_preview',
                'landing_picture','landing_picture_preview',
                'landing_picture_two','landing_picture_2_preview',
                'landing_picture_three','landing_picture_3_preview',
                'landing_picture_four','landing_picture_4_preview',
                'landing_picture_five','landing_picture_5_preview',

            )
        }

        ),
        (
            'Themes', {
                'fields': them_fields
            }
        )
    )

    readonly_fields = (
        'logo_preview',
        'logo_2_preview',
        'logo_3_preview',
        'landing_picture_preview',
        'landing_picture_2_preview',
        'landing_picture_3_preview',
        'landing_picture_4_preview',
        'landing_picture_5_preview',
        *them_fields
    )

# # There is only one item in the table, you can get it this way:
# from .models import ClubInfo
# config = ClubInfo.objects.get()

# # get_solo will create the item if it does not already exist
# config = ClubInfo.get_solo()


@admin.register(BlogAndArticle)
class BlogAndArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    readonly_fields = ('comments',)
    form=BlogAndArticleAdminForm


@admin.register(LastNews)
class LastNewsAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


@admin.register(Affiliates)
class AffiliatesAdmin(admin.ModelAdmin):
    pass


@admin.register(GetinTouch)
class GetinTouchAdmin(admin.ModelAdmin):
    actions = (broadcast_email,)
    list_filter = ['created']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    form = SemesterAdminForm


class ImageAdminInline(admin.TabularInline):
    model = Images
    exclude = ['width', 'height']


@admin.register(ClubEvent)
class ClubEventAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    inlines = [ImageAdminInline]
    readonly_fields = ('comments',)
    # exclude=()
