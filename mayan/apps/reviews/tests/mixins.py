from ..models import Candidate, ReviewForm

class ReviewsTestMixin:
    def setUp(self):
        super().setUp()
        if not hasattr(self, 'test_reviews'):
            self.test_reviewforms = []
        if not hasattr(self, 'test_candidates'):
            self.test_candidates = []

    def _create_test_candidate(self):
        self.test_candidate = Candidate.objects.create()
        self.test_candidates.append(self.test_candidate)

    def _create_test_reviewform(self):
        self.test_reviewform = ReviewForm.objects.create()
        self.test_reviewforms.append(self.test_reviewform)