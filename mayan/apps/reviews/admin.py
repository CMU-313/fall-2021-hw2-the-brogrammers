### Used to display model in Django Admin Panel"
from django.contrib import admin

from .models import ReviewForm, Candidate


@admin.register(ReviewForm)
class ReviewFormAdmin(admin.ModelAdmin):
    list_display = ('reviewerName', 'candidate', 'leadership', 'extracurriculars','recLetters','interview', 'essay')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'phone_number', 'gpa', 'major', 'university')