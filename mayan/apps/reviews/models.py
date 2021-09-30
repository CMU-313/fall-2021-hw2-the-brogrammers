from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bleach import Cleaner
from bleach.linkifier import LinkifyFilter
from datetime import date

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from mayan.apps.templating.classes import Template
from mayan.apps.acls.models import AccessControlList
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.events.classes import EventManagerMethodAfter, EventManagerSave
from mayan.apps.events.decorators import method_event

from .events import (
    event_review_created, event_review_edited, event_review_document_added,
    event_review_document_removed
)

# Candidate model represents a candidate for a future review.
class Candidate(models.Model):
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
  )
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

  
  # set default ordering when Candidate objects are queried
  class Meta:
    ordering = ['firstName', 'lastName']

  def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)
  
  # methods to average a Candidate's reviews
  def get_reviews_interview_avg(self):
    L = self.get_reviews()
    if len(L) == 0:
      return 'N/A'
    res = 0
    for r in L:
      res += r.interview
    return round(res / len(L), 2)
  
  def get_reviews_leadership_avg(self):
    L = self.get_reviews()
    if len(L) == 0:
      return 'N/A'
    res = 0
    for r in L:
      res += r.leadership
    return round(res / len(L), 2)

  def get_reviews_recletter_avg(self):
    L = self.get_reviews()
    if len(L) == 0:
      return 'N/A'
    res = 0
    for r in L:
      res += r.recLetters
    return round(res / len(L), 2)

  def get_reviews_extra_avg(self):
    L = self.get_reviews()
    if len(L) == 0:
      return 'N/A'
    res = 0
    for r in L:
      res += r.extracurriculars
    return round(res / len(L), 2)

  def get_reviews_essay_avg(self):
    L = self.get_reviews()
    if len(L) == 0:
      return 'N/A'
    res = 0
    for r in L:
      res += r.essay
    return round(res / len(L), 2)

  def get_reviews_count(self):
    return self.get_reviews().count()

  def get_reviews(self):
    reviews = ReviewForm.objects.filter(
      candidate=self.pk
    )
    return reviews

# ReviewForm model represents information we collect on a candidate for evals
class ReviewForm(ExtraDataModelMixin, MPTTModel):

  parent = TreeForeignKey(
    blank=True, db_index=True, null=True, on_delete=models.CASCADE,
    related_name='children', to='self'
  )

  candidate = models.ForeignKey(
    Candidate, on_delete=CASCADE,
    help_text=_('Target candidate.'),
    verbose_name=_('Candidate')
  )

  reviewerName = models.CharField(
    max_length=255, help_text=_('Name of the reviewer.'),
    verbose_name=_('Reviewer')
  )

  leadership = models.PositiveIntegerField(
    help_text=_('Leadership rating of candidate (0 - 10)'),
    verbose_name=_('Leadership'),
    validators = [
      MaxValueValidator(10),
      MinValueValidator(0),
    ]
  )

  extracurriculars = models.PositiveSmallIntegerField(
    help_text=_('Extracurriculars rating of candidate (0 - 10)'),
    verbose_name=_('Extracurriculars'),
    validators = [
      MaxValueValidator(10),
      MinValueValidator(0),
    ]    
  )

  recLetters = models.PositiveSmallIntegerField(
    help_text=_('RecLetters rating of candidate (0 - 10)'),
    verbose_name=_('Rec Letters'),
    validators = [
      MaxValueValidator(10),
      MinValueValidator(0),
    ]
  )

  interview = models.PositiveSmallIntegerField(
    help_text=_('Interview rating of candidate (0 - 10)'),
    verbose_name=_('Interview'),
    validators = [
      MaxValueValidator(10),
      MinValueValidator(0),
    ],
  )

  essay = models.PositiveSmallIntegerField(
    help_text=_('Essay rating of candidate (0 - 10)'),
    verbose_name=_('Essay'),
    validators = [
      MaxValueValidator(10),
      MinValueValidator(0),
    ],
  )

  created_at = models.DateField(
    default=date.today,
    verbose_name=_('Creation Date'),
    validators=[
      MaxValueValidator(limit_value=date.today)
    ],
  )

  def __str__(self):
        return 'Review for candidate, {}'.format(str(self.candidate))

  def get_absolute_url(self):
        return reverse(
            viewname='reviews:reviewform_detail', kwargs={'reviewform_id': self.pk}
        )

  def get_rendered_body(self, field):
      cleaner = Cleaner(
          filters=[LinkifyFilter]
      )
      template = Template(template_string=cleaner.clean(text=self.reviewerName))
      if(field == "reviwerName"):
        template = Template(
            template_string=cleaner.clean(text=self.reviewerName)
        )
      elif(field == "candidate"):
        template = Template(
            template_string=cleaner.clean(text=str(self.candidate))
        )
      elif(field == "leadership"):
        template = Template(
            template_string=cleaner.clean(text=self.leadership)
        )
      elif(field == "extracurriculars"):
        template = Template(
            template_string=cleaner.clean(text=self.extracurriculars)
        )
      elif(field == "recLetters"):
        template = Template(
            template_string=cleaner.clean(text=self.recLetters)
        )
      elif(field == "interview"):
        template = Template(
            template_string=cleaner.clean(text=self.interview)
        )
      elif(field == "essay"):
        template = Template(
            template_string=cleaner.clean(text=self.essay)
        )
      elif(field == "createdAt"):
        template = Template(
            template_string=cleaner.clean(text=self.created_at)
        )
      return template.render()

  class MPTTMeta:
    order_insertion_by = ('candidate',)

  class Meta:
      # unique_together doesn't work if there is a FK
      # https://code.djangoproject.com/ticket/1751
      unique_together = ('parent', 'candidate')
      verbose_name = _('Review')
      verbose_name_plural = _('Reviews')
