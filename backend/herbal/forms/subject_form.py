from django import forms
from herbal.models import Subject
from locations.models import Region,District,Ward

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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 IMPORTANT: prevent loading all data
        self.fields["region"].queryset = Region.objects.none()
        self.fields["district"].queryset = District.objects.none()
        self.fields["ward"].queryset = Ward.objects.none()
