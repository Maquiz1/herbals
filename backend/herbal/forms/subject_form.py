from django import forms
from herbal.models import Subject
from locations.models import Region, District, Ward


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject

        exclude = ["subject_id", "site"]  # auto + calculated

        labels={
            "reg_date":"Registration Date",
            "dob":"Date of Birth",
            "sex":"Sex",
            "hid":"Hospital ID",
            "idn":"ID Number",
        }
        widgets = {
            "reg_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),

            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),

            "sex": forms.Select(attrs={"class": "form-control"}),
            "id_type": forms.Select(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "education_level": forms.Select(attrs={"class": "form-control"}),
            "occupation": forms.Select(attrs={"class": "form-control"}),
            "other_occupation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Specify occupation"
            }),
            "hid": forms.TextInput(attrs={"class": "form-control"}),
            "idn": forms.TextInput(attrs={"class": "form-control"}),

            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "other_phone": forms.TextInput(attrs={"class": "form-control"}),

            "street": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

            # Select2 fields
            "region": forms.Select(attrs={"class": "form-control", "id": "region"}),
            "district": forms.Select(attrs={"class": "form-control", "id": "district"}),
            "ward": forms.Select(attrs={"class": "form-control", "id": "ward"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # AJAX-controlled fields
        self.fields["region"].queryset = Region.objects.none()
        self.fields["district"].queryset = District.objects.none()
        self.fields["ward"].queryset = Ward.objects.none()

        # FIX for POST (validation)
        if self.data:
            region_id = self.data.get("region")
            district_id = self.data.get("district")

            if region_id:
                self.fields["region"].queryset = Region.objects.filter(id=region_id)
                self.fields["district"].queryset = District.objects.filter(region_id=region_id)

            if district_id:
                self.fields["ward"].queryset = Ward.objects.filter(district_id=district_id)

        # FIX for edit mode
        elif self.instance.pk:
            if self.instance.region:
                self.fields["region"].queryset = Region.objects.filter(id=self.instance.region_id)
                self.fields["district"].queryset = District.objects.filter(region=self.instance.region)

            if self.instance.district:
                self.fields["ward"].queryset = Ward.objects.filter(district=self.instance.district)
                
    def clean(self):
        cleaned_data = super().clean()
        occupation = cleaned_data.get("occupation")
        other = cleaned_data.get("other_occupation")

        if occupation and str(occupation.value) == "96" and not other:
            self.add_error("other_occupation", "Please specify occupation")

        return cleaned_data