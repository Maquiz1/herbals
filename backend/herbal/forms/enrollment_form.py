# herbal/forms/enrollment_form.py

from django import forms
from herbal.models import Enrollment


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment

        fields = [
            "enrollment_date",
            "pt_category",
            "pt_type",
            "treatment_type",
            "previous_date",
            "total_cycle",
            "cycle_number",
            "status",
        ]

        widgets = {
            "enrollment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),

            "pt_category": forms.Select(
                attrs={"class": "form-select"}
            ),

            "pt_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "treatment_type": forms.Select(
                attrs={"class": "form-select"}
            ),

            "previous_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),

            "total_cycle": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),

            "cycle_number": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    # =========================
    # ✅ CLEAN VALIDATION
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        pt_type = cleaned_data.get("pt_type")
        previous_date = cleaned_data.get("previous_date")

        total_cycle = cleaned_data.get("total_cycle")
        cycle_number = cleaned_data.get("cycle_number")

        # ✅ Follow-up must have previous date
        if pt_type == "follow_up" and not previous_date:
            self.add_error(
                "previous_date",
                "Previous date is required for follow-up patients."
            )

        # ✅ Cycle logic
        if total_cycle and cycle_number:
            if cycle_number > total_cycle:
                self.add_error(
                    "cycle_number",
                    "Cycle number cannot exceed total cycles."
                )

        return cleaned_data