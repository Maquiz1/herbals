from django import forms
from herbal.models import Subject


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "subject_id",
            "site",
            "first_name",
            "last_name",
            "sex",
            "date_of_birth",
        ]

        widgets = {
            "subject_id": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.Select(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "sex": forms.Select(attrs={"class": "form-control"}),
            # "age_eligible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            # "inclusion_criteria_met": forms.CheckboxInput(
            #     attrs={"class": "form-check-input"}
            # ),
            # "exclusion_criteria_present": forms.CheckboxInput(
            #     attrs={"class": "form-check-input"}
            # ),
            # "eligible": forms.Select(attrs={"class": "form-control"}),
            # "eligible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            # "comments": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

        # def clean_age_eligible(self):

        #     age_eligible = self.cleaned_data["age_eligible"]

        #     if not age_eligible:
        #         raise forms.ValidationError(
        #             "Subject must be ≥18 years to proceed."
        #         )

        #     return age_eligible
