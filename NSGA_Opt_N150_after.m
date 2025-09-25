clear
clc
% parpool('local')
addpath('/apps/generic/gurobi/11.0.1/linux64/matlab/')
u_lb= [0 0 0 0 0 1 1 1]; % the interval lower bound is 180s; otherwise no more improvement
u_ub=[10 10 10 10 10 15 15 15]; % the interval upper bound is 600s

% objFunction_1 = @(para) TTC_par(para);
% objFunction_2 = @(para) Car_flow_par(para);
% objFunction_3 = @(para) Operation_cost_par(para);
objFcn = {@entry_f1, @entry_f3};
% PRO = UserProblem('objFcn', objFunction, 'encoding', [1 1 1 1 1 1 1], 'lower', u_lb, 'upper', u_ub);

% [Dec,Obj,Con]=
for i=1:1
    [Dec,Obj,Con] = platemo('algorithm',@NSGAII, 'objFcn', objFcn, 'encoding', [1 1 1 1 1 2 2 2], ...
        'lower', u_lb, 'upper', u_ub,...
    'N', 150, 'maxFE', 15000, 'once',1,'save', 10, 'run', 0521);
end

save('2025-05-21-N150-after.mat')

function prepare_alsun_cache(X)
    global ALSUN_CACHE
    N = size(X, 1);
    ALSUN_CACHE = nan(N, 3);
    parfor i = 1:N
        ALSUN_CACHE(i, :) = ALSUN_Model_Single_after(X(i, :));
    end
end

function f = get_obj1(~)
    global ALSUN_CACHE
    f = ALSUN_CACHE(:, 1);
end

function f = get_obj2(~)
    global ALSUN_CACHE
    f = ALSUN_CACHE(:, 2);
end

function f = get_obj3(~)
    global ALSUN_CACHE
    f = ALSUN_CACHE(:, 3);
end

function f = entry_f1(X)
    prepare_alsun_cache(X);  
    f = get_obj1(X);
end

function f = entry_f2(X)
    f = get_obj2(X);
end

function f = entry_f3(X)
    f = get_obj3(X);
end

