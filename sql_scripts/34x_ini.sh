#!/bin/bash

# TODO pass year parameter

# only local test
echo 'load_data_347........'
mysql -f -u root -proot666 -h localhost < load_data_347.sql

echo 'mark_outliers_347........'
mysql -f -u root -proot666 -h localhost < mark_outliers_347.sql
#mysql -f -u root -proot666 -h localhost < cleaning_347.sql

echo 'transform_graph........'
mysql -f -u root -proot666 -h localhost < transform_graph.sql

# Export
echo 'export........'
rm ./test/FORM34x_2013_VECTORS.csv
mysql -f -u root -proot666 -h localhost economy_graph -e "select concat(TARGETNIU,',',SOURCENIU,',',AMOUNT) 'SOURCENIU, TARGETNIU, AMOUNT' FROM tblForm34x_2013 order by SOURCENIU, TARGETNIU" > ./test/FORM34x_2013_VECTORS.csv

#rm ./test/FORM34x_2013_NODES.csv
#mysql -f -u root -proot666 -h localhost economy_graph -e "select concat(ID,',',AUT,',',EPI,',',PROFIT,',',SALES,',',PURCHASES,',',NEMP,',',NIU,',',NAME) 'ID, AUT, EPI, PROFIT, SALES, PURCHASES, NEMP, NIU, NAME' FROM tblTaxFillers34x_2013 order by ID" > ./test/FORM34x_2013_NODES.csv


# Summary
mysql -f -u root -proot666 -h localhost economy_graph < Summary_347_SingleYear29112014
	


