import logging
from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.widgets import TextAreaDiv

from mayan.apps.views.forms import FilteredSelectionForm

logger = logging.getLogger(name=__name__)



class ReviewDetailForm(forms.Form):
    reviewerName = forms.CharField(
        label=_('Reviewer Name'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    candidate = forms.CharField(
        label=_('Candidate Name'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    leadership = forms.CharField(
        label=_('Leadership Rating (0 - 10):'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    extracurriculars = forms.CharField(
        label=_('Extracurriculars Rating (0 - 10):'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    recLetters = forms.CharField(
        label=_('Recommendation Letters Rating (0 - 10):'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    interview = forms.CharField(
        label=_('Interview Rating (0 - 10):'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    essay = forms.CharField(
        label=_('Essays Rating (0 - 10):'),
        widget=TextAreaDiv(
            attrs={
                'class': 'views-text-wrap text_area_div',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        self.fields['reviewerName'].initial = self.instance.reviewerName
        self.fields['candidate'].initial = self.instance.candidate
        self.fields['leadership'].initial = self.instance.leadership
        self.fields['extracurriculars'].initial = self.instance.extracurriculars
        self.fields['recLetters'].initial = self.instance.recLetters
        self.fields['interview'].initial = self.instance.interview
        self.fields['essay'].initial = self.instance.essay


class ReviewListForm(FilteredSelectionForm):
    class Meta:
        allow_multiple = True
        field_name = 'reviews'
        label = _('Reviews')
        required = False
        widget_attributes = {'class': 'select2'}
