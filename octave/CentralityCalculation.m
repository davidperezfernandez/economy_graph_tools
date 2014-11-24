%Main testing, exact solution, mldivide, Octave version 3.0
%Everything in single file
%Using an updated reading from dot file function
%Ignoring list of labels at the begining of dot file
%Writing output inot CSV file
%Using sparse matrix
%No calculation for active firms
%Calculaing centrality using mldivide
%01.09.2014
%Kenan Huremovic, 



%How to use:
%Need to specify file from which data are loaded
%Need to specify the  output name in csv write function

clear all; %empty the containers
%matlabpool open 
%------------------------------------------------------------------------
%Parameters
alpha =0.55;
beta = 0.3;
w=beta;

%Specify input and output file
fileinput ='FORM34x_2013_VECTORS_normalized.dot';
fileoutput ='FORM34x_2013_VECTORS_centrality.csv';

%------------------------------------------------------------------------
%Testing with random matrix
 %dim=10000;
 %G=sprand(dim,dim,0.001);
 
%--------------------------------------------------------------------------
%Findig the number of nodes in graph (finding occurance of '>' for the first
%time in .dot file)

fileID = fopen(fileinput,'r');
line  = 0;
   while 1
   tline = fgetl(fileID);
   line = line + 1;
   if ischar(tline)
       startRow = strfind(tline, '>');
       if ~isempty(startRow)
           break
       end
   end
end
clear tline, startRow;
fclose(fileID);
%-----------------------------------------------------------------------------
%Reading the graph
tic()

%Consumtion vector
%%Consumption vector, should be loaded from data, for now generated 
%%% Assume all goods are consumption goods as a benchmark, and all are symmetric
dim=line-2; 
co=1/dim*ones(dim,1);
c=sparse(co);
clear co;

%Loading graph datta
%[L1, L2, L3]= textread('C:\Users\User\Dropbox\EmpiricalProductionNetwork\OctaveLocal\Second Iteration\WeightHeaderTest.dot','%d -> %d [weight="%f"] %*s','delimiter',';','headerlines',1);
[L1, L2, L3]= textread(fileinput,'%d -> %d [w="%f"];','delimiter','\n}','headerlines',line-1);
%%calculating number of nodes, assuming nodes have sequential numerical
%%labels
%converting to linear indices
pause;
G=sparse(dim, dim);
for i=1:size(L1)(1)-1
  G(L1(i)+1,L2(i)+1)=L3(i);
end
% 
 clear L1 L2 L3;
disp('loading data:')
toc() 
%----------------------------------------------------------------------
%Preparing matrix - normalization:
tic()
G=G*spdiags((1./sum(G))',0,dim,dim); %Normalization - creating G matrix from adjacency matrix, 
disp('Preparing matrix/normalization:')
toc()

%------------------------------------------------------------------------
%Calculating centrality:
tic()
cent = mldivide(speye(dim)-alpha*G,((1-alpha)*w/beta)*c);
%cent1 = pinv(speye(dim)-alpha*G)*((1-alpha)*w/beta)*c;
disp('Calculation:')
toc()
%sum(cent) %Check if centralities add up to one
dlmwrite(fileoutput, cent,',','precision',  '%.16f')
%xlswrite('C:\Users\User\Dropbox\EmpiricalProductionNetwork\OctaveLocal\Second Iteration\t.xls', 'sheet1')
