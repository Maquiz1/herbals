from django import forms
from herbal.models.crfs.crf7.crf7_model import CRF7

class CRF7Form(forms.ModelForm):

    class Meta:

        model = CRF7

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