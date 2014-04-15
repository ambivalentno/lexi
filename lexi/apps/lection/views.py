from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Course, Lesson, Unit


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course


class LessonDetailView(DetailView):
    model = Lesson


class UnitDetailView(DetailView):
    model = Unit
