 function [Eout] = DPMZ(Ein, VI, VQ, varargin)
% function [Eout] = DPMZ(Ein, VI, VQ, varargin)
% functional baseband description of dual-parallel Mach-Zenhder modulator
% based on sin wave model of MZ
%
% Ein is the electric field into to the DPMZ
% VI is the rf voltage applied to the 'real' modulator of the DPMZ
% (normalized to Vpi by default)
% VQ is the rf voltage applied to the 'imag' modulator of the DPMZ
% (normalized to Vpi by default)
%
%  [Eout] = DPMZ(Ein, VI, VQ,'autobias','min')
%       autobiasX,  autobiasY, or  autobiasOuter: 
%           'min': Vbias is ignored and set to acheived LARGEST loss
%           'max': Vbias is ignored and set to acheived LOWEST loss
%           '+3dB': Vbias is ignored and set to acheived positive slope at 3dB point
%           '-3dB': Vbias is ignored and set to acheived negative slope at 3dB point
%           'zero': biased is set to 0V
%  [Eout] = DPMZ(Ein, VI, VQ,'VpiOuter',4)
%       VpiOuter: override default Vpi of outer MZ to desired value
%  [Eout] = DPMZ(Ein, VI, VQ,'manualbiasouter',2)
%       manualbiasouter: override bias voltage to 2 vpi (in example)
%  [Eout] = DPMZ(Ein, VI, VQ,'rfouter',[-0.1 0 0.1...])
%       rfouter: add rf signal to outer bias point.
% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% Note:  To control biases manually, choose ['autobias', 'zero'] and apply%
% DC bias through VI or VQ or ['manualbiasouter', dcvoltage]              %
%ex: DPMZ(Ein, VI, VQ,'autobiasX','zero','autobiasY','zero','autobiasOuter', 'zero', 'rfouter', Vouter)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%                               -------
%                             /         \
%          --- Ein/sqrt(2) --     MZ      -----------------------------------
%        /                    \ _ _ _ _ /                                     \
%  Ein -                        -------                                         --
%        \                    /         \                                     /
%          --- Ein/sqrt(2) --     MZ      ----   exp(j*pi*Vouter/VpiOuter) --
%                             \_ _ _ _  / 
%
% written by Iannick Monfils
% Last edited July 22, 2008
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
VpiOuter = 1;
mode = 'min';                       %default to bias at Min point
Vouter = VpiOuter + VpiOuter/2;     %default bias to Quadrature point
ModType = 'push-pull';              %default to push-pull
autobiasI = 'zero';                  %default to bias at min
autobiasQ = 'zero';                  %default to bias at min
VrfOuter = 0;                       %default to no rf on outer MZ

for z = 1:2:length(varargin)
    switch varargin{z}
        case {'autobiasI'}
            autobiasI = varargin{z+1};
        case {'autobiasQ'}
            autobiasQ = varargin{z+1};
        case {'autobiasOuter'}
            switch varargin{z+1}
                case{'min'}
                    Vouter = VpiOuter;
                case{'max'}
                    Vouter = 2*VpiOuter;
                case{'+3dB'}
                    Vouter = VpiOuter + VpiOuter/2;
                case{'-3dB'}
                    Vouter = VpiOuter/2;
                case{'zero'}
                    Vouter = 0;
                otherwise
                    disp('Bias mode not recognized.  Outer MZ biased to +3dB as default');
                    Vouter = VpiOuter + VpiOuter/2;
            end
         case {'vpiouter'}  % set VPI
            VpiOuter = varargin{z+1};
         case {'manualbiasouter'}
            Vouter = varargin{z+1};
        case {'rfouter'}
            VrfOuter = varargin{z+1};
         otherwise
            disp([varargin{z} ' not recognized parameter: see help dpmz'])
    end
end

%% electric fields
% inner MZ
Eout_I = MZ(Ein/sqrt(2),VI,'modtype',ModType,'autobias',autobiasI);
Eout_Q = MZ(Ein/sqrt(2),VQ,'modtype',ModType,'autobias',autobiasQ); % ignoring pi/2 rotation since it will be rotated out when fields combine
%outer Mz
Eout = Eout_I/sqrt(2) + Eout_Q/sqrt(2).*exp(j*pi*(Vouter+VrfOuter)/VpiOuter);
