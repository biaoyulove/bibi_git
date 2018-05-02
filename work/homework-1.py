import pickle


def main():
    try:
        pickle_file = open('mydata.pkl', 'rb')
        info = pickle.load(pickle_file)
        pickle_file.close()
    except:
        info = {'user': 'root', 'psd': '123', 'status': True}

    while info['status']:
        for i in range(3):
            user = input("输入用户名：")
            psd = input("输入密码：")
            if user == info['user'] and psd == info['psd']:
                print('欢迎登陆! ' + user)
                break
            else:
                print('用户名密码错误!')
        info['status'] = False

    pickle_file = open('mydata.pkl', 'wb')
    pickle.dump(info, pickle_file)
    pickle_file.close()


if __name__ == '__main__':
    main()
