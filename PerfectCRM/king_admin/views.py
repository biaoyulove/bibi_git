from django.shortcuts import render, redirect
from king_admin import king_admin
from king_admin.utils import *
from king_admin.forms import create_model_form
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    table_list = king_admin.enabled_admins
    return render(request, 'king_admin/table_index.html', {'table_list': table_list})


def display_table_obj(request, app_name, table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]

    # 判断 king_admin_actions
    if request.method == "POST":
        # print(request.POST)
        action = request.POST.get('action')
        selected_ids = request.POST.get('selected_ids')
        if selected_ids:
            selected_objects = admin_class.model.objects.filter(id__in=selected_ids.split(','))
        else:
            raise KeyError("No object selected.")
        if hasattr(admin_class, action):
            action_func = getattr(admin_class, action)
            # 调用 king_admin_actions
            request._kingadmin_action = action
            return action_func(admin_class, request, selected_objects)

    # object_list = admin_class.model.objects.all()
    object_list, filter_condtions = table_filter(request, admin_class)  # 过滤后的结果
    # print(type(object_list), '--->', object_list)
    object_list = table_search(request, admin_class, object_list)
    # print(type(object_list), '--->', object_list)
    object_list, orderby_key = table_sort(request, admin_class, object_list)  # 排序后的结果
    # print("orderby key ", orderby_key)
    paginator = Paginator(object_list, admin_class.list_per_page)  # Show 20 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)
    return render(request, "king_admin/table_objs.html", {"admin_class": admin_class,
                                                          "query_sets": query_sets,
                                                          "filter_condtions": filter_condtions,
                                                          "orderby_key": orderby_key,
                                                          "previous_orderby": request.GET.get("o", ''),
                                                          "search_text": request.GET.get('_q', '')})


def table_obj_change(request, app_name, table_name, obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    dynamic_form = create_model_form(admin_class)

    if request.method == 'GET':
        form_obj = dynamic_form(instance=obj)

    else:
        form_obj = dynamic_form(request.POST, instance=obj)
        if form_obj.is_valid():
            print(form_obj.cleaned_data)
            form_obj.save()
            return redirect(to='table_obj', app_name=app_name, table_name=table_name)

    return render(request, 'king_admin/table_obj_change.html', {'form_obj': form_obj,
                                                                'admin_class': admin_class,
                                                                'app_name': app_name,
                                                                'table_name': table_name})


def table_obj_add(request, app_name, table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    setattr(admin_class, 'is_add_form', True)
    dynamic_form = create_model_form(admin_class)

    if request.method == 'GET':
        form_obj = dynamic_form()
        return render(request, 'king_admin/table_obj_add.html', {'form_obj': form_obj,
                                                                 'admin_class': admin_class})

    elif request.method == 'POST':
        form_obj = dynamic_form(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace('/add/', '/'))
        else:
            return render(request, 'king_admin/table_obj_add.html', {'form_obj': form_obj})


def table_obj_delete(request, app_name, table_name, delete_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=delete_id)
    error_msg = ""
    if admin_class.readonly_table:
        error_msg = "this table is readonly! don't delete!"

    if request.method == "POST":
        if not admin_class.readonly_table:
            obj.delete()
            return redirect('/king_admin/%s/%s/' % (app_name, table_name))
        else:
            error_msg = "this table is readonly! don't delete!"

    return render(request, 'king_admin/table_obj_delete.html', {'obj': [obj, ],
                                                                'admin_class': admin_class,
                                                                'app_name': app_name,
                                                                'table_name': table_name,
                                                                'error_msg': error_msg})
