import os
import json
from numpy.lib.function_base import insert
import pymysql
import pandas as pd 
import copy
from tkinter import *
from tkinter import scrolledtext
file_path=os.getcwd()

file = open(file_path + r'\Lib\和值标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_sum_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_sum_real=dict(dic_sum_real)

file = open(file_path + r'\Lib\跨度标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_cor_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_cor_real=dict(dic_cor_real)

file = open(file_path + r'\Lib\奇偶标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_pa_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_pa_real=dict(dic_pa_real)

file = open(file_path + r'\Lib\尾数标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_tn_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_tn_real=dict(dic_tn_real)

file = open(file_path + r'\Lib\AC值标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_ac_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_ac_real=dict(dic_ac_real)

file = open(file_path + r'\Lib\矩阵数量与最大值标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_arr_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_arr_real=dict(dic_arr_real)


file = open(file_path + r'\Lib\矩阵数量标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_arr_num_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_arr_num_real=dict(dic_arr_num_real)


file = open(file_path + r'\Lib\矩阵最大数标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_arr_max_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_arr_max_real=dict(dic_arr_max_real)

file = open(file_path + r'\Lib\除3余标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_d3_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_d3_real=dict(dic_d3_real)

file = open(file_path + r'\Lib\大小标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_Bs_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_Bs_real=dict(dic_Bs_real)

file = open(file_path + r'\Lib\质合标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_Zh_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)   
dic_Zh_real=dict(dic_Zh_real)

file = open(file_path + r'\Lib\矩阵名标准字典.txt', 'r')
js = file.read()
dic_temp = json.loads(js)
file.close()
dic_arr_name_real=sorted(dic_temp.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=False)   
dic_arr_name_real=dict(dic_arr_name_real)

def Arr_name_com(display=True):
    dic_d3={}
    dic_d3=copy.deepcopy(dic_arr_name_real)
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    
    for key,value in dic_d3.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_s like "%{0}%")  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_s like "%{0}%") b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_s like "%{0}%")  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_s like "%{0}%") b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where a_s like '%{0}%' """.format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_d3[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'矩阵名 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('矩阵名：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_d3


def Zh_com(display=True):
    dic_d3={}
    dic_d3=copy.deepcopy(dic_Zh_real)
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_option2 ;')
    ID_now=int(cur_my.fetchall()[0][0])
    
    for key,value in dic_d3.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2 where zh={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2  where zh={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2 where zh={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2  where zh={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码大小比总数
        sql3="""select Count(*) from du_option2 where zh={}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_d3[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'质合比 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('质合比：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_d3


def Bs_com(display=True):
    dic_d3={}
    dic_d3=copy.deepcopy(dic_Bs_real)
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_option2 ;')
    ID_now=int(cur_my.fetchall()[0][0])
    
    for key,value in dic_d3.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2 where bs={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2  where bs={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2 where bs={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_option2  where bs={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码大小比总数
        sql3="""select Count(*) from du_option2 where bs={}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_d3[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'大小比 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('大小比：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_d3


#区间比参数运算：
def Do_com(display=True):
    dic_d3={}
    dic_d3=copy.deepcopy(dic_d3_real)
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    
    for key,value in dic_d3.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where dom={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where dom={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where dom={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where dom={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where dom={}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_d3[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'区间比 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('区间比：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_d3


def D3_com(display=True):
    dic_d3={}
    dic_d3=copy.deepcopy(dic_d3_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_d3.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where d3={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where d3={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where d3={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where d3={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where d3={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_d3[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'除3余 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('除3余：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_d3

#区间比参数运算：
def Sum_com(display=True):
    
    dic_sum={}
    dic_sum=copy.deepcopy(dic_sum_real)
     #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_sum.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where sum={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where sum={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where sum={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where sum={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where sum={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
#         aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),(lose_now*dd3)]
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(float(value[1])*lose_now,2)]
        dic_sum[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'和值  ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('和值：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=理论占比*当前遗漏】')
    return dic_sum

#跨度比参数运算：
def Cor_com(display=True):
    
    dic_cor={}
    dic_cor=copy.deepcopy(dic_cor_real)
     #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_cor.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where cor={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where cor={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where cor={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where cor={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where cor={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_cor[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'跨度  ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('跨度：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_cor

#奇偶比参数运算：
def Pa_com(display=True):
    
    dic_pa={}
    dic_pa=copy.deepcopy(dic_pa_real)
     #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_pa.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where pa={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where pa={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where pa={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where pa={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where pa={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_pa[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'奇偶  ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('奇偶：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_pa

#尾数比参数运算：
def Tn_com(display=True):
    
    dic_tn={}
    dic_tn=copy.deepcopy(dic_tn_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_tn.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ta_n={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where ta_n={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ta_n={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ta_n={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where ta_n={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_tn[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'尾数  ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('尾数：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_tn

#尾数比参数运算：
def Ac_com(display=True):
    
    dic_ac={}
    dic_ac=copy.deepcopy(dic_ac_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_ac.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ac={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where ac={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ac={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where ac={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where ac={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_ac[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'AC  ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('AC：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_ac

#矩阵数量与最大值参数运算：
def Arr_com(display=True):
    
    dic_arr={}
    dic_arr=copy.deepcopy(dic_arr_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_arr.items():
        key_lst=list(key.split('_'))
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_n={0} and a_max={1})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_n={0} and a_max={1}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key_lst[0],key_lst[1])
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_n={0} and a_max={1})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_n={0} and a_max={1}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key_lst[0],key_lst[1])
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where a_n={0} and a_max={1}""".format(key_lst[0],key_lst[1])
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.4f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_arr[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'矩阵组合：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('矩阵组合：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    return dic_arr

#矩阵数量参数运算：
def Arr_num_com(display=True):
    
    dic_arr_num={}
    dic_arr_num=copy.deepcopy(dic_arr_num_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_arr_num.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_n={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_n={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_n={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_n={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where a_n={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_arr_num[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'矩阵数 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
#     print('矩阵数：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')

    return dic_arr_num

#矩阵数量参数运算：
def Arr_max_com(display=True):
    
    dic_arr_max={}
    dic_arr_max=copy.deepcopy(dic_arr_max_real)
    #建立mysql连接
    conn_my=pymysql.connect(host='localhost',user='root',password='1234',database='Ducolor') 
    #设置游标
    cur_my=conn_my.cursor() 
    cur_my.execute('select count(*) from du_multi_opt ;')
    ID_now=int(cur_my.fetchall()[0][0])
    for key,value in dic_arr_max.items():
        #当期遗漏
        sql1="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_max={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt  where a_max={0}) b on b.tttt   = a.tttt +1  order 
        by bbbb desc limit 1;""".format(key)
        cur_my.execute(sql1)
        dd1=cur_my.fetchall()
        if dd1 :
            lose_now=ID_now-dd1[0][0]
        else:
            lose_now=ID_now
    #     print(key,' : 当前遗漏：',lose_now)
        #最大遗漏：
        sql2="""
        select  a.num as bbbb ,a.num  - b.num  -1 as aaaa  from (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_max={0})  a left join (select *,ROW_NUMBER () 
        over(order by num desc) as tttt from du_multi_opt where a_max={0}) b on b.tttt   = a.tttt +1  order 
        by aaaa desc limit 1;""".format(key)
        cur_my.execute(sql2)
        dd2=cur_my.fetchall()
        if dd2 :
            lose_max=dd2[0][1]
        else:
            lose_max=ID_now
        #开奖号码区间比总数
        sql3="""select Count(*) from du_multi_opt where a_max={0}""".format(key)
        cur_my.execute(sql3)
        dd3=cur_my.fetchall()[0][0]
        pr1=float('%.4f'%(int(dd3)/ID_now*100))
        aa_temp=[dd3,pr1,lose_max,lose_now,'%.2f'%(float(value[1])-pr1),round(lose_now*float(value[1]),2)]
        dic_arr_max[key].append(aa_temp)
        aa_temp=[]

    #     print(key,' :  ','理论',value[0],'占比',value[1],'%',' 实际',dd3,
    #           ' 占比', '%.2f'%(int(dd3)/ID_now*100), '%  最大遗漏',lose_max,' 当前遗漏',lose_now)
    cur_my.close()
    conn_my.close()
#     print('最大数：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
    if display:
        text.delete(0.0,END)
        text.insert(0.0,'最大数 ：【理论，占比】，【实数，占比，最大遗漏，当前遗漏，占比差，系数=实数*当前遗漏】')
        text.insert(INSERT,'\n')
    return dic_arr_max

def dis_opt(display=True):
    t=r_value.get()-1
    o=r_value1.get()
      
    res_dict=sub_name_lst[t]()
    if display:
        #理论
        atr=sorted(res_dict.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)
        en3b.delete(0,END)
        en3b.insert(0,atr[0][-1][0])
        en3a.delete(0,END)
        en3a.insert(0,atr[-1][-1][0])
        #实数
        atr=sorted(res_dict.items(), key = lambda kv:(kv[1][2][0], kv[0]),reverse=True)
        en1b.delete(0,END)
        en1b.insert(0,atr[0][-1][2][0])
        en1a.delete(0,END)
        en1a.insert(0,atr[-1][-1][2][0])
        #遗漏
        atr=sorted(res_dict.items(), key = lambda kv:(kv[1][2][3], kv[0]),reverse=True)
        en4b.delete(0,END)
        en4b.insert(0,atr[0][-1][2][3])
        en4a.delete(0,END)
        en4a.insert(0,atr[-1][-1][2][3])
        #系数
        atr=sorted(res_dict.items(), key = lambda kv:(kv[1][2][5], kv[0]),reverse=True)
        en2b.delete(0,END)
        en2b.insert(0,atr[0][-1][2][5])
        en2a.delete(0,END)
        en2a.insert(0,atr[-1][-1][2][5])


    if o!=1:
        if o==2:
            o=0
        else:
            o=o-1            
        d3_tupe_order=sorted(res_dict.items(), key = lambda kv:(kv[1][2][o], kv[0]),reverse=True)
        for p in d3_tupe_order:
            text.insert(END,p)
            text.insert(INSERT,'\n')
    else:
        d3_tupe_order=sorted(res_dict.items(), key = lambda kv:(kv[1][0], kv[0]),reverse=True)
        for p in d3_tupe_order:
            text.insert(END,p)
            text.insert(INSERT,'\n')
    
    return res_dict
    # json_str = json.dumps(res_dict) #dumps
    # with open('opt_temp.txt', 'w') as f:
    #     f.write(json_str)
    # f.close()

def select_opt():
    res_dict=dis_opt(display=False)
    if chn5_var.get()==0:
        
        n1a=int(en1a.get())
        n1b=int(en1b.get())

        n2a=float(en2a.get())
        n2b=float(en2b.get())

        n3a=int(en3a.get())
        n3b=int(en3b.get())

        n4a=int(en4a.get())
        n4b=int(en4b.get())
        text.insert(INSERT,'\n')
        pr_sum=0
        str_name=text.get(1.0,2.0)[:4]
        name_lst=[]
        text.insert(END,'筛选条件：')
        
        text.insert(INSERT,'\n')
        text.insert(END,'实数：')
        text.insert(END,'>= ')
        text.insert(END,en1a.get())
        text.insert(END,' ; <= ')
        text.insert(END,en1b.get())
        text.insert(INSERT,'\n')

        text.insert(END,'系数：')
        text.insert(END,'>= ')
        text.insert(END,en2a.get())
        text.insert(END,' ; <= ')
        text.insert(END,en2b.get())
        text.insert(INSERT,'\n')

        text.insert(END,'理论')
        text.insert(END,'>= ')
        text.insert(END,en3a.get())
        text.insert(END,' ; <= ')
        text.insert(END,en3b.get())
        text.insert(INSERT,'\n')

        text.insert(END,'遗漏：')
        text.insert(END,'>= ')
        text.insert(END,en4a.get())
        text.insert(END,' ; <= ')
        text.insert(END,en4b.get())
        text.insert(INSERT,'\n')
        text.insert(INSERT,'\n')

        for key,values in res_dict.items():
            if ((values[2][0]>=n1a) and (values[2][0]<=n1b) and (values[2][5]>=n2a)  and (values[2][5]<=n2b)  and (values[0]>=n3a)  and (values[0]<=n3b)  and (values[2][3]>=n4a) and (values[2][3]<=n4b)):
                text.insert(END,key)
                text.insert(END,' : ')
                text.insert(END,values)
                text.insert(INSERT,'\n')
                pr_sum+=round(float(values[1]),4)
                name_lst.append(key)
        text.insert(INSERT,'\n')
        text.insert(END,'占比：')
        text.insert(END,round(pr_sum,2))
        text.insert(END,' %')
        text.insert(INSERT,'\n')
        text.insert(INSERT,'\n')
        text.insert(END,str_name)
        text.insert(END,' :')
        for n in name_lst:
            text.insert(END,n)
            text.insert(END,' ')
        text.insert(END,'        ')
        text.insert(END,'占比：')
        text.insert(END,round(pr_sum,2))
        text.insert(END,' %')
    else:
        text.insert(INSERT,'\n')
        pr_sum=0
        str_name=text.get(1.0,2.0)[:2]
        name_lst=[]
        text.insert(END,'筛选条件：')
        text.insert(INSERT,'\n')
        text.insert(END,'范围：')
        text.insert(END,'>= ')
        text.insert(END,en5a.get())
        text.insert(END,' ; <= ')
        text.insert(END,en5b.get())
        text.insert(INSERT,'\n')
        for key,values in res_dict.items():
            if (int(key)>=int(en5a.get())and (int(key)<=int(en5b.get()))):
                text.insert(END,key)
                text.insert(END,' : ')
                text.insert(END,values)
                text.insert(INSERT,'\n')
                pr_sum+=round(float(values[1]),4)
        text.insert(INSERT,'\n')
        text.insert(END,'占比：')
        text.insert(END,round(pr_sum,2))
        text.insert(END,' %')
        text.insert(INSERT,'\n')
        text.insert(INSERT,'\n')
        text.insert(END,str_name)
        text.insert(END,' :')
        text.insert(END,en5a.get())
        text.insert(END,' ')
        text.insert(END,en5b.get())
        text.insert(END,'        占比：')
        text.insert(END,round(pr_sum,2))
        text.insert(END,' %')







    # file = open('opt_temp.txt', 'r')
    # js = file.read()
    # dic = json.loads(js)
    # print(dic)
    # file.close()

def en_allow():
    if chn5_var.get()==1:
        en1a.config(state='disable')
        en1b.config(state='disable')
        en2a.config(state='disable')
        en2b.config(state='disable')
        en3a.config(state='disable')
        en3b.config(state='disable')
        en4a.config(state='disable')
        en4b.config(state='disable')
    elif chn5_var.get()==0:
        en1a.config(state='normal')
        en1b.config(state='normal')
        en2a.config(state='normal')
        en2b.config(state='normal')
        en3a.config(state='normal')
        en3b.config(state='normal')
        en4a.config(state='normal')
        en4b.config(state='normal')

def copy_txt():
    copy_=text.get(0.0,END)
    text.clipboard_clear()
    text.clipboard_append(copy_)  
    
root=Tk()
name_lst=[[1,'和值'],[2,'区间'],[3,'尾数'],[4,'AC'],[5,'奇偶'],
          [6,'跨度'],[7,'矩阵数'],[8,'最大数'],[9,'除3余'],
          [10,'大小比'],[11,'质合比'],[12,'矩阵名'],[13,'组合']]
sub_name_lst=[Sum_com,Do_com,Tn_com,Ac_com,Pa_com,Cor_com,Arr_num_com,Arr_max_com,D3_com,Bs_com,Zh_com,Arr_name_com,Arr_com]

WIDTH=800
HEIGHT=650
col_num=[400,430]

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (WIDTH / 2)
y = (hs / 2) - (HEIGHT / 2)
root.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))
root.title('基础参数统计_GUI版')
root.iconbitmap(r'E:\图标\yellow.ico')
root.resizable(False,False)
# root.configure(bg='DimGray') #DimGray

text = scrolledtext.ScrolledText(root,width=85, height=25,font=("Times New Roma",11),bg='Gainsboro',relief="solid")
text.place(x=5,y=5)
r_value = IntVar()
# r_value.set(1)

for y in range(400,431,30):
    if y==400:
        for num,name in name_lst[:7]:
            ra=Radiobutton(root,text=name,variable=r_value,value=num,command=dis_opt)
            ra.place(x=(num-1)*70+15,y=y)
    else:
        for num,name in name_lst[7:]:
            ra=Radiobutton(root,text=name,variable=r_value,value=num,command=dis_opt)
            ra.place(x=(num-8)*70+15,y=y)
fr1=Frame(root,bg='red').pack()
# fr1.place(x=750,y=650)
bnt2=Button(root,text='复制结果',command=copy_txt)
bnt2.place(x=530,y=397)
lab2=Label(root,text='参数筛选运算：')
lab2.place(x=10,y=470)
chn5_var=IntVar()
chn5_var.set(0)
chb5=Checkbutton(root,text='参数范围框选',variable=chn5_var,command=en_allow)
chb5.place(x=95,y=470)
en5a=Entry(root)
en5a.place(x=200,y=473,width=50,height=20)
en5b=Entry(root)
en5b.place(x=265,y=473,width=50,height=20)
lab5=Label(root,text='~')
lab5.place(x=248,y=473)

l1=Label(root,text='实数')
l1.place(x=10,y=500)
en1a=Entry(root,width=5)
en1a.place(x=50,y=503)
en1b=Entry(root,width=9)
en1b.place(x=110,y=503)
lab3=Label(root,text='~')
lab3.place(x=92,y=503)

l2=Label(root,text='系数')
l2.place(x=10,y=525)
en2a=Entry(root,width=5)
en2a.place(x=50,y=528)
en2b=Entry(root,width=9)
en2b.place(x=110,y=528)
lab3=Label(root,text='~')
lab3.place(x=92,y=528)

l3=Label(root,text='理论')
l3.place(x=10,y=550)
en3a=Entry(root,width=5)
en3a.place(x=50,y=553)
en3b=Entry(root,width=9)
en3b.place(x=110,y=553)
lab3=Label(root,text='~')
lab3.place(x=92,y=553)

l4=Label(root,text='遗漏')
l4.place(x=10,y=575)
en4a=Entry(root,width=5)
en4a.place(x=50,y=578)
en4b=Entry(root,width=9)
en4b.place(x=110,y=578)
lab3=Label(root,text='~')
lab3.place(x=92,y=578)

l1=Label(root,text='参数排序选择')
l1.place(x=710,y=5)
r_value1=IntVar()
r_value1.set(1)
ra1=Radiobutton(fr1,text='理论',variable=r_value1,value=1)
ra1.place(x=710,y=30)

ra1=Radiobutton(fr1,text='实数',variable=r_value1,value=2)
ra1.place(x=710,y=50)

ra1=Radiobutton(fr1,text='最大遗漏',variable=r_value1,value=3)
ra1.place(x=710,y=70)

ra1=Radiobutton(fr1,text='当前遗漏',variable=r_value1,value=4)
ra1.place(x=710,y=90)

ra1=Radiobutton(fr1,text='占比差',variable=r_value1,value=5)
ra1.place(x=710,y=110)

ra1=Radiobutton(fr1,text='系数',variable=r_value1,value=6)
ra1.place(x=710,y=130)

bnt=Button(root,text='运算',command=select_opt)
bnt.place(x=85,y=610)

root.mainloop()

