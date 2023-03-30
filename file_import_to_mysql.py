#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install mysql-connector-python')


# In[1]:


get_ipython().run_line_magic('pwd', '')


# In[15]:


import pandas as pd
import numpy as np

AggTransByStates = pd.read_csv('AggTransByStates.csv')
AggUserByBrand = pd.read_csv('AggUserByBrand.csv')
mapTransByDistrict = pd.read_csv('mapTransByDist.csv')
mapUserByDistReg = pd.read_csv('mapUserByDistReg.csv')


# In[3]:


mapUserByDistReg.dtypes


# # Map User by District Registration Data to MySQL

# In[4]:


import mysql.connector
from mysql.connector import Error
try:
    mydb =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aaj2606",
        database="aaj")
    if mydb.is_connected():  
        cursor= mydb.cursor()
        cursor.execute("use aaj;") 
        cursor.execute("DROP TABLE IF EXISTS mapUserByDistReg;")
        cursor.execute("CREATE TABLE mapUserByDistReg                       (State varchar(100),                        Year int,                        Quater varchar(5),                        District varchar(50),                        Registered_user int,                        App_opening int)")
        print("mapUserByDistReg  table is created....")

        for i, row in mapUserByDistReg.iterrows():
            query= "INSERT INTO aaj.mapUserByDistReg VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,tuple(row))
            mydb.commit()
        print("mapUserByDistReg values are inserted to MySQL....")
except Error:
    pass
    


# In[34]:


AggTransByStates


# In[5]:


AggTransByStates.dtypes


# # # Aggregated Transaction by States Data Inserting to MySQL

# In[6]:


import mysql.connector
from mysql.connector import Error
try:
    mydb =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aaj2606",
        database="aaj")
    if mydb.is_connected():  
        cursor= mydb.cursor()
        cursor.execute("use aaj;")
        cursor.execute("DROP TABLE IF EXISTS AggTransByStates;")
        cursor.execute("CREATE TABLE AggTransByStates                       (State varchar(100),                        Year int,                        Quater varchar(5),                        Transaction_type varchar(50),                        Transaction_count int,                        Transaction_amount float(50,3))")
        print("Agg Transaction By State table is created....")

        for i, row in AggTransByStates.iterrows():
            query="INSERT INTO aaj.AggTransByStates VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,tuple(row))
            mydb.commit()
        print("AGG Transaction By State values are inserted to MySQL....")
except Error:
    pass
    


# In[7]:


AggUserByBrand.dtypes


# # # Aggregated Users by Brand  Data Inserting to MySQL

# In[10]:


import mysql.connector
from mysql.connector import Error
try:
    mydb =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aaj2606",
        database="aaj")
    if mydb.is_connected():  
        cursor= mydb.cursor()
        cursor.execute("use aaj;")
        cursor.execute('DROP TABLE IF EXISTS AggUserByBrand;')
       
        cursor.execute("CREATE TABLE AggUserByBrand                       (State varchar(100),                        Year int,                        Quater varchar(5),                        Brand varchar(50),                        Brand_count int,                        Brand_percentage float(50,3))")
        print("AggUserByBrand table is created....")

        for i, row in AggUserByBrand.iterrows():
            query="INSERT INTO aaj.AggUserByBrand VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,tuple(row))
            mydb.commit()
        print("AggUserByBrand values are inserted to MySQL....")
except Error:
    pass


# In[ ]:


mapTransByDist.dtypes


# # Map Transaction by District Data Inserting to MySQL

# In[12]:


import mysql.connector
from mysql.connector import Error
try:
    mydb =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aaj2606",
        database="aaj")
    if mydb.is_connected():  
        cursor= mydb.cursor()
        cursor.execute("use aaj;")
        cursor.execute("CREATE TABLE mapTransByDistrict                       (State varchar(100),                        Year int,                        Quater varchar(5),                        District varchar(50),                        Transaction_count int,                        Transaction_amount float(50,3))")
        print("mapTransByDistrict table is created....")

        for i, row in mapTransByDistrict.iterrows():
            query="INSERT INTO aaj.mapTransByDistrict VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(query,tuple(row))
            mydb.commit()
        print("mapTransByDistrict values are inserted to MySQL....")
except Error:
    pass


# # Fetch the Data From MySQL Table to Python

# In[13]:


try:
    mydb = mysql.connector.connect(host='localhost',
                           database='aaj', user='root',
                           password='Aaj2606')
    if  mydb.is_connected():
        cursor = mydb.cursor()        
        cursor.execute("SELECT Users FROM map_user")
        records = cursor.fetchall()
        data=pd.DataFrame(records,
                    columns=[i[0] for i  in cursor.description])

        mydb.commit()
        cursor.close()
        mydb.close()  
        print("connecting to MySQL")
except Error as e:
    print("Error while connecting to MySQL", e)

data


# In[16]:


mapUserByDistReg_filter = np.where((mapUserByDistReg['State']=='gujarat') & (mapUserByDistReg['Year']==2022))
mapUserByDistReg_filter=mapUserByDistReg.loc[mapUserByDistReg_filter]
mapUserByDistReg_filter


# In[ ]:




