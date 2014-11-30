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

# Ventas = 1
UPDATE relaciones_comerciales SET outlier_1 = 1
WHERE 
( 
 ((VentaDeclarada > @K1 AND VentaImputada<>0) OR (VentaImputada > @K1 AND VentaImputada<>0)) AND
 ( (ABS(VentaDeclarada - VentaImputada) > @p1*VentaDeclarada)  AND  (ABS(VentaDeclarada - VentaImputada) > @p1*VentaImputada))
OR
 ( abs(VentaDeclarada - VentaImputada) > @p1*@K1 AND (VentaDeclarada< @K1 AND VentaImputada < @K1) )
);



## OUTLIERS TYPE 2
## Outlier type 1 flag column
ALTER TABLE relaciones_comerciales ADD COLUMN outlier_2 decimal(1) NOT NULL DEFAULT 0 AFTER outlier_1;
#
##  Single declared movements bigger than K2 and suppose an increment of p2*100% from the last year 
#SET @K2=1000000;
#SET @p2=0.2;
#
## Ventas = 2
#UPDATE relaciones_comerciales r SET outlier_2 = 1
#WHERE 
#(VentaDeclarada = 0 AND VentaImputada  > @K2 AND VentaImputada  > (SELECT a.VentaImputada*(1+p2)  FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND a.NiuImputado = r.NiuImputado)) OR 
#(VentaImputada  = 0 AND VentaDeclarada > @K2 AND VentaDeclarada > (SELECT a.VentaDeclarada*(1+p2) FROM relaciones_comerciales_anterior a WHERE a.NiuDeclarante = r.NiuDeclarante AND a.NiuImputado = r.NiuImputado));


##  Negative values ?
#




## OUTLIERS TYPE 3
## Negative values modify previous values
ALTER TABLE relaciones_comerciales ADD COLUMN outlier_3 decimal(1) NOT NULL DEFAULT 0 AFTER outlier_2;

## Mark true negative values: single declared & double declared not marked as outlier type 1
#
## Ventas = 2
#UPDATE relaciones_comerciales SET outlier_3 = 1
#WHERE 
#((VentaDeclarada = 0 AND VentaImputada  < 0) OR (VentaDeclarada < 0 AND VentaImputada  = 0)) OR
#(VentaDeclarada < 0 AND VentaImputada  < 0 AND outlier_1 = 0);

