/*
	Script para calcular metricas (Clustering)
*/

drop table if exists #temp_principal;
drop table if exists #temp_snacksyalcohol;
drop table if exists #temp_pets;
drop table if exists #temp_babies;
drop table if exists #temp_produce;
drop table if exists #temp_dairyeggs;

/*
	Genero las metricas de hora de compra promedio y frecuencia de compra [dias]
*/
select user_id, 
	avg(cast(order_hour_of_day as float)) as AVG_Hour_Of_Day,
	avg(cast(days_since_prior_order as float)) as AVG_Days_Since_Prior_Order,
	count(ord.product_id) as Cantidad_Productos,
	count(distinct o.order_id) as Cantidad_Ventas,
	case 
		when (count(distinct o.order_id) > 0 and (avg(cast(days_since_prior_order as float)))>0) then
			(count(ord.product_id) * 30) / 
				(avg(cast(days_since_prior_order as float))*count(distinct o.order_id)) 
					
		else 0
	end as Cantidad_Productos_Vendidos_Por_Mes
into #temp_principal
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
where eval_set = 'prior' and esUtil = 1
group by user_id;


/*
	Genero metrica de cant de productos para algunas categorias relevantes
*/
select user_id, count(*) as Cantidad_SnacksYAlcohol
into #temp_snacksyalcohol
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p 
	on p.id = ord.product_id
inner join departments d 
	on d.id = p.department_id
where department in ('snacks','alcohol') and eval_set = 'prior' and esUtil = 1
group by user_id
;

select user_id, 0+count(*) as Cantidad_Babies
into #temp_babies
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p 
	on p.id = ord.product_id
inner join departments d 
	on d.id = p.department_id
where department in ('babies') and eval_set = 'prior' and esUtil = 1
group by user_id
;

select user_id, 0+count(*) as Cantidad_Produce
into #temp_produce
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p 
	on p.id = ord.product_id
inner join departments d 
	on d.id = p.department_id
where department in ('produce') and eval_set = 'prior' and esUtil = 1
group by user_id
;

select user_id, 0+count(*) as Cantidad_Pets
into #temp_pets
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p 
	on p.id = ord.product_id
inner join departments d 
	on d.id = p.department_id
where department in ('pets') and eval_set = 'prior' and esUtil = 1
group by user_id
;

select user_id, 0+count(*) as Cantidad_dairyeggs
into #temp_dairyeggs
from orders o
inner join ordenes ord
	on o.order_id = ord.order_id
inner join products p 
	on p.id = ord.product_id
inner join departments d 
	on d.id = p.department_id
where department in ('dairy eggs') and eval_set = 'prior' and esUtil = 1
group by user_id
;


(select 'User_ID,AVG_Hour_Of_Day,AVG_Days_Since_Prior_Order,Cantidad_Productos,Cantidad_Ventas,Cantidad_Categoria_Babies,Cantidad_Categoria_Pets,Cantidad_Categoria_SnacksYAlcohol,Cantidad_Categoria_Produce,Cantidad_Categoria_DairyEggs'
union
select CONCAT(p.user_id,',',p.AVG_Hour_of_Day,',',p.AVG_Days_Since_Prior_Order,',',p.cantidad_productos,',',p.cantidad_ventas,',',
	case 
		when cantidad_babies is null then 0
		else cast (Cantidad_Babies as float)/cast(p.Cantidad_Productos as float)
	end --as Cantidad_Babies
	, ',',
	case 
		when Cantidad_Pets is null then 0
		else cast(Cantidad_Pets as float)/cast(p.Cantidad_Productos as float)
	end --as Cantidad_Pets
	,',',
	case 
		when cantidad_snacksyalcohol is null then 0
		else cast(Cantidad_SnacksYAlcohol as float)/cast(p.Cantidad_Productos as float)
	end --as Cantidad_SnacksYAlcohol,
	,',',
	case 
		when pr.cantidad_produce is null then 0
		else cast(pr.cantidad_produce as float)/cast(p.Cantidad_Productos as float)
	end --as Cantidad_Produce,
	,',',
	case 
		when d.cantidad_dairyeggs is null then 0
		else cast(d.cantidad_dairyeggs as float)/cast(p.Cantidad_Productos as float)
	end --as Cantidad_DairyEggs
)
from #temp_principal p
left join #temp_produce pr
	on p.user_id = pr.user_id
left join #temp_dairyeggs d
	on p.user_id = d.user_id
left join #temp_babies b
	on p.user_id = b.user_id
left join #temp_pets pe
	on p.user_id = pe.user_id
left join #temp_snacksyalcohol sya
	on sya.user_id = p.user_id
)
order by 1 desc;
