# -*- coding: utf-8 -*-

import json

import requests
from django import forms
from django.conf import settings

DEFAULT_AMAZON_ML_ENDPOINT="https://realtime.machinelearning.us-east-1.amazonaws.com"

EMP_LENGTH_CHOICES = (
    (0.0, "無し"),
    (0.5, "1年未満"),
    (1.0, "満1年"),
    (2.0, "満2年"),
    (3.0, "満3年"),
    (4.0, "満4年"),
    (5.0, "満5年"),
    (6.0, "満6年"),
    (7.0, "満7年"),
    (8.0, "満8年"),
    (9.0, "満9年"),
    (10.0, "10年以上"),
)

HOME_OWNERSHIP_CHOICES = (
    ("0", "賃貸"),
    ("1", "持ち家"),
    ("2", "持ち家(抵当)"),
    ("3", "その他"),
)

TERM_CHOICES = (
    ("36", "36ヶ月"),
    ("60", "60ヶ月"),
)

PURPOSE_CHOICES = (
    ("0", "car"),
    ("1", "credit_card"),
    ("2", "debt_consolidation"),
    ("3", "home_improvement"),
    ("4", "house"),
    ("5", "major_purchase"),
    ("6", "medical"),
    ("7", "moving"),
    ("8", "renewable_energy"),
    ("9", "small_business"),
    ("10", "vacation"),
    ("11", "other"),
)

class ExaminationForm(forms.Form):
    loan_amnt = forms.DecimalField(
        label="ご希望の融資額($)",
        min_value=0,
        max_value=100000,
        required=True,
        widget=forms.NumberInput()
    )
    term = forms.ChoiceField(
        label="ご希望の支払い回数($)",
        choices=TERM_CHOICES,
        required=True,
        widget=forms.Select()
    )
    purpose = forms.ChoiseField(
        label="目的",
        choices=PURPOSE_CHOICES,
        required=True,
        widget=forms.Select()
    )
    emp_title = forms.CharField(
        label="職種",
        max_length=60,
        required=False,
        widget=forms.TextInput()
    )
    emp_length = forms.ChoiceField(
        label="勤続年数",
        choices=EMP_LENGTH_CHOICES,
        required=True,
        widget=forms.Select()
    )
    annual_inc = forms.DecimalField(
        label="年収($)",
        min_value=0,
        required=True,
        widget=forms.NumberInput()
    )
    home_ownership = forms.ChoiceField(
        label="自宅の所有状況",
        choices=HOME_OWNERSHIP_CHOICES,
        required=True,
        widget=forms.Select()
    )

    def predict_loan_status(self):
        model_id = getattr(settings, "AMAZON_ML_MODEL_ID")
        amazon_ml_endpoint = getattr(settings, "AMAZON_ML_ENDPOINT", DEFAULT_AMAZON_ML_ENDPOINT)
        api_gateway_endpoint = getattr(settings, "API_GATEWAY_ENDPOINT")
        payload = {
            "MLModelId": model_id,
            "PredictEndpoint": amazon_ml_endpoint,
            "Record": {
                "loan_amnt": str(self.cleaned_data['loan_amnt']),
                "term":self.cleaned_data['term'],
                "purpose":self.cleaned_data['purpose'],
                "emp_title": self.cleaned_data['emp_title'],
                "emp_length": self.cleaned_data['emp_length'],
                "annual_inc": str(self.cleaned_data['annual_inc']),
                "home_ownership": self.cleaned_data['home_ownership'],
            }
        }
        response = requests.post(api_gateway_endpoint, data=json.dumps(payload))
        return response.json()
