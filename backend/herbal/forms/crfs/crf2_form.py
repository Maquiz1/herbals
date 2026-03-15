from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2

class CRF2Form(forms.ModelForm):

    class Meta:

        model = CRF2

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