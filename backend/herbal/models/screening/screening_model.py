# herbal/models/screening/screening_model.py

from django.db import models
from ..subjects.subject_model import Subject
from core.models import BaseModel


class YesNoChoices(models.IntegerChoices):
    YES = 1, "Yes"
    NO = 2, "No"


class Screening(BaseModel):

    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name="screening"
    )

    # Core
    screening_date = models.DateField()

    # Consent
    consented = models.IntegerField(choices=YesNoChoices.choices)
    consent_date = models.DateField(null=True, blank=True)

    consented_nimregenin = models.IntegerField(choices=YesNoChoices.choices)
    nimregenin_date = models.DateField(null=True, blank=True)

    reasons = models.TextField(blank=True, null=True)

    # Inclusion Criteria
    age_18 = models.IntegerField(choices=YesNoChoices.choices)

    biopsy = models.IntegerField(choices=YesNoChoices.choices)
    breast_cancer = models.IntegerField(choices=YesNoChoices.choices)
    brain_cancer = models.IntegerField(choices=YesNoChoices.choices)
    cervical_cancer = models.IntegerField(choices=YesNoChoices.choices)
    prostate_cancer = models.IntegerField(choices=YesNoChoices.choices)

    # Exclusion Criteria
    pregnant = models.IntegerField(choices=YesNoChoices.choices)
    breast_feeding = models.IntegerField(choices=YesNoChoices.choices)
    ckd = models.IntegerField(choices=YesNoChoices.choices)
    liver_disease = models.IntegerField(choices=YesNoChoices.choices)

    # Notes
    remarks = models.TextField(blank=True, null=True)

    inclusion_criteria_met = models.BooleanField(default=False)
    exclusion_criteria_present = models.BooleanField(default=False)
    eligible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # =========================
        # ✅ BASIC INCLUSION
        # =========================
        basic_inclusion = (
            self.consented == YesNoChoices.YES and
            self.age_18 == YesNoChoices.YES and
            self.biopsy == YesNoChoices.YES
        )

        # =========================
        # ✅ SEX (FK SAFE)
        # =========================
        sex = self.subject.sex_id  # ✅ correct for FK

        # =========================
        # ✅ SEX-AWARE CANCER LOGIC
        # =========================
        common_cancers = [
            self.breast_cancer,   # both sexes ✔
            self.brain_cancer,    # both sexes ✔
        ]

        if sex == 1:  # Male
            specific_cancers = [self.prostate_cancer]

        elif sex == 2:  # Female
            specific_cancers = [self.cervical_cancer]

        else:
            specific_cancers = []

        cancer_fields = common_cancers + specific_cancers

        has_cancer = any(
            field == YesNoChoices.YES for field in cancer_fields
        )

        # Final inclusion
        self.inclusion_criteria_met = basic_inclusion and has_cancer

        # =========================
        # ✅ SEX-AWARE EXCLUSIONS
        # =========================
        exclusion_fields = [
            self.ckd,
            self.liver_disease,
        ]

        if sex == 2:  # Female only
            exclusion_fields.extend([
                self.pregnant,
                self.breast_feeding,
            ])

        self.exclusion_criteria_present = any(
            field == YesNoChoices.YES for field in exclusion_fields
        )

        # =========================
        # ✅ FINAL ELIGIBILITY
        # =========================
        self.eligible = (
            self.inclusion_criteria_met and not self.exclusion_criteria_present
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Screening - {self.subject}"