create table usaeq(
	eq_time	timestamp,
	eq_latitude	int(10) unsigned,
	eq_longitude int(10) unsigned,
	eq_depth decimal(6,6),
	eq_mag decimal(6,6),
	eq_magType varchar(20),
	eq_nst int,
	eq_gap 	decimal(6,6),
	eq_dmin decimal(6,6),
	eq_rms decimal(6,6),
	eq_net varchar(20),
	eq_id varchar(20),
	eq_updated timestamp,
	eq_place varchar(100),
	eq_type varchar(20)
);

select 
    week, count(mag2) as mag2, count(mag3) as mag3, count(mag4) as mag4, count(mag5) as mag5
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
group by week;
