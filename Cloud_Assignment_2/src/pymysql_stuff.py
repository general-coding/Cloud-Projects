import pymysql, csv

conn = pymysql.connect('usaeq.cavhaazwjuoq.us-east-1.rds.amazonaws.com',
                       'puneeth',
                       'bharadwaj',
                       local_infile=1)
 
cursor = conn.cursor()
 
cursor.execute('use usaeq')

create_table_string = """create table usaeq(
                            eq_time timestamp, 
                            eq_latitude double, 
                            eq_longitude double, 
                            eq_depth double, 
                            eq_mag double, 
                            eq_magType varchar(20), 
                            eq_nst double,
                            eq_gap double, 
                            eq_dmin double, 
                            eq_rms double, 
                            eq_net varchar(20), 
                            eq_id varchar(20), 
                            eq_updated timestamp, 
                            eq_place varchar(100), 
                            eq_type varchar(20)
                            );""" 
   
cursor.execute(create_table_string)
fname = "all_month.csv"
count = 0

train_dict = {}
result = []

first_line = True
outfile = open('outfile.csv', 'w')
with open(fname, 'r') as csvfile:
    for line in csvfile.readlines():
        if first_line:
            first_line = False
            continue
        result.append(tuple(line.split(",")))
 
        for r in result:
            p = [str(x) for x in r]
            p = tuple(p)
            query = 'insert into test values("%s", %s, %s, %s, %s, "%s", %s, %s, %s, %s, "%s", "%s", "%s", %s%s, "%s")' % p
            
            outfile.write(",".join(p))
            
            cursor.execute('insert into test values("%s", %s, %s, %s, %s, "%s", %s, %s, %s, %s, "%s", "%s", "%s", %s%s, "%s")' % p)
 
        count = count + 1
  
        if count == 1:
            break

cursor.execute("""load data local infile 'all_month.csv' 
                into table test 
                fields terminated by ',' 
                enclosed by '\"' lines 
                terminated by '\n';""")
 
 
outfile.close()
cursor.execute('commit')
cursor.close()
conn.close()