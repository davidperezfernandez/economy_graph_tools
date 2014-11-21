@echo off
set /a cnt=1
:Main
	if /i "%1"=="" goto :ExecJava
	set p%cnt%=%1
	shift
	set /a cnt=%cnt%+1
	goto :Main
:ExecJava
java -Xmx2048m -Xms256m -cp "./lib/*":csv2graph-1.0.jar:. org.economygraph.Csv2graph %p1%  %p2%  %p3%  %p4%  %p5%  %p6%  %p7%  %p8%  %p9%  %p10%  %p11%  %p12%  %p13%  %p14%  %p15%  %p16%  %p17%  %p18%  %p19%  %p20%  

rem Example usage: csv2graph.bat -vectorfile ./test/vectors.csv
rem Example usage: csv2graph.bat -g -vectorfile ./test/vectors.csv  
