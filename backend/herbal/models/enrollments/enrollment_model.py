# herbal/models/enrollments/enrollment_model.py

from django.db import models
from django.core.exceptions import ValidationError
from ..screening.screening_model import Screening
from core.models import BaseModel


class Enrollment(BaseModel):

    screening = models.OneToOneField(
        Screening,
        on_delete=models.CASCADE,
        related_name="enrollment"
    )

    enrollment_date = models.DateField()

    # =========================
    # ✅ PATIENT CATEGORY
    # =========================
    PT_CATEGORY_CHOICES = [
        ("intervention", "Intervention"),
        ("control", "Control"),
    ]

    pt_category = models.CharField(
        max_length=20,
        choices=PT_CATEGORY_CHOICES
    )

    # =========================
    # ✅ PATIENT TYPE
    # =========================
    PT_TYPE_CHOICES = [
        ("new", "New"),
        ("follow_up", "Follow Up"),
    ]

    pt_type = models.CharField(
        max_length=20,
        choices=PT_TYPE_CHOICES
    )

    # =========================
    # ✅ TREATMENT TYPE
    # =========================
    TREATMENT_TYPE_CHOICES = [
        ("chemo", "Chemotherapy"),
        ("radiation", "Radiation"),
        ("surgery", "Surgery"),
        ("other", "Other"),
    ]

    treatment_type = models.CharField(
        max_length=50,
        choices=TREATMENT_TYPE_CHOICES
    )

    # =========================
    # ✅ PREVIOUS VISIT DATE
    # =========================
    previous_date = models.DateField(
        null=True,
        blank=True
    )

    # =========================
    # ✅ CYCLES
    # =========================
    total_cycle = models.PositiveIntegerField(
        help_text="Total planned treatment cycles"
    )

    cycle_number = models.PositiveIntegerField(
        help_text="Current cycle number"
    )

    # =========================
    # ✅ STATUS
    # =========================
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("terminated", "Terminated"),
        ("lost", "Lost To Follow Up"),
        ("transfer", "Transferred Out"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    # =========================
    # ✅ VALIDATION
    # =========================
    def clean(self):

        # Follow-up must have previous date
        if self.pt_type == "follow_up" and not self.previous_date:
            raise ValidationError({
                "previous_date": "Previous date is required for follow-up patients."
            })

        # Cycle logic
        if self.total_cycle and self.cycle_number:
            if self.cycle_number > self.total_cycle:
                raise ValidationError({
                    "cycle_number": "Cycle number cannot exceed total cycles."
                })

    def __str__(self):
        return f"Enrollment - {self.screening}"