import pandas as pd
from datetime import datetime, date
# import csv

df = pd.read_excel('C:/Users/huy.nguyenq5/Downloads/messy.xlsx', sheet_name='test')


# 1 Clean the names of columns to lowercase separated by “_”, remove any empty
# column if necessary.
# 2 Change the date column to the same format ‘YYYY-MM-DD’.
# 3 Change the name column to the title case (e.g: Jason Mraz).
# 4 Make a new “email” column with the form:
# {last_name}.{first_name}.{id}@yourcompany.com
# 5 Change the phone number column to the format “84……”
# 6 Find any duplicated ID and remove those who join later.
# 7 Filter those who join since 2019 and export to a csv file, delimited by “|”, file name
# “emp_{report_date}.csv” with report_date = today.
# ================================================================================================


# 1 Clean the names of columns to lowercase separated by “_”, remove any empty
df.columns
df.columns = df.columns.str.lower()
df = df.drop('unnamed: 2', axis=1)
df.columns = ['cust_id', 'join_date', 'phone','full_name']
# df.columns = df.columns.str.replace('$', '')
# df.columns = df.columns.str.replace([' ','%'], [''])\\\\

# 2 Change the date column to the same format ‘YYYY-MM-DD’.
def split_date(x):
    s1 = x.split(" ")
    if len(s1) == 2:
        s2 = s1[0]
        return s2
    try:
        return x
    except:
        return None
    
df['join_date'] = df['join_date'].apply(split_date)
df['join_date'] = pd.to_datetime(df['join_date']).dt.date
# df['  JOIN% DATE'] = pd.to_datetime(df['  JOIN% DATE']).dt.normalize()


# 3 Change the name column to the title case (e.g: Jason Mraz).
df['full_name'] = df['full_name'].str.title()

# 4 Make a new “email” column with the form: {last_name}.{first_name}.{id}@yourcompany.com
#====== Option 1
email_arr2 = []
for i in range(0, len(df)):
    split_name = df['full_name'][i].split()
    lst_name = split_name[0]
    fst_name = split_name[1]
    id1 = str(df['cust_id'][i])
    email = '{last_name}.{first_name}.{id}@yourcompany.com'.format(last_name = lst_name,first_name = fst_name,id=id1)
    email_arr2.append(email)

df['email2'] = email_arr2

#====== Option 2
email_arr = []
for i in range(0, len(df)):
    split_name = df['full_name'][i].split()
    last_name = split_name[0]
    first_name = split_name[1]
    id = str(df['cust_id'][i])
    email = '%s.%s.%s@yourcompany.com' %(last_name,first_name,id)
    email_arr.append(email)
df['email'] = email_arr

# 5 Change the phone number column to the format “84……”
df['phone']=df['phone'].astype(str)
df['phone'] = df['phone'].apply(lambda x: x if x.startswith('84') else "84"+x)

# 6 Find any duplicated ID and remove those who join later.

#==== Find any duplicated ID
df_idDup = df[df['cust_id'].duplicated()]

#==== remove those who join later
df = df.drop_duplicates( "cust_id" , keep='first')

#==== remove those who join first
# df.drop_duplicates( "cust_id" , keep='last')

# 7 Filter those who join since 2019 and export to a csv file, delimited by “|”, file name
#==== “emp_{report_date}.csv” with report_date = today.
df.info()
df_19 = df[df.join_date >= date(2019,1,1)].reset_index(drop=True)

#==== export to a csv file
df_19.to_csv('emp_{}.csv'.format(date.today()), sep ='|')












