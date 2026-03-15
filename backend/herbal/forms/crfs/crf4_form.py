from django import forms
from herbal.models.crfs.crf4.crf4_model import CRF4

class CRF4Form(forms.ModelForm):

    class Meta:

        model = CRF4

        fields = [
            "temperature",
            "blood_pressure",
            "notes",
        ]

        widgets = {

            "temperature": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "blood_pressure": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "notes": forms.Textarea(
                attrs={"class": "form-control"}
            ),
        }