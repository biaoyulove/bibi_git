import pickle

goods = [
{"name": "电脑", "price": 1999},
{"name": "鼠标", "price": 10},
{"name": "游艇", "price": 20},
{"name": "美女", "price": 998},
]

try:
    pickle_file = open('mydata.pkl', 'rb')
    user_dict = pickle.load(pickle_file)
    pickle_file.close()
except:
    user_dict = {}

things_list = []

status = True

while status:
    print('***注册或登录,输入back退出!***')
    user = input('用户名: ').strip()
    psd = input('密码: ').strip() 
    if user == 'back' or psd == 'back':
        break
    else:
        if user_dict.get(user):
            if user_dict[user]['psd'] == psd:
                print('用户已登录!')
                user_dict[user]['state'] = True
            else:
                print('密码错误.')
                continue
        else:
            salary = input('薪水: ').strip()
            if not salary.isdigit():
                print('非法字符!')
                continue
            else:
                salary = int(salary)
            user_dict[user] = {'psd': psd, 'salary': salary, 'state': True, 'records':[]}
            print('用户已注册!')
        while user_dict[user]['state']:
            print('\n', '商品列表'.center(50, '*'))
            print('商品ID，商品列表，商品售价')
            for k, v in enumerate(goods):
                print('%s %s:%s元 ' % (k, v['name'], v['price']))
            print('输入要购买的商品，也可以为id>>>')
            while True:
                tag = input('商品或编号: ')
                if tag == 'back':
                    print('消费记录'.center(25, '*'))
                    for record in user_dict[user]['records']:
                        print(record)
                    print('\033[1;31;40m余额:%s\033[0m' % user_dict[user]['salary'])
                    user_dict[user]['state'] = False
                    status = False
                    pickle_file = open('mydata.pkl', 'wb')
                    pickle.dump(user_dict, pickle_file)
                    pickle_file.close()
                    break
                if tag.isdigit():
                    tag = int(tag)
                    if tag > len(goods):
                        print('\033[1;31;40m商品不存在！\033[0m')
                        continue
                    if goods[tag]['price'] <= user_dict[user]['salary']:
                        user_dict[user]['salary'] -= goods[tag]['price']
                        things_list.append(goods[tag]['name'])
                        user_dict[user]['records'].append('购买%s商品，消费%s元.' % (goods[tag]['name'], goods[tag]['price']))
                        print('\033[1;31;40m商品已购买\033[0m')
                    else:
                        print('\033[1;31;40m余额不足！\033[0m')
                        continue
                else:
                    for v in goods:
                        if tag == v['name']:
                            if v['price'] <= user_dict[user]['salary']:
                                user_dict[user]['salary'] -= v['price']
                                things_list.append(v['name'])
                                user_dict[user]['records'].append('购买%s商品，消费%s元.' % (v['name'], v['price']))
                                print('商品已购买\n')
                                break
                            else:
                                print('\033[1;31;40m余额不足！\033[0m')
                                break 
                    


                    
            

