from django import forms
from herbal.models.crfs.crf1.crf1_model import CRF1

class CRF1Form(forms.ModelForm):

    class Meta:

        model = CRF1

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