function [Eout]=DualMZ(Ein,VQ,VI,VO, Vpi, alpha)
%feeds RF signal and DC bias straight to function, i.e. VQ = Vrf_Q + Vbias_Q
%Same model as in paper except there is no alpha parameter (chirp variable)
%And the outer MZ has a perfect split ratio
Vpi_I=Vpi(1);%0.7;
Vpi_Q=Vpi(2);%1.4;
Vpi_O=Vpi(3);%1.1;

aI= alpha(1);
aQ= alpha(2);

splitratio_I=1.05;
splitratio_Q=0.9;
splitratio_O=0.9;

Ein_I=Ein/sqrt(2);
Ein_Q=Ein/sqrt(2);

%% Inside MZ

Eout_I = Ein_I.*sqrt(splitratio_I./(splitratio_I + 1))./sqrt(2).*exp(j*pi/2.*(-1*VI*(1-aI))./Vpi_I) + Ein_I.*sqrt(1./(splitratio_I + 1))./sqrt(2).*exp(j*pi/2.*(VI*(1+aI))./Vpi_I);

Eout_Q = Ein_Q.*sqrt(splitratio_Q./(splitratio_Q + 1))./sqrt(2).*exp(j*pi/2.*(-1*VQ*(1-aQ))./Vpi_Q) + Ein_Q.*sqrt(1./(splitratio_Q + 1))./sqrt(2).*exp(j*pi/2.*(VQ*(1+aQ))./Vpi_Q);

%%Outer Mz


Eout = exp(1i*pi/4)*(Eout_I/sqrt(2).*exp(j*pi/2*((-1*VO)/Vpi_O)) + Eout_Q/sqrt(2).*exp(j*pi/2*((VO)/Vpi_O)));
