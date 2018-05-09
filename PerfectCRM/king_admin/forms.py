from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext as _


def create_model_form(admin_class):
    """动态生成MODEL FORM"""
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

            if not hasattr(admin_class, 'is_add_form'):
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

            if hasattr(admin_class, 'clean_%s' % field_name):
                field_clean_func = getattr(admin_class, 'clean_%s' % field_name)
                setattr(cls, 'clean_%s' % field_name, field_clean_func)

        return ModelForm.__new__(cls)

    def default_clean(self):
        error_list = []

        # readonly_table check
        if admin_class.readonly_table:
            raise ValidationError(
                _('Table is  readonly,cannot be modified or added'),
                code='invalid'
            )

        if self.instance.id:  # 这是个修改的表单
            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance, field)  # val in db
                if hasattr(field_val, 'select_related'):  # m2m
                    m2m_obj = getattr(field_val, 'select_related')()
                    set_m2m_val = set([i[0] for i in m2m_obj.values_list('id')])
                    set_field_val_from_frontend = set([i.id for i in self.cleaned_data.get(field)])
                    # print('set_m2m_val', set_m2m_val, 'set_field_val_from_frontend', set_field_val_from_frontend)
                    if set_m2m_val != set_field_val_from_frontend:
                        error_list.append(ValidationError(
                            _('field %(field)s is readonly'),
                            code='invalid',
                            params={'field': field}
                        ))
                    continue

                field_val_from_frontend = self.cleaned_data.get(field)
                if field_val != field_val_from_frontend:
                    error_list.append(ValidationError(
                        _('field %(field)s is readonly'),
                        code='invalid',
                        params={'field': field}
                    ))

        # 调用用户自定义验证方法
        response = admin_class.default_form_validation(self)
        if response:
            error_list.append(response)

        if error_list:
            raise ValidationError(error_list)

    class Meta:
        model = admin_class.model
        fields = "__all__"

    attr = {'Meta': Meta, 'clean': default_clean}
    _model_form_class = type("DynamicModelForm", (ModelForm,), attr)
    setattr(_model_form_class, '__new__', __new__)

    return _model_form_class
