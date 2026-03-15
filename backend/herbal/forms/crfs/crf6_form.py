from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6

class CRF6Form(forms.ModelForm):

    class Meta:

        model = CRF6

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