function E = errorFunctionEDESHybrid(p0, pRest, namP,timespan,datGlu,datIns,x0,c,input,sim) % removed pDat

for ind= 1:length(p0)
pRest(namP{ind})= p0(ind);
end

ptemp=pRest;
global t_saved Gpl_saved
t_saved = 0;
Gpl_saved = sim.Gpl;

E = zeros(2*length(timespan),1);
%w_glu = ones(1,length(timespan)); % weights for glucose
%w_ins = ones(1,length(timespan)); % weights for insulin

ODE_model    = @diffeq_diabetes;
ODE_optionsG = odeset('RelTol',1e-5,'OutputFcn',@integratorfunG);
[~,xmodelG]   = ode15s(ODE_model, timespan, x0, ODE_optionsG,ptemp,c,input);

%for ind = 1:length(timespan)
%    E(ind) = (xmodelG(ind,2)-datGlu(ind));
%    E(ind+length(timespan)) = (xmodelG(ind,3)-datIns(ind))*0.1;   % weight insulin
%end

E = [xmodelG(:,2)-datGlu(:);
    (xmodelG(:,3)-datIns(:))*0.1];
