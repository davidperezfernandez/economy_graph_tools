
#USE economy_graph;
drop table IF EXISTS Summary_2013;

#Create table to store the final results. There will be only one row stored in the final table
CREATE TABLE Summary_2013 (
	ID	Int(5) 	NOT NULL DEFAULT '0',
    TotalVentaDeclarada DECIMAL(20,2) DEFAULT '0',
    TotalVentaImputada  DECIMAL(20,2) DEFAULT '0',
    TotalCompraDeclarada DECIMAL(20,2) DEFAULT '0',
    TotalCompraImputada  DECIMAL (20,2) DEFAULT '0',
    AverageVD DECIMAL (20,2) DEFAULT '0', #Average venta declarada, for firms that have declared something in total
	AverageVI DECIMAL (20,2) DEFAULT '0',
	StdVD DECIMAL (20,2) DEFAULT '0', #Standard deviation of venta declarada
	StdVI DECIMAL (20,2) DEFAULT '0',
    NumberDeclarantes Int (20) DEFAULT '0', #Number of nodes that declare something - number of nodes in 347 graph
    NumberLinks Int (20) DEFAULT '0', #Number of links (possibly overestimate), will have more accurate after data cleaning, 
    NumberOfLinksVINotCD Int (20) DEFAULT '0', #Number of links such that VentaImputata != CompraDeclarada (and both not null)
	NumberOfLinksVCNull Int (20) DEFAULT '0', #Number of links such that There is VentaImputada but not CompraDeclarada in data
	NumberOfLinksVNullC Int(20) DEFAULT '0', #Number of links such that VentaImputada is null but Compra Declarada is in the data
	TotalDifVICD DECIMAL (20,2) DEFAULT '0', # Total differnce between Venta Imputada and Compra Declarada in the data
	TotalDifVICDB decimal (20,2) default '0', # Total difference between Venta Imputada and Compra Declarada when both positive
	PRIMARY KEY (ID)
) ENGINE=MYISAM;


#Create view with aggregate node info. Couls have done is without this step, but will need it later. Put into
drop view IF EXISTS Totals;

create view Totals as Select NiuDeclarante, sum(If(VentaDeclarada>0,VentaDeclarada,0)) 'TVD', sum(if(VentaImputada>0, VentaImputada, 0)) 'TVI',
sum(if(CompraDeclarada>0, CompraDeclarada, 0)) 'TCD', sum(if(CompraImputada>0, CompraImputada, 0))'TCI',
abs(if(VentaImputada>0, VentaImputada, 0) -if(CompraDeclarada>0, CompraDeclarada, 0)) 'DIFVICD',
if (VentaImputada>0 and CompraDeclarada >0, abs(VentaImputada-CompraDeclarada),0) 'DIFVICDB' from relaciones_comerciales group by NiuDeclarante;

#Preparing the first row od Summary_2013 to fill it in with calculated statistics
Insert into Summary_2013 values(1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

#Calculating statistics to fill in Summary_2013 table. 
Replace into Summary_2013
(ID, TotalVentaDeclarada,TotalVentaImputada, TotalCompraDeclarada, TotalCompraImputada,AverageVD,AverageVI,StdVD,StdVI,TotalDifVICD, NumberDeclarantes,TotalDifVICDB) 
select 1, sum(TVD)'TVDT', sum(TVI) 'TVIT',sum(TCD) 'TCDT', sum(TCI) 'TCIT',
avg(If (TVD>0,TVD, NULL)) 'AVD', avg(If(TVI>0,TVI, NULL)) 'AVI', std(If(TVD>0,TVD, NULL)) 'STDVD',
std(If(TVI>0,TVI, NULL)) 'STDVI', sum(DIFVICD), Count(*), Sum(DIFVICDB)
From Totals;

update Summary_2013 set NumberLinks = (select count(*) from relaciones_comerciales), 
NumberOfLinksVCNull = (select count(*) from relaciones_comerciales where VentaImputada>=0 AND CompraDeclarada is null),
NumberOfLinksVNullC = (select count(*) from relaciones_comerciales where VentaImputada is null AND CompraDeclarada >=0),
NumberOfLinksVINotCD = (select count(*) from relaciones_comerciales where VentaImputada >= 0 AND CompraDeclarada >=0 and VentaImputada!=CompraDeclarada)
where id=1;
 
SELECT *
FROM Summary_2013
