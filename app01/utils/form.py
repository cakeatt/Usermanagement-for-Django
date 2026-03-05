from django import forms
from django.core.validators import RegexValidator
from app01 import models
from django.core.validators import ValidationError
from app01.utils.encrypt import md5


class BootStrap:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs.update({
                    'class':'form-control',
                    'placeholder':field.label
                })
            field.widget.attrs={
                'class':'form-control',
                'placeholder':field.label,
            }

class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3,label='姓名')
    #password=forms.CharField(label='密码',widget=forms.PasswordInput)
    class Meta:
        model=models.UserInfo
        fields=['name','password','age','account','create_time','gender','depart']

class NumModelForm(BootStrapModelForm):
    mobile=forms.CharField(
        label='手机号',
        validators=[RegexValidator(regex=r'^1\d{10}$',message='手机号格式错误'),
        ]
    )
    class Meta:
        model=models.PrettyNum
        fields=['mobile','price','level','status']
        # exclude=['level']
        # fields="__all__"


    # def clean(self):
    #     cleaned_data=super().clean()
    #     txt_mobile=cleaned_data.get('mobile')
    #     exists=models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
    #     if exists:
    #         raise ValidationError('手机号已存在')
    #     return cleaned_data
    #     显示在表单顶部

    def clean_mobile(self):
        txt_mobile=self.cleaned_data['mobile']
        exists=models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile
    # 显示在字段旁

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.Admin
        fields="__all__"
        widgets={'password':forms.PasswordInput(render_value=True)}

    def clean_password(self):
        txt_password=self.cleaned_data['password']
        return md5(txt_password)

    def clean_confirm_password(self):
        txt_password=self.cleaned_data['password']
        txt_confirm_password=md5(self.cleaned_data['confirm_password'])
        if txt_password != txt_confirm_password:
            raise ValidationError('两次输入密码不一样')
        return txt_confirm_password

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码',widget=forms.PasswordInput(render_value=True))
    class Meta:
        model=models.Admin
        fields="__all__"
        widgets={'password':forms.PasswordInput(render_value=True)}

    def clean_password(self):
        txt_password=md5(self.cleaned_data['password'])
        if self.instance and self.instance.pk:  # 确认是修改场景
            exists = models.Admin.objects.filter(id=self.instance.pk, password=txt_password).exists()
            if exists:
                raise ValidationError('密码不能与修改前一致')
        return txt_password

    def clean_confirm_password(self):
        txt_password = self.cleaned_data.get('password')
        txt_confirm_password = md5(self.cleaned_data['confirm_password'])
        if txt_password is None:
            return txt_confirm_password
        if txt_password != txt_confirm_password:
            raise ValidationError('两次输入密码不一样')
        return txt_confirm_password

class BootStrapForm(BootStrap,forms.Form):
    pass