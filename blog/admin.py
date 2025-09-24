from django.contrib import admin
from .models import User, Article
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name")
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "groups")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

# #
# # class ArticleAdmin(admin.ModelAdmin):
# #     list_display = ('title', 'created_by', 'status', 'published_date', 'created')
# #     list_filter = ('status', 'created_by')
# #     prepopulated_fields = {'slug': ('title',)}
# #     search_fields = ('title', 'body')
# #     ordering = ('-published_date',)
#
# #
# # admin.site.site_header = "Dashboard"
# # admin.site.site_title = "Blogger"
# # admin.site.index_title = "Control Panel"
# # admin.site.register(User, CustomUserAdmin)
# # admin.site.register(Article, ArticleAdmin)
#
#
# # admin.py (excerpt)
# from django.contrib import admin, messages
# from django.urls import path
# from django.shortcuts import redirect, get_object_or_404
# from django.utils.html import format_html
# from .models import Article
# from .utils.gemini_client import generate_article_text
#
#
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_by', 'status', 'published_date', 'created')
#     list_filter = ('status', 'created_by')
#     prepopulated_fields = {'slug': ('title',)}
#     search_fields = ('title', 'body')
#     ordering = ('-published_date',)
#     actions = ['generate_with_gemini']
#     change_form_template = "admin/blog/article/change_form.html"  # we'll add a small override template
#
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('<path:object_id>/generate_gemini/', self.admin_site.admin_view(self.generate_single), name='blog_article_generate_gemini'),
#         ]
#         return custom_urls + urls
#
#     def generate_with_gemini(self, request, queryset):
#         """Admin action for multiple selected articles."""
#         success = 0
#         for article in queryset:
#             try:
#                 generated = generate_article_text(article.title, article.description or "")
#                 article.body = generated
#                 article.status = Article.DRAFT  # ensure it's a draft
#                 article.published_date = None
#                 article.save()
#                 success += 1
#             except Exception as e:
#                 self.message_user(request, f"Failed for {article.title}: {e}", level=messages.ERROR)
#         self.message_user(request, f"Generated content for {success} article(s).", level=messages.SUCCESS)
#     generate_with_gemini.short_description = "Generate article content with Gemini (set as draft)"
#
#     def generate_single(self, request, object_id, *args, **kwargs):
#         """Admin view for generating content for a single Article via a button on the change form."""
#         article = get_object_or_404(Article, pk=object_id)
#         try:
#             generated = generate_article_text(article.title, article.description or "")
#             article.body = generated
#             article.status = Article.DRAFT
#             article.published_date = None
#             article.save()
#             self.message_user(request, f"Generated content for “{article.title}”. It is saved as draft.", level=messages.SUCCESS)
#         except Exception as e:
#             self.message_user(request, f"Generation failed: {e}", level=messages.ERROR)
#
#         # Redirect back to change form
#         return redirect('admin:blog_article_change', object_id)
#
#
# admin.site.site_header = "Dashboard"
# admin.site.site_title = "Blogger"
# admin.site.index_title = "Control Panel"
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Article, ArticleAdmin)


# blog/admin.py

from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse
from django.core.exceptions import ValidationError
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget, ArrayWidget
from unfold.decorators import action
from .models import Article
from .utils.gemini_client import generate_article_text
import logging

logger = logging.getLogger(__name__)


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'body': WysiwygWidget(),
            'description': admin.widgets.AdminTextInputWidget(attrs={'class': 'vTextField'}),
        }


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    form = ArticleAdminForm
    list_display = [
        'title',
        'status',
        'created_by',
        'created',
        'published_date',
        'gemini_actions'
    ]
    list_filter = ['status', 'created', 'published_date', 'created_by']
    search_fields = ['title', 'description', 'body']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created', 'modified']

    # Unfold specific configurations
    list_display_links = ['title']
    list_per_page = 25

    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'description', 'body'),
            'classes': ['wide']
        }),
        ('Publication', {
            'fields': ('status', 'published_date'),
            'classes': ['wide']
        }),
        ('Meta Information', {
            'fields': ('created_by', 'created', 'modified'),
            'classes': ['collapse']
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-with-gemini/',
                self.admin_site.admin_view(self.generate_article_view),
                name='blog_article_generate_gemini',
            ),
            path(
                '<int:object_id>/regenerate-with-gemini/',
                self.admin_site.admin_view(self.regenerate_article_view),
                name='blog_article_regenerate_gemini',
            ),
            path(
                'generate-gemini-ajax/',
                self.admin_site.admin_view(self.generate_gemini_ajax),
                name='blog_article_generate_gemini_ajax',
            ),
        ]
        return custom_urls + urls

    def gemini_actions(self, obj):
        """Display action buttons for Gemini generation"""
        if obj.pk:
            regenerate_url = reverse('admin:blog_article_regenerate_gemini', args=[obj.pk])
            return format_html(
                '<a class="button" href="{}" style="background: #4285f4; color: white; '
                'padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 12px;">'
                '🤖 Regenerate with Gemini</a>',
                regenerate_url
            )
        return format_html(
            '<span style="color: #666; font-size: 12px;">Save first to enable Gemini</span>'
        )

    gemini_actions.short_description = 'Gemini Actions'
    gemini_actions.allow_tags = True

    def get_changeform_initial_data(self, request):
        """Add generate button to change form"""
        initial = super().get_changeform_initial_data(request)
        return initial

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add Gemini generation context to change view"""
        extra_context = extra_context or {}
        extra_context['show_gemini_button'] = True
        extra_context['gemini_generate_url'] = reverse('admin:blog_article_generate_gemini_ajax')
        return super().change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """Add Gemini generation context to add view"""
        extra_context = extra_context or {}
        extra_context['show_gemini_button'] = True
        extra_context['gemini_generate_url'] = reverse('admin:blog_article_generate_gemini_ajax')
        return super().add_view(request, form_url, extra_context)

    def generate_article_view(self, request):
        """View for generating new article with Gemini"""
        if request.method == 'POST':
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            word_target = int(request.POST.get('word_target', 800))

            if not title:
                messages.error(request, 'Title is required to generate an article.')
                return self._render_generate_form(request)

            try:
                # Generate content with Gemini
                generated_content = generate_article_text(
                    title=title,
                    description=description or None,
                    word_target=word_target
                )

                # Create new article
                article = Article(
                    title=title,
                    description=description,
                    body=generated_content,
                    created_by=request.user,
                    status=Article.DRAFT
                )
                article.save()

                messages.success(
                    request,
                    f'Article "{title}" generated successfully! You can now review and edit it.'
                )

                # Redirect to edit the new article
                return HttpResponseRedirect(
                    reverse('admin:blog_article_change', args=[article.pk])
                )

            except Exception as e:
                logger.error(f"Gemini generation failed: {str(e)}")
                messages.error(request, f'Generation failed: {str(e)}')
                return self._render_generate_form(request, {
                    'title': title,
                    'description': description,
                    'word_target': word_target
                })

        return self._render_generate_form(request)

    def regenerate_article_view(self, request, object_id):
        """View for regenerating existing article content"""
        try:
            article = Article.objects.get(pk=object_id)
        except Article.DoesNotExist:
            messages.error(request, 'Article not found.')
            return HttpResponseRedirect(reverse('admin:blog_article_changelist'))

        if request.method == 'POST':
            word_target = int(request.POST.get('word_target', 800))
            use_description = request.POST.get('use_description') == 'on'

            try:
                # Generate new content
                generated_content = generate_article_text(
                    title=article.title,
                    description=article.description if use_description else None,
                    word_target=word_target
                )

                # Update article body
                article.body = generated_content
                article.save()

                messages.success(
                    request,
                    f'Article "{article.title}" regenerated successfully!'
                )

                return HttpResponseRedirect(
                    reverse('admin:blog_article_change', args=[article.pk])
                )

            except Exception as e:
                logger.error(f"Gemini regeneration failed: {str(e)}")
                messages.error(request, f'Regeneration failed: {str(e)}')

        context = {
            'article': article,
            'opts': self.model._meta,
            'title': f'Regenerate "{article.title}" with Gemini',
        }

        return TemplateResponse(
            request,
            'admin/blog/article/generate_gemini.html',
            context
        )

    def generate_gemini_ajax(self, request):
        """AJAX endpoint for generating content"""
        if request.method != 'POST':
            return JsonResponse({'error': 'POST method required'}, status=405)

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        word_target = int(request.POST.get('word_target', 800))

        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)

        try:
            generated_content = generate_article_text(
                title=title,
                description=description or None,
                word_target=word_target
            )

            return JsonResponse({
                'success': True,
                'content': generated_content,
                'message': 'Content generated successfully!'
            })

        except Exception as e:
            logger.error(f"AJAX Gemini generation failed: {str(e)}")
            return JsonResponse({
                'error': str(e),
                'message': 'Generation failed. Please try again.'
            }, status=500)

    def _render_generate_form(self, request, initial_data=None):
        """Helper to render the generation form"""
        context = {
            'title': 'Generate Article with Gemini',
            'opts': self.model._meta,
            'initial_data': initial_data or {},
        }
        return TemplateResponse(
            request,
            'admin/blog/article/generate_gemini.html',
            context
        )

    @action(description="Generate selected articles with Gemini", permissions=["change"])
    def bulk_generate_with_gemini(self, request, queryset):
        """Bulk action to regenerate multiple articles"""
        updated_count = 0
        errors = []

        for article in queryset:
            try:
                generated_content = generate_article_text(
                    title=article.title,
                    description=article.description,
                    word_target=800
                )
                article.body = generated_content
                article.save()
                updated_count += 1
            except Exception as e:
                errors.append(f"{article.title}: {str(e)}")

        if updated_count:
            messages.success(request, f'Successfully regenerated {updated_count} articles.')

        if errors:
            messages.warning(request, f'Errors occurred: {"; ".join(errors[:3])}...')

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # Ensure the body field has a reliable marker
    #     if 'body' in form.fields:
    #         widget = form.fields['body'].widget
    #         widget.attrs.update({
    #             'data-gemini-target': 'true',
    #             'class': widget.attrs.get('class', '') + ' gemini-body-field'
    #         })
    #     return form


    def save_model(self, request, obj, form, change):
        """Set created_by when creating new articles"""
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # Unfold specific methods for better integration
    def get_list_display(self, request):
        """Customize list display for Unfold"""
        return self.list_display

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # We'll inject the button via formfield_for_dbfield instead
        return fieldsets

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        if db_field.name == "body":
            # Store article ID for AJAX call
            article_id = request.resolver_match.kwargs.get('object_id')
            if article_id:
                formfield.widget.attrs.update({
                    'data-article-id': article_id,
                    'class': (formfield.widget.attrs.get('class', '') + ' gemini-body-field').strip()
                })
        return formfield

    class Media:

        css = {
            'all': ('admin/css/gemini_admin.css',)
        }
        js = ('admin/js/gemini_admin.js',)


admin.site.site_header = "Dashboard"
admin.site.site_title = "Blogger"
admin.site.index_title = "Control Panel"
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Article, ArticleAdmin)

