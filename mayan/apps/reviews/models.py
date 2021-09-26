from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


"""
Sample Review

Key: Question
Value: Response

"""

class Candidate(models.Model):
  # We assume that this information is somehow imported correctly
  firstName = models.CharField(
    max_length=255, help_text=_('First Name of Candidate'),
    verbose_name=_('First Name'), default=''
  )
  lastName = models.CharField(
    max_length=255, help_text=_('Last Name of Candidate'),
    verbose_name=_('Last Name'), default=''
  )
  email = models.EmailField(
    max_length=255, help_text=_('Email of Candidate'),
    verbose_name=_('email'), default=''
  )
  phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone_number = models.CharField(
    validators=[phone_regex], max_length=17, 
    blank=True, help_text=_('Phone Number of Candidate'),
  ) # validators should be a list
  gpa = models.DecimalField(
    max_digits=3, decimal_places=2, help_text=_('GPA of the applicant'),
  )
  major = models.CharField(
    max_length=255, help_text=_('Major of the applicant.'),
    verbose_name=_('Major')
  )
  university = models.CharField(
    max_length=255, help_text=_('University of the applicant.'),
    verbose_name=_('University')
  )
  # potentially add zero-many relationship


  def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

# we don't need to explicitely implement the link from candidate to review forms
#   formIDs = models.JSONField(
#     help_text=_('List of the form IDs.'),
#     verbose_name=_('FormIDs')
#   )


class ReviewForm(models.Model):
  #candidate object
  # foreign key implementation

  reviewerName = models.CharField(
    max_length=255, help_text=_('Name of the reviewer.'),
    verbose_name=_('Name')
  )

  leadership = models.PositiveSmallIntegerField(
    help_text=_('Leadership rating of candidate.'),
    verbose_name=_('Leadership')
  )

  extracurriculars = models.PositiveSmallIntegerField(
    help_text=_('Extracurriculars rating of candidate.'),
    verbose_name=_('Extracurriculars')
  )

  recLetters = models.PositiveSmallIntegerField(
    help_text=_('RecLetters rating of candidate.'),
    verbose_name=_('RecLetters')
  )

  interview = models.PositiveSmallIntegerField(
    help_text=_('Interview rating of candidate.'),
    verbose_name=_('Interview')
  )

  essay = models.PositiveSmallIntegerField(
    help_text=_('Essay rating of candidate.'),
    verbose_name=_('Essay')
  )

  candidate = models.ForeignKey(
      Candidate, on_delete=CASCADE,
      help_text=_('Target candidate.'),
      verbose_name=_('Candidate')
  )

  @staticmethod
  def get_reviews():
    return ReviewForm.objects.all()

"""
    to retrieve forms from candidate c: c.reviewform_set.all()      <- returns a queryset of all forms linked with the candidate
    to add form f to candidate c: f.candidate = c                   <- this also adds form f to candidate c

    See https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/ for more detail
"""