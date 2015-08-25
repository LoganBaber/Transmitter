function [Eout] = MZ(Ein, Vrf, varargin)
%function [Eout] = MZ(Ein,Vrf)
% Sin function model of a Mach-Zehnder modulator
%           Ignores absorption in material
%
%  [Eout] = MZ(Ein,Vrf)
%      Ein is the input electric field
%      Vrf is the rf voltage applied modulator normilized to Vpi
%      DEFAULT is Push-Pull biased at Minimum
%
%  [Eout] = MZ(Ein,Vrf,'autobias','min')
%       autobias: 
%           'min': Vbias is ignored and set to acheived LARGEST loss
%           'max': Vbias is ignored and set to acheived LOWEST loss
%           '+3dB': Vbias is ignored and set to acheived positive slope at 3dB point
%           '-3dB': Vbias is ignored and set to acheived negative slope at 3dB point
%           'zero': biased is set to 0V
%  [Eout] = MZ(Ein,Vrf,'vpi',4,)
%       vpi: override default Vpi to desired value
%  [Eout] = MZ(Ein,Vrf,'manualbias','2',)
%       manualbias: override bias voltage to 2 vpi (in example)
%  [Eout] = MZ(Ein,Vrf,'modtype','push-pull',)
%        'push-pull': V+ is applied to arm1 while V- is applied to arm2
%        'single':  only one arm is driven
%        'push-push': V+ is applied to both arms
%        default is Push-Pull
%  [Eout] = MZ(Ein,Vrf,'splitratio',2)
%        'splitratio': power in top branch/power in bottom branch (default
%        is 50,50 splitter (splitratio = 1)
%  [Eout] = MZ(Ein,Vrf,'er',30)
%        'er': extinction ratio in dB valid from 100 dB to 16 dB
%
%          --- Ein*sqrt(splitratio/(splitratio + 1)) --- phase shift: exp(-jVotal/Vpi) -----
%        /                                                                                   \
%  Ein -                                                                                       --
%        \                                                                                   /
%          --- Ein*sqrt(1/(splitratio + 1))*exp(j*pi/2) --- phase shift: exp(+jVotal/Vpi) --
%
% written by Iannick Monfils
% Last edited July 22 2008
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Vpi = 1;                    %default for Votal signals to be normalized to Vpi
mode = 'min';               %default to bias at Min point
Vbias = 0;                  %default bias to Vpi
ModType = 'push-pull';      %default to push-pull
splitratio = 1;             %power in top branch/power in bottom branch

for z = 1:2:length(varargin)
    switch varargin{z}
        case {'autobias'}
            switch varargin{z+1}
                case{'min'}
                    Vbias = Vpi;
                case{'max'}
                    Vbias = 2*Vpi;
                case{'+3dB'}
                    Vbias = Vpi + Vpi/2;
                case{'-3dB'}
                    Vbias = Vpi/2;
                case{'zero'}
                    Vbias = 0;
                otherwise
                    disp('Bias mode not recognized.  Biased to +3dB in Push-pull mode as default');
                    Vbias = Vpi + Vpi/2;
            end
        case {'vpi'}                            % set VPI
            Vpi = varargin{z+1};
        case {'manualbias'}
            Vbias = varargin{z+1};
        case {'modtype'}
            switch varargin{z+1}
                case{'push-pull'}
                    ModType = 'push-pull';     %default to push-pull
                case{'single'}
                    ModType = 'single';     
                case{'push-push'}
                    ModType = 'push-push';    
                otherwise
                    disp('Modulator type is not recongnized: Defaulting to push-pull')
                    ModType = 'push-pull';     %default to push-pull
            end
        case {'splitratio'}
            splitratio = varargin{z+1};
        case {'er'}
            desiredER = varargin{z+1};
            [out] = open('ERvsSR MZ.mat');    %% ER ratio versus split ratio data
            splitratio = interp1(out.er,out.splitratio,desiredER);  % interpelate the spliting ratio from the desired ER (dB)
        otherwise
            disp([varargin{z} ' not recognized parameter: see help mz'])
    end
end

Vtotal = Vrf+Vbias;  %% total voltage applied (RF + bias)

switch ModType
    case{'push-pull'}
        Eout = Ein.*sqrt(splitratio./(splitratio + 1))./sqrt(2).*exp(j*pi/2.*(-1*Vtotal)./Vpi) + Ein.*sqrt(1./(splitratio + 1))./sqrt(2).*exp(j*pi/2.*Vtotal./Vpi);
        %Eout = Ein.*(sin(-pi*Vrf./(2*Vpi)))
    case{'single'}
        Eout = Ein.*sqrt(splitratio./(splitratio + 1))/sqrt(2) + Ein.*sqrt(1/(splitratio + 1))./sqrt(2)*exp(j*pi.*Vtotal./Vpi);
    case{'push-push'}
        Eout = Ein.*sqrt(splitratio./(splitratio + 1))/sqrt(2)*exp(j*pi/2.*Vtotal./Vpi) + Ein.*sqrt(1/(splitratio + 1))./sqrt(2)*exp(j*pi/2.*Vtotal./Vpi);
end
