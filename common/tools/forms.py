from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from common.models import search_results


class COBDateForm(forms.Form):
    cob_date = forms.DateField(
        label="COB Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )


class SearchResultsForm(forms.ModelForm):
    class Meta:
        model = search_results

        fields = [
            'symbol', 'symbol_name', 'country_code', 'trade_type',
            'scan_source', 'scan_name', 'scan_cob_date', 
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False  # 🔓 Make all fields optional

        self.helper = FormHelper()
        self.helper.form_method = 'get'  # or 'post' if needed
        self.helper.layout = Layout(
            Row(
                Column('symbol', css_class='col-md-3'),
                Column('symbol_name', css_class='col-md-3'),
                Column('country_code', css_class='col-md-3'),
                Column('trade_type', css_class='col-md-3'),
            ),
            Row(
                Column('scan_source', css_class='col-md-3'),
                Column('scan_name', css_class='col-md-3'),
                Column('scan_cob_date', css_class='col-md-3'),

            ),
            Row(
                Column(Submit('submit', '🔍 Filter', css_class='btn btn-primary'), css_class='col-md-4'),
                Column(HTML('<button type="submit" name="export" class="btn btn-success">📤 Export CSV</button>'), css_class='col-md-4'),
                Column(HTML('<a href="?" class="btn btn-outline-secondary">♻️ Reset Filters</a>'), css_class='col-md-4'),
            )
        )
   