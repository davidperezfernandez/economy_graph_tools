USE economy_graph;


##############################################
#   DATA CLEANNING

# OUTLIERS TYPE 1
#   Double declared movements bigger than K with differences bigger than p*100 %

# Outlier type 1 flag column
ALTER TABLE relaciones_comerciales ADD COLUMN outlier_1 decimal(1) NOT NULL DEFAULT 0 AFTER VentaImputada;

# Move type 1 outliers to tblForm347_Outlier1_2013
#  K = 1000000
#  p = 0.2

SET @K1=1000000;
SET @p1=0.2;

# WHERE Imputed income IS NOT NULL AND Reported income IS NOT NULL
# AND ( |Imputed income - Reported income| > p*min⁡{Imputed income,reported income} AND max⁡{Imputed income,Reported income}>K 
# OR |Imputed income-Reported income|>p*K AND max⁡{Imputed income,Reported income}<K

# Compras = 1
UPDATE relaciones_comerciales SET outlier_1 = 1
WHERE 
( 
 ((CompraDeclarada > @K1 AND CompraImputada<>0) OR (CompraImputada > @K1 AND CompraImputada<>0)) AND 
 ( (ABS(CompraDeclarada - CompraImputada) > @p1*CompraDeclarada)  AND  (ABS(CompraDeclarada - CompraImputada) > @p1*CompraImputada))
OR
 ( abs(CompraDeclarada - CompraImputada) > @p1*@K1 AND (CompraDeclarada< @K1 AND CompraImputada < @K1) )
);
#(b.amount > 0) AND (s.amount > 0) ? Negative values ?

# Ventas = 2
UPDATE relaciones_comerciales SET outlier_1 = outlier_1 + 2
WHERE 
( 
 ((VentaDeclarada > @K1 AND VentaImputada<>0) OR (VentaImputada > @K1 AND VentaImputada<>0)) AND
 ( (ABS(VentaDeclarada - VentaImputada) > @p1*VentaDeclarada)  AND  (ABS(VentaDeclarada - VentaImputada) > @p1*VentaImputada))
OR
 ( abs(VentaDeclarada - VentaImputada) > @p1*@K1 AND (VentaDeclarada< @K1 AND VentaImputada < @K1) )
);

# Possible values:
#  0 = no outlier
#  1 = selling outlier type 1
#  2 = buying outlier type 1
#  3 = selling and buying outlier type 1




## OUTLIERS TYPE 2
## Outlier type 1 flag column
ALTER TABLE relaciones_comerciales ADD COLUMN outlier_2 decimal(1) NOT NULL DEFAULT 0 AFTER outlier_1;
#
##  Single declared movements bigger than K2 and suppose an increment of p2*100% from the last year 
#SET @K2=1000000;
#SET @p2=0.2;
#
## Compras = 1
#UPDATE relaciones_comerciales r SET outlier_2 = 1
#WHERE 
#(CompraDeclarada = 0 AND CompraImputada  > @K2 AND CompraImputada  > (SELECT  a.CompraImputada*(1+p2) FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND a.NiuImputado = r.NiuImputado)) OR 
#(CompraImputada  = 0 AND CompraDeclarada > @K2 AND CompraDeclarada > (SELECT a.CompraDeclarada*(1+p2) FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND s.NiuImputado = r.NiuImputado));
#
## Ventas = 2
#UPDATE relaciones_comerciales r SET outlier_2 = outlier_2 + 1
#WHERE 
#(VentaDeclarada = 0 AND VentaImputada  > @K2 AND VentaImputada  > (SELECT  a.VentaImputada*(1+p2) FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND a.NiuImputado = r.NiuImputado)) OR 
#(VentaImputada  = 0 AND VentaDeclarada > @K2 AND VentaDeclarada > (SELECT a.VentaDeclarada*(1+p2) FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND a.NiuImputado = r.NiuImputado));
##  Negative values ?
#
## Possible values:
##  0 = no outlier
##  1 = selling outlier type 1
##  2 = buying outlier type 1
##  3 = selling and buying outlier type 1
#






## OUTLIERS TYPE 3
## Negative values modify previous values
ALTER TABLE relaciones_comerciales ADD COLUMN outlier_3 decimal(1) NOT NULL DEFAULT 0 AFTER outlier_2;

## Mark true negative values: single declared & double declared not marked as outlier type 1
## Compras = 1
#UPDATE relaciones_comerciales SET outlier_3 = 1
#WHERE 
#((CompraDeclarada = 0 AND CompraImputada  < 0) OR (CompraDeclarada < 0 AND CompraImputada  = 0)) OR
#(CompraDeclarada < 0 AND CompraImputada  < 0 AND outlier_1 = 0);
#
## Ventas = 2
#UPDATE relaciones_comerciales SET outlier_3 = outlier_3 + 1
#WHERE 
#((VentaDeclarada = 0 AND VentaImputada  < 0) OR (VentaDeclarada < 0 AND VentaImputada  = 0)) OR
#(VentaDeclarada < 0 AND VentaImputada  < 0 AND outlier_1 = 0);

