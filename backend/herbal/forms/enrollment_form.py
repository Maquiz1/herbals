from django import forms
from herbal.models import Enrollment


class EnrollmentForm(forms.ModelForm):

    class Meta:

        model = Enrollment

        fields = [
            "enrollment_date",
            "consent_signed",
            "enrolled_by",
            "status",
        ]

        widgets = {

            "enrollment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),

            "consent_signed": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

            "enrolled_by": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "status": forms.Select(
                attrs={"class": "form-control"}
            ),

        }