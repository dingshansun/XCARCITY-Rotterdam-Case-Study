function [link_cost, Monetary_cost] = Link_cost_func_bush(X_link, para, Time_cost, Money_cost, transfer_flow_matrix)
% all the costs are categorized in four types: unimode, intermode, OriginMode, and DestiMode
% this version is suitable for a full OD matrix; for any arbitary OD pairs,
% we can just include all the pairs
origin_num=para.OD_dimension.origin;
desti_num=para.OD_dimension.desti;
time_weight=para.time_weight;
money_weight=para.money_weight;
mode_num=5;
Capacity_park=1500;

% prepared money cost, which are constants; [car; bus; bike; metro; rail]
money_cost_unimode=Money_cost.money_cost_unimode;
money_cost_intermodes=Money_cost.money_cost_intermodes;
money_OriginMode=Money_cost.money_OriginMode;
money_DestiMode=Money_cost.money_DestiMode;

% divide the x_link into four categories
link_dimension_unimode=size(money_cost_unimode,1);
link_dimension_intermode=size(money_cost_intermodes,1);
link_dimension_noOD_extended=(link_dimension_unimode+link_dimension_intermode)*origin_num;
link_dimension_Origin_extended=size(money_OriginMode,1);
link_dimension_Desti_extended=size(money_DestiMode,1)*(origin_num-1);

X_link_noOD_extended=X_link(1:link_dimension_noOD_extended);
X_link_Origin_extended=X_link(link_dimension_noOD_extended+1:link_dimension_noOD_extended+link_dimension_Origin_extended);
X_link_Desti_extended=X_link(end-link_dimension_Desti_extended+1:end);

% walking time cost, constants
walking_time_intermodes=Time_cost.WalkingTime.walking_time_intermodes; % Constant
walking_time_OriginMode=Time_cost.WalkingTime.walking_time_OriginMode; % Constant
walkingtime_DestiMode=Time_cost.WalkingTime.walkingtime_DestiMode;  % Constant

% In-vehicle time cost for unimode links
time0_cost_unimode=Time_cost.InVehicleTimeT0;  % BPR function: different parameters for various modes
alpha_unimode=Time_cost.Para.alpha_unimode;
beta_unimode=Time_cost.Para.beta_unimode;

% Parking time cost for intermode links and DestiMode links
parkfinding_time0_intermodes=Time_cost.parkfinding.parkfinding_time0_intermodes;  % BPR function
parkfinding_time0_DestiMode=Time_cost.parkfinding.parkfinding_time0_DestiMode; % BPR function
alpha_intermodes_parking=Time_cost.Para.alpha_intermodes_parking;   % the capacity C can also be specified
beta_intermodes_parking=Time_cost.Para.beta_intermodes_parking;

% Waiting time cost for intermode links and OriginMode links
waiting_time0_intermodes=Time_cost.waitingtime.waiting_time0_intermodes;  % Linear function: different parameters for various modes
waiting_time0_OriginMode=Time_cost.waitingtime.waiting_time0_OriginMode; % Linear function: as above
alpha_intermodes_waiting=Time_cost.Para.alpha_intermodes_waiting;
alpha_OriginMode_waiting=Time_cost.Para.alpha_OriginMode_waiting;
alpha_DestiMode_parking=Time_cost.Para.alpha_DestiMode_parking;
beta_DestiMode_parking=Time_cost.Para.beta_DestiMode_parking;

% sum up the link flows on the same link, generate the real link flow
X_link_noOD=sum(reshape(X_link_noOD_extended,origin_num,[]),1)';
X_link_Origin=X_link_Origin_extended;
X_link_Desti=sum(reshape(X_link_Desti_extended,(origin_num-1),[]),1)';
X_link_unimode=X_link_noOD(1:link_dimension_unimode);
X_link_intermode=X_link_noOD(link_dimension_unimode+1:link_dimension_unimode+link_dimension_intermode);

% calculate the link cost
% unimode links: money_cost_unimode(ready); time cost is the in-vehicle time
time_cost_unimode=time0_cost_unimode.*(1+alpha_unimode.*(X_link_unimode./2000).^beta_unimode);
% intermode links: money_cost_intermode is ready; time cost includes
% walking time (ready), waiting time, and parking time
waiting_time_intermodes=waiting_time0_intermodes+alpha_intermodes_waiting.*(transfer_flow_matrix*X_link_intermode);
% A hotfix to the parking flow; all the cars transfer at the same node should share the same parking capacity
data = X_link_intermode;
group_size = mode_num-1;
data_reshaped = reshape(data, group_size, []);
group_sums = sum(data_reshaped, 1);
group_sums(1:origin_num)=group_sums(1:origin_num)+reshape(X_link_Desti(1:mode_num:mode_num*origin_num), 1, []);
X_Desti_park=repelem(group_sums(1:origin_num)',5);
data_new = repmat(group_sums, group_size, 1);
data = data_new(:);

parkfinding_time_intermodes=parkfinding_time0_intermodes.*(1+alpha_intermodes_parking.*(data./Capacity_park).^beta_intermodes_parking);
time_cost_intermode=waiting_time_intermodes+parkfinding_time_intermodes+walking_time_intermodes;
% Origin links: money_OriginMode (ready); time cost includes walking time
% and waiting time
waiting_time_OriginMode=waiting_time0_OriginMode+alpha_OriginMode_waiting.*X_link_Origin;
time_cost_OriginMode=waiting_time_OriginMode+walking_time_OriginMode;
% Destination link: money_DestiMode (ready); time cost includes walking
% time and parking time
parkfinding_time_DestiMode=parkfinding_time0_DestiMode.*(1+alpha_DestiMode_parking.*(X_Desti_park./Capacity_park).^beta_DestiMode_parking);
time_cost_DestiMode=parkfinding_time_DestiMode+walkingtime_DestiMode;
% extend the costs to the OD-based link flow vector

Link_cost_unimode=money_weight.*money_cost_unimode+time_weight.*time_cost_unimode;
Link_cost_intermode=money_weight.*money_cost_intermodes+time_weight.*time_cost_intermode;
Link_cost_OriginMode=money_weight.*money_OriginMode+time_weight.*time_cost_OriginMode;
Link_cost_DestiMode=money_weight.*money_DestiMode+time_weight.*time_cost_DestiMode;

link_cost=[repelem([Link_cost_unimode;Link_cost_intermode],origin_num); Link_cost_OriginMode; repelem(Link_cost_DestiMode, origin_num-1)];
Monetary_cost=0;
end

