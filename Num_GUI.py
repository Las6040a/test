# 从当前目录下将双色球字典.txt文本文件读入，并转换成字典：
import pandas as pd #载入pandas模块
import numpy as np #载入numpy模块
import pymysql #载入pymysql模块，python中执行mysql命令
import time #载入time模块，计算运行时间
import json #载入json模块
import random #载入random模块
from tkinter import * #载入tkinter模块
from tkinter import scrolledtext #载入带滑动条文本框模块
from tkinter.filedialog import (askopenfilename,asksaveasfilename) #载入文件操作模块


#读入双色球字典2
file = open(r'E:\python学习\双色球字典2.txt', 'r') 
js = file.read()
dic = json.loads(js)
# print(dic)
file.close()

#自定义函数红球蓝球遗漏值
def Los_Red_Bule(Con_In):
    """
    按指定开奖序号统计红球及蓝球遗漏值；
    返回：红球遗和、红球位遗以及蓝球位遗值
    """
    cur.execute("select * from du_los_count where con={}".format(Con_In))
    ID_Now=cur.fetchall()[0][0]
    
    R_lo=[]
    R_lt=[]
    R_mp=[]
    B_lt=[]
    #当期红球遗漏统计：
    for i in range(1,34):
        sql="""
        select * from du_los_count where (num between 90 and {0}) 
        and (R1={1} or R2={1} or R3={1} or R4={1} or R5={1} or R6={1}) 
        order by con desc limit 1""".format(ID_Now,i)
        cur.execute(sql)
        aa=cur.fetchall()
        if aa:
            id1=ID_Now-aa[0][0]
            R_lo.append(id1)
        else:
            id1=ID_Now
            R_lo.appenda(id1)
    
    #当期红球位遗统计：
    for i in range(1,7):
        for j in range(i,28+i):
            r_temp='R'+str(i)
            sql="""
            select * from du_los_count where (num between 90 and {0}) 
            and ({1}={2}) order by con desc limit 1""".format(ID_Now,r_temp,j)
            cur.execute(sql)
            aa=cur.fetchall()
            if aa:
                id2=ID_Now-aa[0][0]
                R_mp.append(id2)
            else:
                id2=ID_Now
                R_mp.append(id2)
        R_lt.append(R_mp)
        R_mp=[]
        
     #当期篮球遗漏统计：
    for i in range(1,17):
        sql="""
        select * from du_los_count where (num between 90 and {0}) and B1={1}
        order by con desc limit 1""".format(ID_Now,i)
        cur.execute(sql)
        aa=cur.fetchall()
        if aa:
            id3=ID_Now-aa[0][0]
            B_lt.append(id3)
        else:
            id3=ID_Now
            B_lt.appenda(id3)
#     print(sum(R_lo))
    return R_lo,R_lt,B_lt

#取得最新一期开奖序号
conn=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') #建立mysql连接
cur=conn.cursor() #建立mysql游标
cur.execute('select con from du_multi_opt order by con desc limit 1;') #获取最新序号
ID_new=cur.fetchall()[0][0]

#调用自定义函数得到当期红球遗和、位遗、蓝球位遗数值
Red_lot=Los_Red_Bule(ID_new)

cur.close() #关闭游标
conn.close() #关闭mysql连接

#尾号判断
def Tai_com(l1,l2): #l1字典中的value[4][1]值（尾号组合），l2：输入的尾号组合
    n=0
    wh_bool=False
    if l2=='':
        wh_bool=True
    for i in l1:
        if i in l2:
            n+=1
            if n==len(l2):
#                 print("OK")
                wh_bool=True
                break
    return wh_bool

#红球和值判断，当range_in=True时，按范围判断
def Red_sum(In_dict,In_,range_in=True):
    r_sum_bool=False
    if In_ =='' :
        r_sum_bool=True
    else:
        In_input=list(In_.split(' '))
        if range_in:
            if (In_dict>=(int(In_input[0]))) and (In_dict<=(int(In_input[1]))):
                r_sum_bool=True
        else:
            for i in In_input:
                if int(i)==In_dict:
                    r_sum_bool=True
                    break
    return r_sum_bool 
    
#尾数判断
def Tai_num(In_t1,In_t2):
    t_num_bool=False
    if In_t2=='':
        t_num_bool=True
    else:
        t2=list(In_t2.split(' '))
        for i in t2:
            if int(i)==In_t1:
                t_num_bool=True
                break
    return t_num_bool
            
    
#区间判断
def Do_com(In_d1,In_d2):
    do_com_bool=False
    if In_d2=='':
        do_com_bool=True
    else:
        d2=list(In_d2.split(' '))
        for i in d2:
            if i==In_d1:
                do_com_bool=True
                break
    return do_com_bool

#奇偶判断
def Pa_com(In_p1,In_p2):
    pa_com_bool=False
    if In_p2=='':
        pa_com_bool=True
    else:
        p2=list(In_p2.split(' '))
        for i in p2:
            if i==In_p1:
                pa_com_bool=True
                break
    return pa_com_bool

#AC判断
def AC_com(In_a1,In_a2):
    ac_com_bool=False
    if In_a2=='':
        ac_com_bool=True
    else:
        a2=list(In_a2.split(' '))
        for i in a2:
            if int(i)==In_a1:
                ac_com_bool=True
                break
    return ac_com_bool

#跨度判断
def Cor_com(In_a1,In_a2):
    cor_com_bool=False
    if In_a2=='':
        cor_com_bool=True
    else:
        a2=list(In_a2.split(' '))
        for i in a2:
            if int(i)==In_a1:
                cor_com_bool=True
                break
    return cor_com_bool

#矩阵数判断
def arr_num_com(In_p1,In_p2):
    arr_num_com_bool=False
    if In_p2=='':
        arr_num_com_bool=True
    else:
        p2=list(In_p2.split(' '))
        for i in p2:
            if int(i)==In_p1:
                arr_num_com_bool=True
                break
    return arr_num_com_bool

#最大数判断
def arr_max_com(In_p1,In_p2):
    arr_max_com_bool=False
    if In_p2=='':
        arr_max_com_bool=True
    else:
        p2=list(In_p2.split(' '))
        for i in p2:
            if int(i)==In_p1:
                arr_max_com_bool=True
                break
    return arr_max_com_bool

#红球遗和判断，当range_in=True时，按范围判断
def Red_lo(In_p1,In_p2,range_in=True):
    Red_lo_bool=False
    R_lo_sum=0
    
    In_p1_lst=list(In_p1.split(' '))
    for rl in In_p1_lst:
        R_lo_sum+=Red_lot[0][int(rl)-1]
    
    if In_p2=='':
        Red_lo_bool=True
    else:
        p2=list(map(int,In_p2.split(' ')))
        if range_in:
            if (R_lo_sum>=int(p2[0])) and (R_lo_sum<=int(p2[1])):
                Red_lo_bool=True
        else:
            if R_lo_sum in p2:
                Red_lo_bool=True
                
            
    return Red_lo_bool,R_lo_sum
#红球位遗判断，当range_in=True时，按范围判断
def Red_lt(In_p1,In_p2,range_in=True):
    Red_lt_bool=False
    R_lt_sum=0
   
    j=1
    In_p1_lst=list(In_p1.split(' '))
    for i in In_p1_lst:
        R_lt_sum+=Red_lot[1][j-1][int(i)-j]
        j+=1
    
    if In_p2=='':
        Red_lt_bool=True
    else:
        p2=list(map(int,In_p2.split(' ')))
        if range_in:
            if (R_lt_sum>=int(p2[0])) and (R_lt_sum<=int(p2[1])):
                Red_lt_bool=True
        else:
            if R_lt_sum in p2:
                Red_lt_bool=True
    return Red_lt_bool,R_lt_sum

#矩阵名判断
def A_name(In_dict,In_):
    a_name_bool=False
    if In_=='':
        a_name_bool=True
    else:
        a_dic=list(In_dict.split(' '))
        a_in=list(In_.split(' '))
        for i in a_dic:
            if i in a_in:
                a_name_bool=True
                break
    return a_name_bool

# def r_and_b(key_in,sum_range):
#     rb_bool=False
    
#     key_num=list(key_in.split(' '))
#     r_sum=0
#     for i in key_num:
#         i_temp='%02d'%int(i)
#         r_sum +=int(red_dict[i_temp][3])
                    
#     if sum_range=='':
#         rb_bool=True
#     else:
#         max_sum=int(list(sum_range.split(' '))[1])
#         min_sum=int(list(sum_range.split(' '))[0])
#         if (r_sum>=min_sum) and r_sum<=max_sum:
#             rb_bool=True
            
#     return [rb_bool,r_sum]
    

#胆码判断
def loc_num(key_in,l_num_in):
    l_bool=False
    
    if l_num_in=='':
        l_bool=True
    else:
        x=0
        key_lst=list(key_in.split(' '))
        l_num_lst=list((l_num_in.strip()).split(' '))
        for i in l_num_lst:
            if str(int(i)) in key_lst:
                x+=1
        if x==len(l_num_lst):
            l_bool=True
    return l_bool

#除3余判断
def D3_com(In_p1,In_p2):
    D3_bool=False
    if In_p2=='':
        D3_bool=True
    else:
        p2=list(In_p2.split(' '))
        if In_p1 in p2:
            D3_bool=True
            
    return D3_bool
#大小判断
def Bs_com(In_p1,In_p2):
    Bs_bool=False
    if In_p2=='':
        Bs_bool=True
    else:
        p2=map(str,list(In_p2.split(' ')))
        if In_p1 in p2:
            Bs_bool=True
    return Bs_bool
#质合判断
def Zh_com(In_p1,In_p2):
    Zh_bool=False
    if In_p2=='':
        Zh_bool=True
    else:
        p2=map(str,list(In_p2.split(' ')))
        if In_p1 in p2:
            Zh_bool=True
    return Zh_bool
#大底整理
def Num_cal_by_part(s_in):
    #将输入的大底进行去重、排序、整数型转换、数组化
    s1=s_in.split(' ')
    n_part=sorted(list(set(list(map(int,s1)))))
    return n_part

def Run_program():
    # while True:
    #     s_in = input('大底：')
    #     s1 = s_in.split(' ')
    #     #     t=sorted(list(set(list(map(int,s1)))))
    #     if s_in == '':

    #         break
    #     elif (len(s_in.split(' ')) >= 6):
    #         s1 = s_in.split(' ')
    #         t = sorted(map(int, s1))
    #         break
    #     else:
    #         print('少于6个号码，重新输入')
    t = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33]
   
    s_in=dd.get().strip()
    if s_in=='':
        s_in=t
    else:
        s1 = s_in.split(' ')
        t=sorted(list(set(list(map(int,s1)))))
    # hz = input('和值：')
    hz1=hz.get().strip()
    # qj = input('区间：')
    qj=dom.get().strip()
    # ws = input('尾数：')
    ws=tn.get().strip()
    # wh = input('尾号：')
    wh=ts.get().strip()
    # ac = input('AC值：')
    ac1=ac.get().strip()
    # pa = input('奇偶：')
    pa1=pa.get().strip()
    # cor = input('跨度：')
    cor=cr.get().strip()
    # arr_num = input('矩阵数：')
    arr_num=an.get().strip()
    # arr_max = input('最大数：')
    arr_max=am.get().strip()
    # d3 = input('除3余：')
    d31=d3.get().strip()
    # bs = input('大小：')
    bs1=bs.get().strip()
    # zh = input('质合：')
    zh1=zh.get().strip()
    # R_lo_in = input('遗和：')
    R_lo_in=yh.get().strip()
    # R_lt_in = input('位遗：')
    R_lt_in=wy.get().strip()
    # a_name = input('指定矩阵:')
    a_name=zd.get().strip()
    # l_num = input('胆码：')
    l_num=dm.get().strip()
    sum_ra=''

    # while True:
    #     sum_ra = input('系数和值：')
    #     if (len(sum_ra.split(' ')) == 2) | (sum_ra == ''):
    #         break
    #     else:
    #         print('必须输入两个正整数，中间用空格分开，请重新输入！')


    lst_dis = []
    n = 0
    l = len(t)
    t1 = time.time()
    for r1 in range(0, l - 5):
        for r2 in range(r1 + 1, l - 4):
            for r3 in range(r2 + 1, l - 3):
                for r4 in range(r3 + 1, l - 2):
                    for r5 in range(r4 + 1, l - 1):
                        for r6 in range(r5 + 1, l):
                            key = str(t[r1]) + ' ' + str(t[r2]) + ' ' + str(
                                t[r3]) + ' ' + str(t[r4]) + ' ' + str(
                                    t[r5]) + ' ' + str(t[r6])
                            value = dic[key]
                            Red_lo_aa = Red_lo(key, R_lo_in, range_in=False)
                            Red_lt_aa = Red_lt(key, R_lt_in, range_in=False)
                            if ((loc_num(key,l_num)==True) and 
                                (Do_com(value[2],qj)==True) and
                                (Red_sum(value[0],hz1,range_in=True)==True) and
                                (Tai_com(value[5],wh)==True) and
                                (Tai_num(value[4],ws)==True) and
                                (AC_com(value[6],ac1)==True)  and
                                (Pa_com(value[3],pa1)==True)  and
                                (arr_num_com(value[7],arr_num)==True)  and 
                                (arr_max_com(value[8],arr_max)==True)  and
#                                 (r_and_b(key,sum_ra)[0]==True)  and
                                (Cor_com(value[1],cor)==True)  and
                                (D3_com(value[12],d31)==True)  and
                                (Red_lo_aa[0]==True)  and
                                (Bs_com(value[10],bs1)==True)  and
                                (Zh_com(value[11],zh1)==True)  and
                                (Red_lt_aa[0]==True) and 
                                (A_name(value[9],a_name)==True)):
    #                             print(key, end=' : ')
                                text.insert(END,key)
                                text.insert(END,': ')
                                text.insert(END,'[')
                                for te in value:
                                    text.insert(END,te)
                                    text.insert(END,',')
                                text.insert(END,'] ')
                                text.insert(END,Red_lo_aa[1])
                                text.insert(END,' ')
                                text.insert(END,Red_lt_aa[1])
                                text.insert(INSERT,'\n')
    #                             print(value, Red_lo_aa[1], Red_lt_aa[1])
                                n += 1
                                if int(checkVar.get())==1:
                                    lst_dis.append(key)
    t2 = time.time()
#     print('共计', n, '注')
#     print('耗时：', '%.2f' % (t2 - t1), '秒')
    str1='共计 ' +str(n) +'注' +'\n'
    str2='耗时：' + '%.2f' % (t2 - t1) +' 秒'  +'\n' +'\n'
    str3=str1+str2
#     text.insert(INSERT,'\n')
    text.insert(0.0,str3)
    text.insert(INSERT,'\n')
#     text.insert(END,str2)
    if len(lst_dis)>0:
        pd_data=pd.DataFrame(lst_dis)
        # pd_data.to_csv('Res_in.csv',index=False,header=None)
        pd_data.to_csv(r'E:\python学习\Res_in.csv',index=False,header=None)

def Run_program1():
    
    re=pd.read_csv(r'E:\python学习\33套29组数组\测试.txt',header=None,skiprows=1,index_col=0)
    re_arr=np.array(re)
    
    # hz = input('和值：')
    hz1=hz.get().strip()
    # qj = input('区间：')
    qj=dom.get().strip()
    # ws = input('尾数：')
    ws=tn.get().strip()
    # wh = input('尾号：')
    wh=ts.get().strip()
    # ac = input('AC值：')
    ac1=ac.get().strip()
    # pa = input('奇偶：')
    pa1=pa.get().strip()
    # cor = input('跨度：')
    cor=cr.get().strip()
    # arr_num = input('矩阵数：')
    arr_num=an.get().strip()
    # arr_max = input('最大数：')
    arr_max=am.get().strip()
    # d3 = input('除3余：')
    d31=d3.get().strip()
    # bs = input('大小：')
    bs1=bs.get().strip()
    # zh = input('质合：')
    zh1=zh.get().strip()
    # R_lo_in = input('遗和：')
    R_lo_in=yh.get().strip()
    # R_lt_in = input('位遗：')
    R_lt_in=wy.get().strip()
    # a_name = input('指定矩阵:')
    a_name=zd.get().strip()
    # l_num = input('胆码：')
    l_num=dm.get().strip()
    sum_ra=''

    lst_dis = []
    n = 0
#     l = len(t)
    t1 = time.time()
    for key33 in re_arr:
        key=str(key33[0])
        value = dic[key]
        Red_lo_aa = Red_lo(key, R_lo_in, range_in=False)
        Red_lt_aa = Red_lt(key, R_lt_in, range_in=False)
        if ((loc_num(key,l_num)==True) and 
            (Do_com(value[2],qj)==True) and
            (Red_sum(value[0],hz1,range_in=True)==True) and
            (Tai_com(value[5],wh)==True) and
            (Tai_num(value[4],ws)==True) and
            (AC_com(value[6],ac1)==True)  and
            (Pa_com(value[3],pa1)==True)  and
            (arr_num_com(value[7],arr_num)==True)  and 
            (arr_max_com(value[8],arr_max)==True)  and
#                                 (r_and_b(key,sum_ra)[0]==True)  and
            (Cor_com(value[1],cor)==True)  and
            (D3_com(value[12],d31)==True)  and
            (Red_lo_aa[0]==True)  and
            (Bs_com(value[10],bs1)==True)  and
            (Zh_com(value[11],zh1)==True)  and
            (Red_lt_aa[0]==True) and 
            (A_name(value[9],a_name)==True)):
#                             print(key, end=' : ')
            text.insert(END,key)
            text.insert(END,': ')
            text.insert(END,'[')
            for te in value:
                text.insert(END,te)
                text.insert(END,',')
            text.insert(END,'] ')
            text.insert(END,Red_lo_aa[1])
            text.insert(END,' ')
            text.insert(END,Red_lt_aa[1])
            text.insert(INSERT,'\n')
#                             print(value, Red_lo_aa[1], Red_lt_aa[1])
            n += 1
            if int(checkVar.get())==1:
                lst_dis.append(key)
    t2 = time.time()
#     print('共计', n, '注')
#     print('耗时：', '%.2f' % (t2 - t1), '秒')
    str1='共计 ' +str(n) +'注' +'\n'
    str2='耗时：' + '%.2f' % (t2 - t1) +' 秒'  +'\n' +'\n'
    str3=str1+str2
#     text.insert(INSERT,'\n')
    text.insert(0.0,str3)
    text.insert(INSERT,'\n')
#     text.insert(END,str2)
    if len(lst_dis)>0:
        pd_data=pd.DataFrame(lst_dis)
        pd_data.to_csv('Res_in.csv',index=False,header=None)

re=pd.read_csv(r'E:\python学习\33套29组数组\测试.txt',header=None,skiprows=1,index_col=0)
re_arr=np.array(re)

def action():
    dd_dis = '大底：' + dd.get().strip()
    hz_dis = '和值：' + hz.get().strip()
    dom_dis = '区间：' + dom.get().strip()
    tn_dis = '尾数：' + tn.get().strip()
    ts_dis = '尾号：' + ts.get().strip()
    ac_dis = 'AC：' + ac.get().strip()
    pa_dis = '奇偶：' + pa.get().strip()
    cr_dis = '跨度：' + cr.get().strip()
    an_dis = '矩阵数：' + an.get().strip()
    am_dis = '最大数：' + am.get().strip()
    d3_dis = '除3余：' + d3.get().strip()
    bs_dis = '大小：' + bs.get().strip()
    zh_dis = '质合：' + zh.get().strip()
    yh_dis = '遗和：' + yh.get().strip()
    wy_dis = '位遗：' + wy.get().strip()
    zd_dis = '指定矩阵：' + zd.get().strip()
    dm_dis = '胆码：' + dm.get().strip()

    dis_text = [
        dd_dis, hz_dis, dom_dis, tn_dis, ts_dis, ac_dis, pa_dis, cr_dis,
        an_dis, am_dis, d3_dis, bs_dis, zh_dis, yh_dis, wy_dis, zd_dis, dm_dis
    ]
    
    text.delete(0.0,END)
    for i in dis_text:
        text.insert(END, i)
        text.insert(INSERT, '\n')
    text.insert(INSERT, '\n')
    
    #方案选择：区别：如果用33套数组前置缩水，则直接遍历前置缩水后的号码组合列表，否则用大底组成的列表6层循环C(大底，6)
    if int(checkVar1.get())==1: #如果利用33套数组前置缩水则调用Run_program1
        print(checkVar1.get())
        Run_program1()
    else: #否则调用Run_program
        Run_program()

def copy_clip(): #复制运算结果（text文本框内的内容）
    copy_=text.get(0.0,END)
    text.clipboard_clear()
    text.clipboard_append(copy_)

def reset(): #清空所有输入框及文本框的内容
    text.delete(0.0,END)
    dd.delete(0,END)
    hz.delete(0,END)
    dom.delete(0,END)
    tn.delete(0,END)
    ts.delete(0,END)
    ac.delete(0,END)
    pa.delete(0,END)
    cr.delete(0,END)
    an.delete(0,END)
    am.delete(0,END)
    d3.delete(0,END)
    bs.delete(0,END)
    zh.delete(0,END)
    yh.delete(0,END)
    wy.delete(0,END)
    zd.delete(0,END)
    dm.delete(0,END)

def svae_opt(): #保存方案
    opt_dic = {
        'dd': dd.get(),
        'hz': hz.get(),
        'dom': dom.get(),
        'tn': tn.get(),
        'ts': ts.get(),
        'ac': ac.get(),
        'pa': pa.get(),
        'cr': cr.get(),
        'an': an.get(),
        'am': am.get(),
        'd3': d3.get(),
        'bs': bs.get(),
        'zh': zh.get(),
        'yh': yh.get(),
        'wy': wy.get(),
        'zd': zd.get(),
        'dm': dm.get()
    }
    
    file_svae_name=asksaveasfilename(title='保存文件',initialdir='E:\方案保存',filetypes=[('缩水方案','*.sa')])
    if file_svae_name!='':
        json_str=json.dumps(opt_dic) #dumps
        fin_ex=file_svae_name.find('.sa')
        if fin_ex==-1:
            file_svae_name=file_svae_name+'.sa'
        with open(file_svae_name, 'w') as f:
            f.write(json_str)
        f.close() 

def load_opt(): #读取方案
    file_load_name=askopenfilename(title='打开文件',initialdir='E:\方案保存',filetypes=[('缩水方案','*.sa'),('所有类型','*.*')])
    if file_load_name!='':
        file = open(file_load_name, 'r')
        js = file.read()
        dic_tk = json.loads(js)
        file.close()
    
        dd.delete(0,END)
        hz.delete(0,END)
        dom.delete(0,END)
        tn.delete(0,END)
        ts.delete(0,END)
        ac.delete(0,END)
        pa.delete(0,END)
        cr.delete(0,END)
        an.delete(0,END)
        am.delete(0,END)
        d3.delete(0,END)
        bs.delete(0,END)
        zh.delete(0,END)
        yh.delete(0,END)
        wy.delete(0,END)
        zd.delete(0,END)
        dm.delete(0,END)

        dd.insert(END,dic_tk['dd'])
        hz.insert(END,dic_tk['hz'])
        dom.insert(END,dic_tk['dom'])
        tn.insert(END,dic_tk['tn'])
        ts.insert(END,dic_tk['ts'])
        ac.insert(END,dic_tk['ac'])
        pa.insert(END,dic_tk['pa'])
        cr.insert(END,dic_tk['cr'])
        an.insert(END,dic_tk['an'])
        am.insert(END,dic_tk['am'])
        d3.insert(END,dic_tk['d3'])
        bs.insert(END,dic_tk['bs'])
        zh.insert(END,dic_tk['zh'])
        yh.insert(END,dic_tk['yh'])
        wy.insert(END,dic_tk['wy'])
        zd.insert(END,dic_tk['zd'])
        dm.insert(END,dic_tk['dm'])



    
#实例化tk
root=Tk()
#更改图标
root.iconbitmap(r'E:\图标\yellow.ico')
#设置窗口宽高及屏幕位置：250x100--->宽高，+300+300-->右下角处于屏幕的x,y坐标
root.geometry('1200x700+300+200')
#窗口不能拉宽拉高
root.resizable(False,False)
root.configure(bg='DimGray') #DimGray
#设置窗口标题
root.title('双色球号码缩水')

#创建标签
#左0
Label(root,text='大底:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=0,column=0)
#将输入框放置在标签之后
dd=Entry(root,bg='Gainsboro')
dd.grid(row=0,column=1,padx=10,pady=3,ipadx=180)

#右0
Label(root,text='和值:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=0,column=2)
#将输入框放置在标签之后
hz=Entry(root,bg='Gainsboro')
hz.grid(row=0,column=3,padx=10,pady=3,ipadx=180)

#左1
Label(root,text='区间:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=1,column=0)
#将输入框放置在标签之后
dom=Entry(root,bg='Gainsboro')
dom.grid(row=1,column=1,padx=10,pady=3,ipadx=180)

#右1
Label(root,text='尾数:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=1,column=2)
#将输入框放置在标签之后
tn=Entry(root,bg='Gainsboro')
tn.grid(row=1,column=3,padx=10,pady=3,ipadx=180)

#左2
Label(root,text='尾号:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=2,column=0)
#将输入框放置在标签之后
ts=Entry(root,bg='Gainsboro')
ts.grid(row=2,column=1,padx=10,pady=3,ipadx=180)

#右2
Label(root,text='AC:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=2,column=2)
#将输入框放置在标签之后
ac=Entry(root,bg='Gainsboro')
ac.grid(row=2,column=3,padx=10,pady=3,ipadx=180)

#左3
Label(root,text='奇偶:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=3,column=0)
#将输入框放置在标签之后
pa=Entry(root,bg='Gainsboro')
pa.grid(row=3,column=1,padx=10,pady=3,ipadx=180)

#右3
Label(root,text='跨度:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=3,column=2)
#将输入框放置在标签之后
cr=Entry(root,bg='Gainsboro')
cr.grid(row=3,column=3,padx=10,pady=3,ipadx=180)

#左4
Label(root,text='矩阵数:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=4,column=0)
#将输入框放置在标签之后
an=Entry(root,bg='Gainsboro')
an.grid(row=4,column=1,padx=10,pady=3,ipadx=180)

#右4
Label(root,text='最大数:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=4,column=2)
#将输入框放置在标签之后
am=Entry(root,bg='Gainsboro')
am.grid(row=4,column=3,padx=10,pady=3,ipadx=180)

#左5
Label(root,text='除3余:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=5,column=0)
#将输入框放置在标签之后
d3=Entry(root,bg='Gainsboro')
d3.grid(row=5,column=1,padx=10,pady=3,ipadx=180)

#右5
Label(root,text='大小:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=5,column=2)
#将输入框放置在标签之后
bs=Entry(root,bg='Gainsboro')
bs.grid(row=5,column=3,padx=10,pady=3,ipadx=180)

#左6
Label(root,text='质合:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=6,column=0)
#将输入框放置在标签之后
zh=Entry(root,bg='Gainsboro')
zh.grid(row=6,column=1,padx=10,pady=3,ipadx=180)

#右6
Label(root,text='遗和:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=6,column=2)
#将输入框放置在标签之后
yh=Entry(root,bg='Gainsboro')
yh.grid(row=6,column=3,padx=10,pady=3,ipadx=180)

#左7
Label(root,text='位遗:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=7,column=0)
#将输入框放置在标签之后
wy=Entry(root,bg='Gainsboro')
wy.grid(row=7,column=1,padx=10,pady=3,ipadx=180)

#右7
Label(root,text='指定矩阵:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=7,column=2)
#将输入框放置在标签之后
zd=Entry(root,bg='Gainsboro')
zd.grid(row=7,column=3,padx=10,pady=3,ipadx=180)

#左8
Label(root,text='胆码:',font=('仿宋',11),bg='DimGray',fg='White').grid(row=8,column=0)
#将输入框放置在标签之后
dm=Entry(root,bg='Gainsboro')
dm.grid(row=8,column=1,padx=10,pady=3,ipadx=180)



# #创建文本框
# text=Text(root,width=159,height=20)


text = scrolledtext.ScrolledText(root, width=137, height=25,font=("Times New Roma",11),bg='Gainsboro',relief="solid")
text.place(x=70,y=250)


#6个按钮创建,并单击绑定6个相关自定义函数,这时,自定义函数后面不能有括号，否则只执行一次
button1=Button(root,text='运 算',width='10',command=action,bg='Gainsboro',font=('仿宋',12)).place(x=785,y=655)
button2=Button(root,text='复制结果',width='10',command=copy_clip,bg='Gainsboro',font=('仿宋',12)).place(x=685,y=655)
button3=Button(root,text='重 置',width='10',command=reset,bg='Gainsboro',font=('仿宋',12)).place(x=585,y=655)
button4=Button(root,text='保存方案',width='10',command=svae_opt,bg='Gainsboro',font=('仿宋',12)).place(x=485,y=655)
button5=Button(root,text='加载方案',width='10',command=load_opt,bg='Gainsboro',font=('仿宋',12)).place(x=385,y=655)
button6=Button(root,text='退出',width='10',command=quit,bg='Gainsboro',font=('仿宋',12)).place(x=1085,y=655)
checkVar = StringVar(value="0") #设置第一个复选框默认值=0时不选
chbnt=Checkbutton(root,bg='DimGray',variable=checkVar) #创建复选框1
chbnt.place(x=885,y=645)
Label(root,text='生成投注号码',font=('仿宋',11),bg='DimGray',fg='White').place(x=910,y=647) #复选框1标签
photo=PhotoImage(file='E:\图标\小问号.png',width=20,height=20) #创建问号图标
imglable=Label(root,image=photo,bg='DimGray') #将问号图标与标签imglable绑定
imglable.place(x=20,y=657) #问号图标位置

checkVar1 = StringVar(value="0") #创建复选框2
chbnt1=Checkbutton(root,bg='DimGray',variable=checkVar1)
chbnt1.place(x=885,y=665)
Label(root,text='33套数组前置缩水',font=('仿宋',11),bg='DimGray',fg='White').place(x=910,y=667) #复选框1标签

# imglable.bind('<Enter>',func_1)

#循环弹窗
root.mainloop()