from boto.s3.connection import S3Connection
import csv, os, pymysql

AWSAccessKeyId = AWSAccessKeyId
AWSSecretKey = AWSSecretKey


def s3_stuff(): 
    s3_conn = S3Connection(AWSAccessKeyId, AWSSecretKey)
     
    bucket = s3_conn.get_bucket('your-bucket-name')
     
    for file_key in bucket.list():
        print(file_key)
        infname = file_key.name
        file_key.get_contents_to_filename('./csvfiles/'+infname)
    
    infile = open('./csvfiles/'+infname, 'r')
    outfile = open('./csvfiles/input_to_s3_nofirstline.csv', 'w')
    firstline = 1
     
    try:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if firstline == 1:
                firstline = 0
                pass
            else:
                writer.writerow(row)
    finally:
        infile.close()
        outfile.close()
        
    os.rename('./csvfiles/input_to_s3_nofirstline.csv', './csvfiles/'+infname)

def mysql_stuff():
    print('Connecting to RDS...')
    conn = pymysql.connect('your-rds-endpoint',
                           'username',
                           'password',
                           local_infile=1)
    
    print('Creating cursor...')
    cursor = conn.cursor()
    
    print('Cursor use')
    cursor.execute('use usaeq')
    
    print('Cursor drop')
    cursor.execute("drop table if exists usaeq")
    
    print('Cursor create')
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
                                eq_net varchar(100), 
                                eq_id varchar(20), 
                                eq_updated timestamp, 
                                eq_place varchar(100), 
                                eq_type varchar(20)
                            );""" 
    
    print('Cursor execute')
    cursor.execute(create_table_string)
    
    print('Loading data into RDS..')
    cursor.execute("""load data local infile './csvfiles/all_month.csv' 
                    into table usaeq 
                    fields terminated by ',' 
                    enclosed by '\"'
                    lines terminated by '\n'
                    ignore 1 lines;""")
     
    print('Cursor commit')
    cursor.execute('commit')
    
    print('Cursor select')
    cursor.execute("select count(1) from usaeq")
    rows_loaded =cursor.fetchall()
    print(rows_loaded)
    
    print('2000 Random queries')
    query = 'select * from usaeq group by rand() limit 10'
    restricted_query = 'select * from (select * from usaeq limit 2000) A group by rand() limit 10'
    for i in range(1,2000):
        cursor.execute(restricted_query) 
    
    cursor.close()
    conn.close()
    
s3_stuff()
mysql_stuff()
