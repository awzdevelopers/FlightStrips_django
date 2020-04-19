from django import forms
from app1.models import user,flight,companyList,typeList,DaysOfweek
from datetimepicker.widgets import DateTimePicker
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput
from bootstrap_modal_forms.forms import BSModalForm




class loginForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['username','password']

        widgets = {
            'password':forms.TextInput(attrs={'class':'datepicker','type':'password'}),
            }

    # 'EOBT':



class RegisterForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['name','family','username','password','email','phone','job']

        widgets = {
            'job':forms.TextInput(attrs={'class':'fadeIn second','type':'text','id':'login','placeholder':'job'}),
            'job':forms.TextInput(attrs={'class':'hidden','type':'text','id':'login','placeholder':'job'}),
            }

class PassForm(forms.ModelForm):
    class Meta:
        model=user
        fields=['email']

class flightInfoForm(forms.ModelForm):
    CHOICES=[('Sunday','sun'),
         ('Monday','mon'),('Tuesday','tue'),
              ('Wednesday','wed'),('Thursday','thr'),
                   ('Friday','fri'),('Saturday','sat')]
    company=forms.ModelChoiceField(queryset=companyList.objects.all())
    type=forms.ModelChoiceField(queryset=typeList.objects.all())
    daysOfweek = forms.MultipleChoiceField(choices=CHOICES)

    # DayofWeek=forms.MultipleChoiceField(queryset=flight.objects.get(DayofWeek=CHOICES),widget = forms.CheckboxSelectMultiple)
    class Meta:
        model=flight
        fields=['company','flightNum','level','DepAirport','DesAirport','route','EOBT','type','dateFrom','dateTo','daysOfweek','delay','change','register']
        widgets = {
            'dateFrom':DatePickerInput(attrs={'class':'datepicker'}),
            'dateTo':DatePickerInput(attrs={'class':'datepicker'}),

            # 'EOBT':forms.TimeInput(attrs={'class':'timepicker'}),
            'EOBT':TimePickerInput(attrs={'class': 'timepicker'}),
            'company':forms.TextInput(attrs={'class':'form-control','placeholder':'company name...'}),
            'flightNum':forms.TextInput(attrs={'class':'form-control','placeholder':'flight number...'}),
            'level':forms.TextInput(attrs={'class':'form-control','placeholder':'level...'}),
            'route':forms.TextInput(attrs={'class':'form-control','placeholder':'route...'}),
            'type':forms.TextInput(attrs={'class':'form-control','placeholder':'type of aircraft...'}),
            'DepAirport':forms.TextInput(attrs={'class':'form-control','id':'pwd'}),
            'DesAirport':forms.TextInput(attrs={'class':'form-control','id':'pwd'}),
            'daysOfweek':forms.CheckboxSelectMultiple(attrs={'class':'form-check-input'}),
            'delay':forms.HiddenInput(),
            'change':forms.HiddenInput(),
            'register':forms.HiddenInput(),


        }
        # widgets = {
        #     'company': forms.TextInput(attrs={'class': 'form-control'}),
        # }

        # 'password':forms.TextInput(attrs={'placeholder':'Password'})}
class TypeForm(forms.ModelForm):
    class Meta:
        model=typeList
        fields=['type']
        widgets = {

            'type':forms.TextInput(attrs={'class':'form-control','placeholder':'type name...'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model=companyList
        fields=['company']
        widgets = {

           'company':forms.TextInput(attrs={'class':'form-control','placeholder':'type name...'}),
        }
class delForm(BSModalForm):
    class Meta:
        model=flight
        fields=['company']
