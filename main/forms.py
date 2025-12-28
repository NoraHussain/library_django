from django import forms
from django.core.mail import send_mail

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

class ContactForm(forms.Form):

    # 1. Fields
    
    name = forms.CharField(
        max_length=100,
        min_length=3,
        required=True,
        label="Full Name",
        help_text="Enter your real name",
        initial="Guest",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your name"
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email address"
        })
    )

    message = forms.CharField(
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "class": "form-control",
            "placeholder": "Write your message"
        })
    )

    # TextInput
    # Textarea
    # EmailInput
    # PasswordInput
    # NumberInput
    # DateInput
    # CheckboxInput
    # Select
    # RadioSelect

    agree = forms.BooleanField(required=True, initial=True, disabled=True)

    
    # 2. Field-level validation
    
    def clean_message(self):
        message = self.cleaned_data.get("message") # after is_valid()

        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters")

        if "spam" in message.lower():
            raise forms.ValidationError("Spam content detected")

        return message
    
    
    
    # 3. Cross-field validation
    
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        message = cleaned_data.get("message")

        if name and email and message and name.lower() in message.lower():
            raise forms.ValidationError(
                "Name should not be part of the message"
            )

        return cleaned_data

    
    # 4. Override save-like logic
    
    def process(self):
        """
        Custom method (not Django built-in)
        Used for business logic after validation
        """
        print("Sending Mails .... ")

        # send_mail(
        #     subject="Contact Form Submission",
        #     message=self.cleaned_data["message"],
        #     from_email=self.cleaned_data["email"],
        #     recipient_list=["nora.hussain.1999@gmail.com"],
        #     fail_silently=False,
        # )

        return self.cleaned_data
