# herbal/models/visits/unschedule_visit_model.py

from django.db import models
from ..enrollments.enrollment_model import Enrollment
from core.models import BaseModel

class UnscheduledVisit(BaseModel):

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="unscheduled_visits"
    )

    visit_date = models.DateField()

    reason = models.TextField()

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Unscheduled - {self.enrollment.patient}"
