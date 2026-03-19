# herbal/forms/screening_form.py

from django import forms
from herbal.models import Screening, YesNoChoices


class ScreeningForm(forms.ModelForm):

    class Meta:
        model = Screening

        fields = [
            # Core
            "screening_date",

            # Consent
            "consent",
            "consent_date",
            "consent_reasons",

            "consent_nimregenin",
            "nimregenin_date",
            "nimregenin_reasons",

            # Inclusion
            "age_18",
            "biopsy",
            "breast_cancer",
            "brain_cancer",
            "cervical_cancer",
            "prostate_cancer",

            # Exclusion
            "pregnant",
            "breast_feeding",
            "ckd",
            "liver_disease",

            # Notes
            "remarks",
        ]

        labels={
            "age_18":"Aged eighteen years and above",
            "biopsy":"Confirmed cancer with biopsy?",
            "consent":"Did the participant consent to be part of the study?",
            "consent_nimregenin":"Did the participant consent to use NIMREGENIN preparation?",
        }
        widgets = {
            # Date fields
            "screening_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "consent_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "nimregenin_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            # Select fields
            "consent": forms.Select(attrs={"class": "form-select"}),
            "consent_nimregenin": forms.Select(attrs={"class": "form-select"}),
            "age_18": forms.Select(attrs={"class": "form-select"}),
            "biopsy": forms.Select(attrs={"class": "form-select"}),
            "breast_cancer": forms.Select(attrs={"class": "form-select"}),
            "brain_cancer": forms.Select(attrs={"class": "form-select"}),
            "cervical_cancer": forms.Select(attrs={"class": "form-select"}),
            "prostate_cancer": forms.Select(attrs={"class": "form-select"}),

            "pregnant": forms.Select(attrs={"class": "form-select"}),
            "breast_feeding": forms.Select(attrs={"class": "form-select"}),
            "ckd": forms.Select(attrs={"class": "form-select"}),
            "liver_disease": forms.Select(attrs={"class": "form-select"}),

            # Text areas
            "consent_reasons": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "nimregenin_reasons": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        subject = getattr(self.instance, "subject", None)
        sex = subject.sex_id if subject else None

        # =========================
        # ✅ BASE REQUIRED FIELDS (COMMON)
        # =========================
        required_fields = [
            "screening_date",
            "consent",
            "consent_nimregenin",
            "age_18",
            "biopsy",
            "breast_cancer",
            "brain_cancer",
            "ckd",
            "liver_disease",
        ]

        for field in required_fields:
            self.fields[field].required = True

        # =========================
        # 👨 MALE RULES
        # =========================
        if sex == 1:
            self.fields["prostate_cancer"].required = True

            self.fields["cervical_cancer"].required = False
            self.fields["pregnant"].required = False
            self.fields["breast_feeding"].required = False

        # =========================
        # 👩 FEMALE RULES
        # =========================
        elif sex == 2:
            self.fields["cervical_cancer"].required = True
            self.fields["pregnant"].required = True
            self.fields["breast_feeding"].required = True

            self.fields["prostate_cancer"].required = False

    # =========================
    # ✅ CLEAN LOGIC
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        consent = cleaned_data.get("consent")
        consent_date = cleaned_data.get("consent_date")
        consent_reasons = cleaned_data.get("consent_reasons")

        nimr = cleaned_data.get("consent_nimregenin")
        nimr_date = cleaned_data.get("nimregenin_date")
        nimr_reasons = cleaned_data.get("nimregenin_reasons")

        # =========================
        # ✅ CONSENT VALIDATION
        # =========================
        if consent == YesNoChoices.YES and not consent_date:
            self.add_error("consent_date", "Consent date is required if consent is Yes.")

        if consent == YesNoChoices.NO and not consent_reasons:
            self.add_error("consent_reasons", "Reason is required if consent is No.")

        # =========================
        # ✅ NIMREGENIN VALIDATION
        # =========================
        if nimr == YesNoChoices.YES and not nimr_date:
            self.add_error(
                "nimregenin_date",
                "Date is required if consent to use NIMREGENIN is Yes."
            )

        if nimr == YesNoChoices.NO and not nimr_reasons:
            self.add_error(
                "nimregenin_reasons",
                "Reason is required if NIMREGENIN consent is No."
            )

        # =========================
        # ✅ SEX-AWARE CLEANING
        # =========================
        subject = getattr(self.instance, "subject", None)
        sex = subject.sex_id if subject else None

        if sex == 1:  # 👨 Male
            cleaned_data["cervical_cancer"] = None
            cleaned_data["pregnant"] = None
            cleaned_data["breast_feeding"] = None

        elif sex == 2:  # 👩 Female
            cleaned_data["prostate_cancer"] = None

        return cleaned_data