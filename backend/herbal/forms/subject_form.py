from django import forms
from herbal.models import Subject

class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        fields = [
            "reg_date",
            "first_name",
            "last_name",
            "sex",
            "dob",
            "region",
            "district",
            "ward",
        ]

        widgets = {
            "reg_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "sex": forms.Select(attrs={"class": "form-control"}),

            # 👇 IMPORTANT (we control via AJAX)
            "region": forms.Select(attrs={"class": "form-control", "id": "region"}),
            "district": forms.Select(attrs={"class": "form-control", "id": "district"}),
            "ward": forms.Select(attrs={"class": "form-control", "id": "ward"}),
        }
