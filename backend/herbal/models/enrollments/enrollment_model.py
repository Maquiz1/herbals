# herbal/models/enrollments/enrollment_model.py

from django.db import models
from django.core.exceptions import ValidationError
from ..screening.screening_model import Screening
from core.models import BaseModel
from choices.models import PatientType,PatientCategory,TreatmentType

class Enrollment(BaseModel):

    screening = models.OneToOneField(
        Screening,
        on_delete=models.CASCADE,
        related_name="enrollment"
    )

    enrollment_date = models.DateField()

    pt_category = models.ForeignKey(
        PatientCategory,
        on_delete=models.PROTECT,
        related_name="subject_categories"
    )

    pt_type = models.ForeignKey(
        PatientType,
        on_delete=models.PROTECT,
        related_name="subject_types"
    )

    # =========================
    # ✅ TREATMENT TYPE
    # =========================
    treatment_type = models.ForeignKey(
        TreatmentType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="subject_treatments"
    )

    treatment_date = models.DateField(
        null=True,
        blank=True
    )
    
    # =========================
    # ✅ PREVIOUS VISIT DATE
    # =========================
    previous_treatment = models.ForeignKey(
        TreatmentType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="subject_previous_treatment"
    )
        
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

    remarks = models.TextField(
        blank=tuple,null=True
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