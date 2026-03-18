# herbal/models/subjects/subject_model.py
from django.db import models
from datetime import date

from sites.models import Site
from choices.models.sex_model import Sex
from core.models import BaseModel
from core.managers.site_manager import SiteRestrictedManager


class Subject(BaseModel):
    
    subject_id = models.CharField(max_length=50, unique=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)

    reg_date = models.DateField()
    dob = models.DateField(null=True,blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    
    sex = models.ForeignKey(Sex, on_delete=models.PROTECT)
    
    hid = models.CharField(max_length=100)
    idn = models.CharField(max_length=100, blank=True, null=True)
    id_type = models.CharField(
        max_length=50,
        choices=[
            ("NIDA", "NIDA"),
            ("VOTER", "Voter ID"),
            ("PASSPORT", "Passport"),
            ("LICENSE", "DRIVING LICENSE"),
            ("OTHER", "Other"),
        ],
        blank=True,
        null=True
    )

    marital_status = models.CharField(
        max_length=20,
        choices=[
            ("single", "Single"),
            ("married", "Married"),
            ("divorced", "Divorced"),
            ("separated", "Separated"),
            ("widowed", "Widowed/Widower"),
            ("cohabit", "Cohabit"),
        ],
        blank=True,
        null=True
    )

    education_level = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    occupation = models.CharField(max_length=150, blank=True, null=True)
    
    phone_number = models.CharField(max_length=20)
    other_phone = models.CharField(max_length=20, blank=True, null=True)

    # Location fields (you may later convert to FK if using location models)
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

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