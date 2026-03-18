# herbal/models/subjects/subject_model.py
from django.db import models
from datetime import date

from sites.models import Site
from core.models import BaseModel
from core.managers.site_manager import SiteRestrictedManager


class Subject(BaseModel):

    subject_id = models.CharField(max_length=50, unique=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    sex = models.CharField(
        max_length=10, choices=[("Male", "Male"), ("Female", "Female")]
    )

    date_of_birth = models.DateField()

    phone = models.CharField(max_length=20, blank=True, null=True)

    village = models.CharField(max_length=100, blank=True)

    registration_date = models.DateField(auto_now_add=True)

    site = models.ForeignKey(Site, on_delete=models.PROTECT)

    objects = SiteRestrictedManager()

    # ----------------------------
    # AGE
    # ----------------------------
    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def save(self, *args, **kwargs):

        # Only generate if not already set
        if not self.subject_id:

            site_code = self.site.code  # MNH / ORC

            # Get last subject for this site
            last_subject = Subject.objects.filter(
                site=self.site,
                subject_id__startswith=site_code
            ).order_by("-subject_id").first()

            if last_subject:
                last_number = int(last_subject.subject_id.split("-")[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.subject_id = f"{site_code}-{str(new_number).zfill(3)}"

        super().save(*args, **kwargs)
        
    # ----------------------------
    # STATUS (FIXED)
    # ----------------------------
    @property
    def status(self):

        screening = getattr(self, "screening", None)

        if screening:

            enrollment = getattr(screening, "enrollment", None)

            if enrollment:

                # ✅ Check termination FIRST (highest priority)
                if hasattr(enrollment, "termination"):
                    return "terminated"

                return "enrolled"

            return "screened"

        return "registered"

    # ----------------------------
    # PROGRESS (IMPROVED)
    # ----------------------------
    @property
    def progress(self):

        status_map = {
            "registered": 20,
            "screened": 50,
            "enrolled": 80,
            "completed": 100,
        }

        return status_map.get(self.status, 0)

    # ----------------------------
    # OPTIONAL HELPERS (VERY USEFUL)
    # ----------------------------
    @property
    def is_registered(self):
        return self.status == "registered"

    @property
    def is_screened(self):
        return self.status == "screened"

    @property
    def is_enrolled(self):
        return self.status == "enrolled"

    def __str__(self):
        return f"{self.subject_id} - {self.first_name} {self.last_name}"