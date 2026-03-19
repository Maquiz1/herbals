# herbal/forms/screening_form.py

from django import forms
from herbal.models import Screening


class ScreeningForm(forms.ModelForm):

    class Meta:
        model = Screening

        fields = [
            # Core
            "screening_date",

            # Consent
            "consented",
            "consent_date",
            "consented_nimregenin",
            "nimregenin_date",
            "reasons",

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

        widgets = {
            # Date fields
            "screening_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "consent_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "nimregenin_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            # Select fields (Yes/No)
            "consented": forms.Select(attrs={"class": "form-select"}),
            "consented_nimregenin": forms.Select(attrs={"class": "form-select"}),
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
            "reasons": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    # =========================
    # ✅ VALIDATIONS
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        consented = cleaned_data.get("consented")
        consent_date = cleaned_data.get("consent_date")

        nimr = cleaned_data.get("consented_nimregenin")
        nimr_date = cleaned_data.get("nimregenin_date")

        # ✅ Consent date required if consented
        if consented == 1 and not consent_date:
            self.add_error("consent_date", "Consent date is required if consent is Yes.")

        # ✅ Nimr consent date required
        if nimr == 1 and not nimr_date:
            self.add_error("nimregenin_date", "Date is required if consented to Use NIMREGENIN is Yes.")

        return cleaned_data