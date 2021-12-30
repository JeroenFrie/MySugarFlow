function [list_glu] = run_model_fun(mass,carb_weight,t_meal_start)

Data= readmatrix('Data_Glu_Ins_pre.csv'); %glucose= Data(i,1:5)'; insulin= Data(i,6:10)';
sim.Mg    = 0;    %Mg: glucose mass in gut [mg]
sim.Gint  = 0; 
%struct with info on meal
data.Dmeal{1,1} = carb_weight;   %D (total amount of carbohydrates ingested) [mg] 75g
data.t_meal_start = t_meal_start;   %starting time of the meal [min]
data.Mb = mass;             %bodymas vs [kg]
k=1;                    %index of the meal number
timespan = linspace(0,199,200);
ti= [0 15 30 60 120]';

p_values= zeros(size(Data,1),4);
residuals= zeros(size(Data,1),10);
sim_glu = zeros(size(Data,1),200);
sim_ins = zeros(size(Data,1),200);

a=1;
for i= 1:size(Data,1)
    glucose= Data(i,1:5)'; insulin= Data(i,6:10)';
    [p,c] = load_pHealthy_c([],Data,i); 
    sim.Gpl   = p(13);  %Gpl: basal plasma glucose concentration [mmol/L]
    sim.Ipl   = p(14);  %Ipl: basal plasma insulin concentration [mU/L]
    [x0,input] = load_x0_input(sim,data,k,timespan);
    x0(2)= glucose(1,1);  x0(3) = insulin(1,1);
    

    p0= [0.013511373352062 0.003806228136097 0.583886959936111 4.724211331206339]; % initial parameter values for optimization
    namP= {1,5,6,8}; % choice of parameters to estimate based on data
    lbP= p0*0.001; % lower bound of parameter set (contraining)
    hbP= p0*1000;  % upper bound of the parameter set (constraining)
    pRest= p; options=optimset('Algorithm','trust-region-reflective','MaxFunEvals',500,'TolX',1e-30);
    [resI.x, resI.resnorm, resI.residual,resI.exitflag, resI.output, resI.lambda,resI.jacobian] ...
    = lsqnonlin(@errorFunction, p0, lbP, hbP, options,pRest,namP,ti,glucose,insulin,x0,c,input,sim); % Optimization algorithm - ResI.x represents parameter values - ResI.residual represents the residual values
    residuals(a,:) = resI.residual';
    p_values(a,:)= resI.x';   
 
    for j = 1:length(p_values(i,:))    
    p(namP{j}) = p_values(i,j);
    end   

    global t_saved Gpl_saved
    t_saved = 0;
    Gpl_saved = Data(i,1)';
    
    ODE_model    = @diffeq_diabetes;
    ODE_optionsG = odeset('RelTol',1e-5,'OutputFcn',@integratorfunG);
    [sim.tGID,xmodelGID] = ode15s(ODE_model,timespan,x0,ODE_optionsG,p,c,input);
    sim_glu(a,:) = xmodelGID(:,2)';
    sim_ins(a,:) = xmodelGID(:,3)';
    
    a=a+1;

 
end
list_glu = sim_glu

end