from django import forms

class RegisterForm(forms.Form):
    
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), 
                               required=True)
    verify_password = forms.CharField(widget=forms.PasswordInput(), 
                                      required=True)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        verify_password = cleaned_data.get('verify_password')
        if password!=verify_password:
            self.errors['verify_password'] = \
                            self.error_class(['Passwords do not match'])
            del self.cleaned_data['password']
        del self.cleaned_data['verify_password']
        return cleaned_data


class UserVerifyForm(forms.Form):
    username = forms.CharField()
    confirmation_code = forms.CharField(required=True, max_length=6,
                                        label="Verification Code")