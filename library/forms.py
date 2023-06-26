from django.forms import ModelForm, Textarea

from .models import *


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']
        widgets = {
            "text": Textarea(attrs={"cols": 20, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
