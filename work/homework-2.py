menu = {
    '北京':{
        '海淀':{
            '五道口':{
                'soho':{},
                '网易':{},
                'google':{}
            },
            '中关村':{
                '爱奇艺':{},
                '汽车之家':{},
                'youku':{},
            },
            '上地':{
                '百度':{},
            },
        },
        '昌平':{
            '沙河':{
                '老男孩':{},
                '北航':{},
            },
            '天通苑':{},
            '回龙观':{},
        },
        '朝阳':{},
        '东城':{},
    },
    '上海':{
        '闵行':{
            "人民广场":{
                '炸鸡店':{}
            }
        },
        '闸北':{
            '火车战':{
                '携程':{}
            }
        },
        '浦东':{},
    },
    '山东':{},
}

menu_state = [menu,]
while True:
    for k in menu_state[-1]:
        print('输入->%s<-进入子菜单; ' % k)
    print('\n输入->back<-返回上一层; ', '\n输入->exit<-退出. ')
    tag = input('\n请输入:')
    if tag in menu_state[-1]:
        menu_state.append(menu_state[-1][k])
    elif tag == 'back':
        if menu_state[-1] != menu:
            menu_state.pop()
        else:print('无上级菜单.')
    elif tag == 'exit':break
    else:
        print('无效输入.')
            
