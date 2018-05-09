from crm import models
from django.shortcuts import render, redirect


enabled_admins = {}


class BaseAdmin:
    list_display = []
    list_filters = []
    search_fields = []
    filter_horizontal = []  # 多选框
    list_per_page = 20
    ordering = None
    actions = ['delete_selected_objects', ]
    readonly_fields = []
    readonly_table = False  # 整页只读

    def delete_selected_objects(self, request, queryset):
        # print(self, request, queryset)
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name

        # 删除提交
        error_msg = ""
        if not self.readonly_table:
            if request.POST.get('delete_confirm') == 'true':
                queryset.delete()
                return redirect("/king_admin/%s/%s/" % (app_name, table_name))
        else:
            error_msg = "this table is readonly! don't delete!"

        selected_ids = ','.join([str(i.id) for i in queryset])
        action = request._kingadmin_action

        return render(request, 'king_admin/table_obj_delete.html', {'obj': queryset,
                                                                    'admin_class': self,
                                                                    'app_name': app_name,
                                                                    'table_name': table_name,
                                                                    'selected_ids': selected_ids,
                                                                    'action': action,
                                                                    'error_msg': error_msg})

    def default_form_validation(self):
        """
        用户自定义form验证，重写此方法.
        :return: ValidationError
        """
        pass

    """def clean_(field_name) (self):对单个字段验证."""
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name:
            return name
        else:
            self.add_error('name', "can't be null")


class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status', 'user_custom']
    list_filters = ['source', 'consultant', 'consult_course', 'status']
    search_fields = ['qq', 'name', "consultant__name"]
    filter_horizontal = ['tags']
    list_per_page = 5
    readonly_fields = ['qq', 'consultant', 'tags']
    readonly_table = True

    def user_custom(self):
        """用户自定义显示字段"""
        return '用户自定义显示字段'

    user_custom.display_name = '自定义显示字段'


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


class RoleAdmin(BaseAdmin):
    list_display = ('name', 'menus')


class UserProfileAdmin(BaseAdmin):
    list_display = ('user', 'name', 'roles')


def register(model_class, admin_class):
    """
    king_admin 注册函数
    type model_class: django.db.models.base.ModelBase
    """
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {}

    admin_class.model = model_class
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class


"""king_admin 注册"""
register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdmin)
register(models.Role, RoleAdmin)
register(models.UserProfile, UserProfileAdmin)
