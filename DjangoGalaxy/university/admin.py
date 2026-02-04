from django.contrib import admin
from . import models

@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["name", 'country']

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]

@admin.register(models.UniversityCourse)
class UniversityCourseAdmin(admin.ModelAdmin):
    list_display = ["semester", "duration_weeks"]