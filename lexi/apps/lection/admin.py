from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from embed_video.admin import AdminVideoMixin
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Course, Lesson, Question, Answer, Unit


class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 3


class BaseAnswerInline(admin.StackedInline):
    model = Answer


class QuestionInline(NestedStackedInline):
    model = Question
    inlines = [AnswerInline,]
    extra = 1
    # fieldsets = [
    #     (_('Text'), {'fields': ['text','creator']}),
    #     (_('Additional data'),
    #      {'fields': ['title'],
    #      'classes': ['collapse']}
    #     ),
    # ]


class UnitInline(NestedStackedInline):
    model = Unit
    inlines = [QuestionInline,]
    extra = 1
    fieldsets = [
        (_('Data'), {'fields': ['title', 'video', 'creator']}),
        (_('Explanation'), {'fields': ['explanation'], 'classes': ['collapse']}),
    ]


class UnitAdmin(
    AdminVideoMixin,
    admin.ModelAdmin,
    # NestedModelAdmin
    ):
    # inlines = [QuestionInline]
    pass


class LessonAdmin(AdminVideoMixin,
                  # NestedModelAdmin,
                  admin.ModelAdmin
                  ):
    pass
    # inlines = [UnitInline]
    # fields = ('title', 'course', 'creator', 'slug')


class UserAnsAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'answer',
    )
    # pass

class QuestionAdmin(admin.ModelAdmin):
    inlines = [BaseAnswerInline]

admin.site.register(Unit, UnitAdmin)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
