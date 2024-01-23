from django.forms import ModelForm
from app1.models import TODO
class TODOform(ModelForm):
    class Meta:
        model=TODO
        fields=['title','status','priority']