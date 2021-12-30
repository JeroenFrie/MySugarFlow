function [p,c]=load_pHealthy_c(data,Data,i)

%load_pHealthy_c - Reference parameters for healthy subject model
%
%[p,c]=load_pHealthy_c()
%
%Inputs:
% data: struct with information on insulin used. Use [] for a normal simulation
% of a healthy subject
%Outputs:
% p: parameters (vector)
% c: constants (struct)

% -- healthy parameter values from the best fitting model
p = [   1.35e-2  %k1
    6.33e-1  %k2
    5.00e-5  %k3
    1.00e-3  %k4
    3.80e-3  %k5
    5.82e-1  %k6
    2.20e-2  %k7
    4.71     %k8
    1.08e-2  %k9
    2.60     %k10
    1.35     %sigma /index 11
    0.63     %Km /index 12
    Data(i,1);      %Gb /index 13
    Data(i,6);];      %Iplb /index 14  
   
%%
% -- set constants
c        = struct();
c.f      = 0.005551;    %f [mmol/mg], must be equal to mgdL_to_mmolL /10 in load_data.m
c.vg     = 17/70;       %vg [L/kg]
c.gbliv  = 0.043;       %gbliv [mmol/L]
c.beta   = 1;           %beta [(mmol/L)/(microU/mL)]
c.taui   = 31;          %taui [min]
c.taud   = 3;           %taud [min]
c.vi     = 13/70;       %distribution volume of insulin per kg bodymass, vi [L/kg]
c.Gthpl  = 9;           %Gthpl [mmol/L]
c.t_integralwindow = 30;%Lower bound of moving time window of Gint
c.c1     = 0.1;         %c1 [1/min](previously k8)
c.c2     = c.gbliv.*(p(12)+p(13))/p(13) - p(5)*c.beta*p(14);          %c2 [mmol/L/min] = gbliv * (Km+Gb)/Gb - k5*beta*Ibpl; constant term in gnon-it
c.c3     = p(7).*p(13)/(c.beta*c.taui.*p(14)).*c.t_integralwindow;  %c3 [1/min] = k7 * Gb/(beta*tau_i*Ibpl).*t_integralwindow ; constant term in iliv

