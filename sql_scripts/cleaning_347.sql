USE economy_graph;


##############################################
#   DATA CLEANNING

# TEST: REMOVE ALL OUTLIERS
DELETE FROM relaciones_comerciales 
WHERE 
(outlier_1 > 0) OR (outlier_2 > 0) OR (outlier_3 > 0);