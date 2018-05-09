from django.shortcuts import render


def index(request):
    # role = request.user.userprofile.roles.all()
    # # print(role)  # <QuerySet [<Role: 老师>]>
    # for menu in role[0].menus.all():
    #     print(menu.name, menu.url_name)
    #     """Quit the server with CTRL-BREAK.
    #         客户表
    #         首页"""
    # print(dir(request))
    # print(request.get_host(), request.get_port(), request.path_info)
    return render(request, "index.html")


def customer_list(request):
    return render(request, "sales/customers.html")
