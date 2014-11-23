USE economy_graph;

DROP TABLE IF EXISTS relaciones_comerciales;
CREATE TABLE relaciones_comerciales (
	NiuDeclarante	DECIMAL(11,0) 	NOT NULL DEFAULT '0',
	NifDeclarante	CHAR(9)			DEFAULT NULL,
	NiuImputado		DECIMAL(11,0) 	NOT NULL DEFAULT '0',
	NifImputado		CHAR(9) 		DEFAULT NULL,
	CompraDeclarada	DECIMAL(15,2) 	DEFAULT NULL,
	CompraImputada	DECIMAL(15,2) 	DEFAULT NULL,
	VentaDeclarada	DECIMAL(15,2) 	DEFAULT NULL,
	VentaImputada	DECIMAL(15,2) 	DEFAULT NULL,
	PRIMARY KEY (NiuDeclarante,NiuImputado)
) ENGINE=MYISAM;


# load data
LOAD DATA LOCAL INFILE "./test/DATA347_2013.csv" REPLACE INTO TABLE relaciones_comerciales  
	CHARACTER SET UTF8 
	FIELDS 
		OPTIONALLY ENCLOSED BY '"' TERMINATED BY ',' ESCAPED BY '\\'  
	LINES 
		TERMINATED BY '\n'
	IGNORE 1 LINES;


