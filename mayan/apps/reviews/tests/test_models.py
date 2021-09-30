from mayan.apps.testing.tests.base import BaseTestCase

from ..models import Candidate, ReviewForm

from .mixins import ReviewsTestMixin

class ReviewTestCase(ReviewsTestMixin, BaseTestCase):
    def test_candidate_creation(self):
        self._create_test_candidate()

        self.assertEqual(Candidate.objects.all().count(), 1)
        self.assertQuerysetEqual(
            Candidate.objects.all(), (repr(self.test_candidate),)
        )
    def test_reviewform_creation(self):
        self._create_test_reviewform()

        self.assertEqual(ReviewForm.objects.all().count(), 1)
        self.assertQuerysetEqual(
            ReviewForm.objects.all(), (repr(self.test_reviewform),)
        )