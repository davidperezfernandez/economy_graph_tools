# set schema
USE economy_graph;


DROP TABLE IF EXISTS tblForm34x_2013;

CREATE TABLE tblForm34x_2013(	
	SOURCENIU			NUMERIC(11),
	TARGETNIU			NUMERIC(11),
	AMOUNT				NUMERIC(16,2),
	PRIMARY KEY (SOURCENIU,TARGETNIU)
);

# Flow: goods no maney flow

# SINGLE DECLARED
# Compras
INSERT INTO tblForm34x_2013 
SELECT 	
	if(CompraDeclarada > CompraImputada, NiuImputado,     NiuDeclarante),
	if(CompraDeclarada > CompraImputada, NiuDeclarante,   NiuImputado),
	if(CompraDeclarada > CompraImputada, CompraDeclarada, CompraImputada)
FROM relaciones_comerciales
WHERE 
(NiuDeclarante > NiuImputado) AND
( (CompraDeclarada > 0 AND CompraImputada = 0) OR (CompraDeclarada = 0 AND CompraImputada > 0) ) AND 
(outlier_1 + outlier_2 + outlier_3 = 0);
# just for testing purposes: no outliers

# Ventas
INSERT INTO tblForm34x_2013 
SELECT 	
	if(VentaDeclarada >= VentaImputada, NiuDeclarante,  NiuImputado),
	if(VentaDeclarada >= VentaImputada, NiuImputado,	NiuDeclarante),
	if(VentaDeclarada >= VentaImputada, VentaDeclarada, VentaImputada)
FROM relaciones_comerciales
WHERE 
(NiuDeclarante > NiuImputado) AND
( (VentaDeclarada > 0 AND VentaImputada = 0) OR (VentaDeclarada = 0 AND VentaImputada > 0) ) AND 
(outlier_1 + outlier_2 + outlier_3 = 0);






# DOUBLE DECLARED
# Take bigger values for double declared operations

# erase outliers

# Compras
INSERT INTO tblForm34x_2013 
SELECT 	
	if(CompraDeclarada >= CompraImputada, NiuImputado,     NiuDeclarante),
	if(CompraDeclarada >= CompraImputada, NiuDeclarante,   NiuImputado),
	if(CompraDeclarada >= CompraImputada, CompraDeclarada, CompraImputada)
FROM relaciones_comerciales
WHERE 
(NiuDeclarante > NiuImputado) AND
( CompraDeclarada > 0 AND CompraImputada > 0 ) AND 
  (outlier_1 + outlier_2 + outlier_3 = 0);


# Ventas
INSERT INTO tblForm34x_2013 
SELECT 	
	if(VentaDeclarada >= VentaImputada, NiuDeclarante,  NiuImputado),
	if(VentaDeclarada >= VentaImputada, NiuImputado,    NiuDeclarante),
	if(VentaDeclarada >= VentaImputada, VentaDeclarada, VentaImputada)
FROM relaciones_comerciales
WHERE 
(NiuDeclarante > NiuImputado) AND
( VentaDeclarada > 0 AND VentaImputada > 0 ) AND 
  (outlier_1 + outlier_2 + outlier_3 = 0);
