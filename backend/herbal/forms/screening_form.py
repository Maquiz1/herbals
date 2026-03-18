# herbal/forms/screening_form.py

from django import forms
from herbal.models import Screening


class ScreeningForm(forms.ModelForm):

    class Meta:

        model = Screening

        fields = [
            "screening_date",
            "age_eligible",
            "inclusion_criteria_met",
            "exclusion_criteria_present",
            "eligible",
            "comments",
        ]

        widgets = {
            "screening_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "age_eligible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "inclusion_criteria_met": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "exclusion_criteria_present": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "eligible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
        def clean_age_eligible(self):

            age_eligible = self.cleaned_data["age_eligible"]

            if not age_eligible:
                raise forms.ValidationError(
                    "Subject must be ≥18 years to proceed."
                )

            return age_eligible
