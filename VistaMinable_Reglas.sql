create view vista as
(select o.order_id, o.user_id, o.order_number, o.order_dow, o.order_hour_of_day, days_since_prior_order, product_id, product_name, aisle_id, aisle, department_id, department, esUtil
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p
	on p.id = ord.product_id
inner join departments d
	on d.id = p.department_id
inner join aisles a
	on a.id = p.aisle_id
where esUtil = 1 and eval_set = 'train');

--drop view vista

select ('Order_ID,User_ID,Order_Number,Order_Dow,Order_Hour_of_Day,Days_since_prior_order,Product_ID,Product_name,Aisle_ID,Aisle,Department_ID,Department,Quantity')
union
select CONCAT(
	order_id, ',',
	user_id, ',',
	order_number, ',',
	order_dow, ',',
	order_hour_of_day, ',',
	days_since_prior_order, ',',
	product_id, ',',
	product_name, ',',
	aisle_id, ',',
	aisle, ',',
	department_id, ',',
	department, ',',
	1)
from vista
where esUtil = 1
order by 1 desc;
