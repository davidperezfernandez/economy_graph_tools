USE economy_graph;

drop table IF EXISTS Aggregates_2013;

#Create table to store the final results. There will be only one row stored in the final table
CREATE TABLE Aggregates_2013 (
	Niu Int(5) 	NOT NULL DEFAULT '0',
    TVD DECIMAL(20,2) DEFAULT '0',
    TVI  DECIMAL(20,2) DEFAULT '0',
    TCD DECIMAL(20,2) DEFAULT '0',
    TCI DECIMAL (20,2) DEFAULT '0',
	PRIMARY KEY (Niu)
) ENGINE=MYISAM;


Insert into Aggregates_2013 select NiuDeclarante, sum(VentaDeclarada), sum(VentaImputada), sum(CompraDeclarada), sum(CompraImputada)
from relaciones_comerciales
group by NiuDeclarante;

