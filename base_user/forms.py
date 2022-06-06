from .models import CustomUser
from django import forms

class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Re-Password'}))

    class Meta:
        model = CustomUser
        fields = (
            'email',
        )
    
        widgets = {
            'email':forms.TextInput(attrs={'placeholder':'E-Mail'}),        
        }
        


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password isn't match")
        return password2

    

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

