from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }
        )
    )
    password = forms.CharField(
        max_length=100, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }
        )
    )
