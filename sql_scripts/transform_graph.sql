# set schema
USE economy_graph;


DROP TABLE IF EXISTS tblForm34x_2013;

CREATE TABLE tblForm34x_2013(	
	SOURCENIU			NUMERIC(11),
	TARGETNIU			NUMERIC(11),
	AMOUNT				NUMERIC(16,2),
	PRIMARY KEY (SOURCENIU,TARGETNIU)
);

# Flow: goods, no money flow

# SINGLE DECLARED
# Ventas
INSERT INTO tblForm34x_2013 
SELECT 		
	NiuDeclarante,	
	NiuImputado,
	if(VentaDeclarada IS NOT NULL, VentaDeclarada, VentaImputada)
FROM relaciones_comerciales
WHERE 
( (VentaDeclarada > 0 AND VentaImputada IS NULL) OR (VentaDeclarada IS NULL AND VentaImputada > 0) ) AND 
(outlier_1 + outlier_2 + outlier_3 = 0);



# DOUBLE DECLARED
# Take bigger values for double declared operations

# erase outliers

# Ventas
INSERT INTO tblForm34x_2013 
SELECT 	
	NiuDeclarante, 
	NiuImputado, 
	if(VentaDeclarada >= VentaImputada, VentaDeclarada, VentaImputada)
FROM relaciones_comerciales
WHERE 
( VentaDeclarada >= 0 AND VentaImputada >= 0 ) AND 
  (outlier_1 + outlier_2 + outlier_3 = 0);



  
