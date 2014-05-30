from django import forms

class CoupleForm(forms.Form):
    # http://blog.eliacontini.info/post/41598616573/django-set-select-choices-dynamically-in-forms
    def __init__(self, *args, **kwargs):
        c = kwargs.pop('choices')
        super(CoupleForm, self).__init__(*args, **kwargs)
        self.fields["mom"] = forms.ChoiceField(choices=c)
        self.fields["dad"] = forms.ChoiceField(choices=c)