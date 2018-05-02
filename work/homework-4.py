
# coding: utf-8

# In[68]:


import re
import pickle


# In[69]:


def load_data():
    try:
        pickle_file = open('mydata.pkl', 'rb')
        staff_table = pickle.load(pickle_file)
        pickle_file.close()
    except:
        staff_table = [
            {'staff_id': '1', 'name': 'Alex Li', 'age': '24', 'phone': '13651054608', 'dept': 'IT', 'enroll_date': '2013-04-01'},
            {'staff_id': '2', 'name': 'Wang', 'age': '23', 'phone': '15143669585', 'dept': 'MMC', 'enroll_date': '2013-01-11'},
            {'staff_id': '3', 'name': 'Bibi', 'age': '18', 'phone': '17743182560', 'dept': 'LOV', 'enroll_date': '2017-05-21'},
            {'staff_id': '4', 'name': 'Liming', 'age': '19', 'phone': '17743182521', 'dept': 'LOV', 'enroll_date': '2018-05-02'},
            {'staff_id': '5', 'name': 'Aoyu', 'age': '17', 'phone': '13651054608', 'dept': 'LOV', 'enroll_date': '2017-11-11'},
            {'staff_id': '6', 'name': 'King', 'age': '15', 'phone': '13651054608', 'dept': 'K', 'enroll_date': '2010-09-01'},
        ]
    return staff_table

    
def save_data(staff_table):
    pickle_file = open('mydata.pkl', 'wb')
    pickle.dump(staff_table, pickle_file)
    pickle_file.close()
    
    


# In[70]:


def re_compile():
    """re预编译"""
    # 查询预编译
    global re_query_re
    re_query_re = re.compile("find (.*) from staff_table where (.*)(['<','>','=','in'])(.*);")
    
    # 日期查询预编译
    global date_re_com
    date_re_com = re.compile("find (.*) from staff_table where enroll_date like (.*);")

    # 添加预编译
    global re_add_re
    re_add_re = re.compile("add staff_table (.*?);")
    
    # 删除预编译
    global del_data_re
    del_data_re = re.compile("del from staff_table where (.*)(['<','>','=','in'])(.*);")
    
    #更新预编译
    global up_data_re
    up_data_re = re.compile("update staff_table set (.*) where (.*)(['<','>','=','in'])(.*);")
    


# In[71]:


def date_query(query):
    """日期查询"""
    date_query_state = date_re_com.match(query)
    if date_query_state:
        fields = date_query_state.group(1).strip()
        date_state = date_query_state.group(2).strip()
        # 确定要显示的字段
        if '*' in fields:
            fields = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
        else:
            fields = [i.strip() for i in fields.split(',')]
        data_list = fuzzy_query('enroll_date', 'like', date_state)
        print_data(fields, data_list)


# In[72]:


def back_data(query):
   """返回数据"""
   query_state = re_query_re.match(query)
   if query_state:
       try:
           find_list = query_state.group(1).strip()
           fint_const1 = query_state.group(2).strip()
           oper = query_state.group(3).strip()
           fint_const2 = query_state.group(4).strip().strip('"').strip("'")
       except:
           return False
       print(oper)
       # 确定要显示的字段
       if '*' in find_list:
           find_list = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
       else:
           find_list = [i.strip() for i in find_list.split(',')]
           
       # 查询数据     
       back_staff_table = fuzzy_query(fint_const1, oper, fint_const2)
       
       # 输出 显示的字段 or 数据   
       print_data(find_list, back_staff_table)
       return True
   return False

   
def judge_operator(op1, oper, op2):
   """操作符运算"""
   if op1.isdigit():
       op1 = int(op1)
   if op2.isdigit():
       op2 = int(op2)
   if oper == '<':
       return op1 < op2
   elif oper == '>':
       return op1 > op2
   elif oper == '=':
       return op1 == op2
   elif oper == 'like':
       return op2 in op1
   elif oper == 'in':
       return op1 in [p.strip() for p in op2.split(',')]
   
   
def fuzzy_query(constraint1, oper, constraint2):
   """可进行模糊查询"""
   if constraint1 and oper and constraint2:
       back_staff_table = []
       for v in staff_table:
           if judge_operator(v[constraint1], oper, constraint2):
               # 添加符合条件的数据
               back_staff_table.append(v)
       return back_staff_table
   else:
       print('语法错误!')
       return None
   
   
def print_data(find, data):
   """打印数据"""
   ele = ""
   for k in find:
       ele += k.center(15, ' ')
   print(ele)
   for v in data:
       tag = ""
       for i in find:
           tag += v[i].center(15, ' ')
       print(tag)
       


# In[73]:


def add_data(string):
    """增加数据"""
    string_state = re_add_re.match(string)
    if string_state:
        data_str = string_state.group(1).strip()
        data_list = list(data_str.split(','))
        tag_list = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
        
        # 获得自增的数值
        auto_id = int(staff_table[-1]['staff_id']) + 1
        
        data_list.insert(0, str(auto_id))
        if len(tag_list) == len(data_list):
            data_dict = dict(zip(tag_list, data_list))
            # 判断手机号是否唯一
            phone = data_dict['phone']
            if not phone.isdigit():
                print('手机号必须为数字!')
                return False
            else:
                for k in staff_table:
                    if phone == k['phone']:
                        print('手机号必须唯一!')
                        return False
            
            staff_table.append(data_dict)
            print('%s 以添加' % data_dict)
            return True
    print('语法错误!')
    return False


# In[74]:


def del_data(query):
    """删除数据"""
    query_re = del_data_re.match(query)
    if query_re:
        # 提取约束条件
        op1 = query_re.group(1).strip()
        oper = query_re.group(2).strip()
        op2 = query_re.group(3).strip()
        print(query_re.groups())
        # 要删除的数据
        del_data_list = []
        for k in staff_table:
            if judge_operator(k[op1], oper, op2):
                del_data_list.append(k)

        # 输出要删除的数据
        fields = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
        print_data(fields, del_data_list)
        for k in del_data_list:
            staff_table.remove(k)
        print('数据已删除!')
        
        


# In[75]:


def up_data(query):
    status = up_data_re.match(query)
    if status:
        data_str = status.group(1).strip()
        op1 = status.group(2).strip()
        oper = status.group(3).strip()
        op2 = status.group(4).strip()
        
        data_list = data_str.split(',')
        # 要更改的数据
        new_data = []
        for k in data_list:
            new_data.append(k.split('='))
        # 被更改的数据库的数据
        old_data = []
        for k in staff_table:
            if judge_operator(k[op1], oper, op2):
                old_data.append(k)
                # 修改数据
                for v in new_data:
                    k[v[0]] = v[-1]
                
        # 输出要更改的数据
        fields = ['staff_id', 'name', 'age', 'phone', 'dept', 'enroll_date']
        print_data(fields, old_data)
        print('数据被更改!')
        


# In[76]:


def main():
    """语法输入"""
    print("""
    支持以下查询，添加，删除，更新...语法输入.   
    ps('[]'内为查询关键字，where支持 <, >, =, like, in,操作，句尾的 ';' 不要忘记,'[]'不要写.)
    \n find [name,age] from staff_table where [age > 22];
    \n find [*] from staff_table where enroll_date like [2013];
    \n add staff_table [Alex Li,25,134435344,IT,2015‐10‐29];
    \n del from staff_table where [id=3];
    \n update staff_table set [dept=Market] where [dept = IT];
    \n 输入 'break' 退出.
    """)
    while True:
        query = input('>>>').strip()
        if query == 'break':
            break
        else:
            # 查询操作
            if query.startswith('find') and 'from staff_table where enroll_date like' not in query:
                back_data(query)  
            
            # 日期查询
            elif query.startswith('find') and 'from staff_table where enroll_date like' in query:
                date_query(query)
            
            # add data
            elif query.startswith('add'):
                add_data(query)
                
            # def data
            elif query.startswith('del'):
                del_data(query)
                
            # update data
            elif query.startswith('update'):
                up_data(query)
            else:
                print('语法错误!')


# In[77]:


if __name__ == '__main__':
    staff_table = load_data()
    re_compile()
    main()
    save_data(staff_table)

