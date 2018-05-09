from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist


register = template.Library()


@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()


@register.simple_tag
def build_table_row(request, obj, admin_class):
    # print(request.path)
    row_ele = ""
    for index, column in enumerate(admin_class.list_display):
        try:
            field_obj = obj._meta.get_field(column)
            if field_obj.choices:  # choices type
                column_data = getattr(obj, "get_%s_display" % column)()
            else:
                column_data = getattr(obj, column)

            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

            if index == 0:  # add a tag, 可以跳转到修改页
                column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                           obj_id=obj.id,
                                                                                           data=column_data)
        except FieldDoesNotExist:
            if hasattr(admin_class, column):
                column_obj = getattr(admin_class, column)
                column_data = column_obj()
            else:
                column_data = '未定义'
        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)


@register.simple_tag
def build_paginator(query_sets, filter_condtions, previous_orderby, search_text):
    temp = '<ul class="pagination">'
    filter_ele = ''

    for k, v in filter_condtions.items():
        filter_ele += '&%s=%s' % (k, v)

    if query_sets.has_previous():
        temp += '<li ><a href="?page=%s%s&o=%s&_q=%s">上页</a></li>' % (query_sets.previous_page_number(), filter_ele, previous_orderby, search_text)

    for loop_counter in query_sets.paginator.page_range:
        ele_class = ''

        if loop_counter == query_sets.number:
            ele_class = 'active'

        temp += '<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>' % (ele_class, loop_counter, filter_ele, previous_orderby, search_text, loop_counter)

    if query_sets.has_next():
        temp += '<li ><a href="?page=%s%s&o=%s&_q=%s">下页</a></li>' % (query_sets.next_page_number(), filter_ele, previous_orderby, search_text)

    temp += '</ul>'

    return mark_safe(temp)


@register.simple_tag
def render_filter_ele(condtion, admin_class, filter_condtions):
    # print('filter_condtions :', filter_condtions) # filter_condtions: {'status': '1', 'source': '2'}
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' % condtion
    field_obj = admin_class.model._meta.get_field(condtion)
    if field_obj.choices:
        # print(field_obj.choices)
        selected = ''
        for choice_item in field_obj.choices:
            # print("choice", choice_item, filter_condtions.get(condtion), type(filter_condtions.get(condtion)))
            # choice (2, '官网') None <class 'NoneType'>
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"

            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def build_table_header_column(column, orderby_key, filter_condtions, admin_class):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k, v)

    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
        {sort_icon}
        </th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down"></span>'''

        if orderby_key.strip("-") == column:  # 排序的就是这个字段
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''

    else:  # 没有排序
        orderby_key = column
        sort_icon = ''

    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name.upper()
    except FieldDoesNotExist:
        column_verbose_name = getattr(admin_class, column).display_name.upper()
        ele = '''<th><a href="javascript:void(0);">{column}</a>'''.format(column=column_verbose_name)
        return mark_safe(ele)

    ele = ele.format(orderby_key=orderby_key, column=column_verbose_name, sort_icon=sort_icon, filters=filters)
    return mark_safe(ele)


@register.simple_tag
def get_m2m_obj_list(admin_class, field, form_obj):
    """返回m2m所有待选数据"""

    """数据库字段对象"""
    field_obj = getattr(admin_class.model, field.name)
    all_obj_list = field_obj.rel.model.objects.all()
    """被修改用户字段对象"""
    if form_obj.instance.id:
        select_obj = getattr(form_obj.instance, field.name)
        all_select_list = select_obj.all()
    else:  # 表示创建新数据
        return all_obj_list

    select_obj_list = []
    for obj in all_obj_list:
        if obj not in all_select_list:
            select_obj_list.append(obj)

    return select_obj_list


@register.simple_tag
def get_m2m_selected_obj_list(form_obj, field):
    """获取m2m已选选项"""
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field.name)
        return field_obj.all()
    else:  # 表示创建新数据
        return None


@register.simple_tag
def print_obj_methods(obj):
    print(obj)


@register.simple_tag
def display_all_related_obj(objs):
    if objs:
        return mark_safe(iteration_related_obj_query(objs))


def iteration_related_obj_query(obj_list):
    ul_ele = "<ul>"
    for obj in obj_list:
        li_ele = '<li> %s: %s </li>' % (obj._meta.verbose_name, obj.__str__().strip("<>"))
        ul_ele += li_ele

        # 循环 many_to_many
        for m2m_obj in obj._meta.local_many_to_many:
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj, m2m_obj.name)
            for v in m2m_field_obj.all():  # 把所有跟这个对象直接关联的m2m字段取出来了
                sub_li_ele = "<li>%s : %s</li>" % (m2m_obj.verbose_name, v.__str__().strip('<>'))
                sub_ul_ele += sub_li_ele
            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele

        # 循环one_to_many
        for related_obj in obj ._meta.related_objects:
            # print(related_obj.__repr__())
            if 'ManyToManyRel' in related_obj.__repr__():
                if hasattr(obj, related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # select_related() == all()
                        target_obj = accessor_obj.select_related()
                        # print(target_obj)
                        # target_obj 相当于 customer.enrollment_set.all()
                        mto_ul_ele = "<ul style='color:red'>"
                        for u in target_obj:
                            mto_li_ele = '''<li> %s: %s </li>''' % (u._meta.verbose_name, u.__str__().strip("<>"))
                            mto_ul_ele += mto_li_ele
                        mto_ul_ele += "</ul>"
                        ul_ele += mto_ul_ele

            elif hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                # print(accessor_obj)
                # 上面accessor_obj 相当于 customer.enrollment_set
                if hasattr(accessor_obj, 'select_related'):  # select_related() == all()
                    target_obj = accessor_obj.select_related()
                    # print('hasattr', target_obj)
                else:
                    target_obj = accessor_obj
                    # print('nohasattr', target_obj)

                # 递归
                if len(target_obj) > 0:
                    # print('递归', target_obj)
                    node = iteration_related_obj_query(target_obj)
                    ul_ele += node

    ul_ele += "</ul>"

    return ul_ele


@register.simple_tag
def get_action_verbose(admin_class, action):
    if hasattr(admin_class, action):
        action_func = getattr(admin_class, action)
        return action_func.display_name if hasattr(action_func, 'display_name') else action_func.__name__


@register.simple_tag
def back_url_host(request, url):
    return request+url


@register.simple_tag
def back_a_tag(app_name, table_name):
    """重写/king_admin/index/ 下的 ,<a>标签的 href. 因为通过URL别名获取href产生错误."""
    url = "/king_admin/%s/%s/" % (app_name, table_name)
    print(url)
    return url
