'''
Created on Feb 28, 2015

@author: puneeth
'''

import os, time, MySQLdb, memcache

def s3_stuff():
    start = time.time()
    os.system("aws s3 cp ./csvfiles/all_month.csv s3://your-bucket-name-/all_month.csv --acl public-read")
    end = time.time()
    
    runtime = end - start
    
    print("Upload time to s3", runtime)

    start = time.time()
    os.system("aws s3 cp s3://your-bucket-name/all_month.csv all_month.csv")
    end = time.time()
    
    s3_time = end-start
    print("Download time from S3", s3_time)
    
def mysql_stuff():
    print('Connecting to RDS...')
    conn = MySQLdb.connect('your-rds-endpoint',
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
    
    start = time.time()
    print('Loading data into RDS..')
    cursor.execute("""load data local infile 'all_month.csv' 
                    into table usaeq 
                    fields terminated by ',' 
                    enclosed by '\"'
                    lines terminated by '\n'
                    ignore 1 lines;""")
    end = time.time()
    mysql_time = end - start
    print("Load time to RDS", mysql_time)
    
    print('Cursor commit')
    cursor.execute('commit')
    
    print('Cursor select')
    cursor.execute("select count(1) from usaeq")
    rows_loaded =cursor.fetchall()
    print(rows_loaded)
    
    print('Time magnitude')
    query = """select week as 'Week |', count(mag2) as '2 - 2.99 |', count(mag3) as '3 - 3.99 |', count(mag4) as '4 - 4.99 |', count(mag5) as '>= 5 |'
                from
                    ((select 
                        case
                                when date(eq_time) between cast('2015-01-20' as date) and cast('2015-01-26' as date) then 1
                                when date(eq_time) between cast('2015-01-27' as date) and cast('2015-02-02' as date) then 2
                                when date(eq_time) between cast('2015-02-03' as date) and cast('2015-02-09' as date) then 3
                                when date(eq_time) between cast('2015-02-10' as date) and cast('2015-02-16' as date) then 4
                                when date(eq_time) between cast('2015-02-17' as date) and cast('2015-02-23' as date) then 5
                                when date(eq_time) between cast('2015-02-24' as date) and cast('2015-02-29' as date) then 6
                            end week,
                            usaeq.eq_id
                    from
                        usaeq) as week, (select 
                        case
                                when eq_mag between 2 and 2.99 then eq_mag
                            end mag2,
                            usaeq.eq_id
                    from
                        usaeq) as mag2, (select 
                        case
                                when eq_mag between 3 and 3.99 then eq_mag
                            end mag3,
                            usaeq.eq_id
                    from
                        usaeq) as mag3, (select 
                        case
                                when eq_mag between 4 and 4.99 then eq_mag
                            end mag4,
                            usaeq.eq_id
                    from
                        usaeq) as mag4, (select 
                        case
                                when eq_mag >= 5 then eq_mag
                            end mag5,
                            usaeq.eq_id
                    from
                        usaeq) as mag5)
                where
                    week.eq_id = mag2.eq_id and
                    week.eq_id = mag3.eq_id and
                    week.eq_id = mag4.eq_id and
                    week.eq_id = mag5.eq_id 
                group by week;"""                
    start = time.time()
    cursor.execute(query)
    end = time.time()
    time_mag_time = end - start
    print('Time magnitude query', time_mag_time)

    rows = cursor.fetchall()
    desc = cursor.description
    print('---------------------------------------------------------------')
    print('Time | \t Magnitude \t \t \t \t \t      |')
    print('---------------------------------------------------------------')
    print("%s \t %s \t %s \t %s \t %s \t " % (desc[0][0], desc[1][0], desc[2][0], desc[3][0], desc[4][0]))
    for row in rows:
        print('---------------------------------------------------------------')
        print("%s    | \t %s \t  | \t %s \t  | \t %s \t  | \t %s   | " % row)
    print('---------------------------------------------------------------')    

    print('2000 Random queries')
    start = time.time()
    query = 'select eq_time from usaeq group by rand() limit 10'
    for i in range(1, 2000):
        cursor.execute(query)
    end = time.time()
    rand_time = end - start
    print('Time for 2000 random queries', rand_time)

    print('Limited queries')
    start = time.time()
    restricted_query = 'select * from (select eq_id from usaeq limit 2000) A group by rand() limit 10'
    for i in range(1,2000):
        cursor.execute(restricted_query) 
    end = time.time()
    lim_time = end - start
    print('Time for limited queries', lim_time)
    
    cursor.close()
    conn.close()

def memcache_stuff():
    memc = memcache.Client(['127.0.0.1:11211'], debug=1);
    try:
        conn = MySQLdb.connect('your-rds-endpoint',
                           'username',
                           'password',
                           'usaeq')
    
    except MySQLdb.Error, e:
         print "Error %d: %s" % (e.args[0], e.args[1])
         sys.exit (1)
    
    count = 0
    start = time.time()
    for i in range(1,2000):
        usaeq = memc.get('usaeq')
        if not usaeq:
            cursor = conn.cursor()
            cursor.execute('select * from usaeq order by eq_time limit 5')
            rows = cursor.fetchall()
            memc.set('usaeq',rows,3600)
            print "Updated memcached with MySQL data"
        else:
#            print "Loaded data from memcached", i
            count = count + 1
    end = time.time()
    print(count)
    rand_time = end - start
    print("Time for 2000 random queries using memcache", rand_time)

    count = 0
    start = time.time()
    for i in range(1,2000):
        usaeqrd = memc.get('usaeqrd')
        if not usaeqrd:
            cursor = conn.cursor()
            cursor.execute('select * from (select eq_time from usaeq limit 2000) A group by rand() limit 10')
            rows = cursor.fetchall()
	    memc.set('usaeqrd', rows, 3600)
	    print "Updated memcached with MySQL data for limited scope"
	else:
#	     print "Loaded data from memcached limited scope", i
	    count = count + 1
    end = time.time()
    print(count)
    limrand_time = end - start
    print("Time for 2000 random limited queries using memcache", limrand_time)    

s3_stuff()
mysql_stuff()
memcache_stuff()
