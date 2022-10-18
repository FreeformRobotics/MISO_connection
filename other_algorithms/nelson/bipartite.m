function x=bipartite( weights)
% find a minimal-weight bipartite matching b/w 2 graphs given a measure of dissimilarity between nodes
%surf(weights) can be used to visualize potential surface for matching
[n,n2]=size(weights);
x0=zeros(n^2, 1);
c=reshape(weights',n^2, 1);
Aeq=zeros(n,n^2);
Aeq2=zeros(n,n^2);
for i=1:n
    Aeq(i,n*(i-1 )+1:n*i)=ones(1 ,n);
    for j=1:n
        Aeq2(i,i+n*(j-1))=1;
    end
end
Aeq=[Aeq;Aeq2];
beq=ones(2*n, 1);
% [temp1,temp2]=size(matchconstr);
% for i=1:temp1
% temp=zeros(1 ,n^2);
% j=matchconstr(i, 1);
% k=matchconstr(i,2);
% temp(n*(j-1 )+k)=1;
% Aeq=[ Aeq;temp];
% beq=[beq;1];
% end
options=optimset('Algorithm','dual-simplex','LargeScale','off');

[x,fval,exitflag,output] = linprog(c,[],[],Aeq,beq,zeros(n^2,1),ones(n^2,1),x0,options);
x=reshape(x,n,n);
x=x';