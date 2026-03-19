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
        
        # 🔥 FIX: when form is submitted
        if self.data:
            region_id = self.data.get("region")
            district_id = self.data.get("district")

            if region_id:
                self.fields["region"].queryset = Region.objects.filter(id=region_id)
                self.fields["district"].queryset = District.objects.filter(region_id=region_id)

            if district_id:
                self.fields["ward"].queryset = Ward.objects.filter(district_id=district_id)

        # 🔥 FIX: when editing existing object
        elif self.instance.pk:
            self.fields["region"].queryset = Region.objects.filter(id=self.instance.region_id)
            self.fields["district"].queryset = District.objects.filter(region=self.instance.region)
            self.fields["ward"].queryset = Ward.objects.filter(district=self.instance.district)
