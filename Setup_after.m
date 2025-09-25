function [Aeq, beq, Money_cost, Time_cost, para, transfer_flow_matrix] = Setup_after(decisions)
%SETUP 
OD=[0	348	171	780	189	534	797	151	37	109	63	444	438	72	25	85	423	101
260	0	952	1247	697	459	1380	331	60	202	156	483	452	216	100	88	328	409
207	821	0	754	2017	474	1796	552	84	281	500	419	525	846	691	126	309	617
417	843	682	0	1167	1188	3518	636	154	331	272	508	512	308	96	147	537	241
154	444	1349	1322	0	626	3397	722	103	305	395	238	258	556	109	104	284	176
529	394	545	2031	739	0	4759	835	252	694	326	633	652	509	71	282	1251	196
290	450	779	1878	1419	1715	0	1183	227	628	501	472	487	658	95	202	555	226
157	273	637	811	943	865	3330	0	351	2208	1765	259	349	1229	87	247	348	133
10	9	24	45	34	42	130	69	0	199	46	29	45	95	3	150	86	6
131	231	435	586	488	848	2227	2454	765	0	1152	224	281	1165	60	519	357	100
69	156	783	346	798	394	1399	1559	225	1034	0	146	167	2807	96	216	150	124
516	543	632	820	350	647	1333	304	120	239	146	0	0	0	0	0	0	0
366	380	558	543	301	473	972	277	151	190	137	0	0	0	0	0	0	0
60	134	747	364	659	440	1349	1116	268	1057	2195	0	0	0	0	0	0	0
0	9	78	10	13	4	16	6	0	6	11	0	0	0	0	0	0	0
179	150	300	362	196	516	902	568	750	853	381	0	0	0	0	0	0	0
672	468	501	1455	534	1903	2278	567	370	523	197	0	0	0	0	0	0	0
120	435	670	328	253	191	604	160	40	76	88	0	0	0	0	0	0	0];
% OD=zeros(18);
% OD(1,11)=1000;
% OD(2,10)=1000;
origin_num=size(OD,1);
desti_num=origin_num;
origin_index=1:origin_num;
desti_index=1:origin_num;
origin_set=arrayfun(@string, origin_index, 'UniformOutput', false);
desti_set=arrayfun(@string, desti_index, 'UniformOutput', false);
para.OD_dimension.origin=origin_num;
para.OD_dimension.desti=desti_num;

OD_pairs=cell(1,origin_num*desti_num);
% generate the OD pairs name, ready for link flow separation
k=1;
for i=1:origin_num
    for j=1:desti_num
        OD_pairs{k}=string(i)+"to"+string(j);
        k=k+1;
    end
end

% v_car=decisions(1);  % km/h; range is 20-60 km/h;
% bus_freq=decisions(2); % range is 3-10
metro_freq=decisions(6:8); % veh/h range is 3-15
% rail_freq=decisions(3);   % range is 2-10
% c_fuel=decisions(5); % fuel cost per km; also including vehicle depreciation cost and road pricing strategy. It ranges from 0.2-0.5
% c_park_low=decisions(6); % half parking fee for single trip; range from 0-5
% c_park_high=Para(7)/2; % range from 5-10
c_park_1=decisions(1);
c_park_4=decisions(2);
c_park_7=decisions(3);
c_park_9=decisions(4);
c_park_17=decisions(5);
c_park_low=4;

v_car=50;
bus_freq=8;
rail_freq=6;
c_fuel=0.3;


v.Car=v_car;
v.Bike=18; % km/h
v.Metro=36;
v.Bus=25;
v.Rail=60;

% c_fuel=0.22; % fuel cost per km; also including vehicle depreciation cost and road pricing strategy. It ranges from 0.2-0.5
% c_park_low=2; % half parking fee for single trip; range from 0-3
% c_park_high=5; % range from 5-10
c_park=zeros(origin_num,1);
for i=1:origin_num
    if i==1
        c_park(i)=c_park_1;
    elseif i==4
        c_park(i)=c_park_4;
    elseif i==7
        c_park(i)=c_park_7;
    elseif i==9
        c_park(i)=c_park_9;
    elseif i==17
        c_park(i)=c_park_17;
    else
        c_park(i)=c_park_low;
    end
end

bus_weight=4;

para.time_weight=25;
para.money_weight=1;


% money travel cost--in-vehicle
base.Bus=1.06; % euros
fare.Bus=0.18;
base.Bike=0;
fare.Bike=0;
base.Metro=1.06;
fare.Metro=0.18;
base.Rail=1.1;
fare.Rail=0.2;
base.Car=0;
fare.Car=c_fuel;

% frequency-waiting time
freq.Bus=bus_freq;
freq.Metro=metro_freq; % veh/h
% nodes 17,6,7 are for 1; nodes 13, 2, 1, 4 are for 2; nodes 3,5,8,10 are
% for 3;
freq.Metro = containers.Map('KeyType','double','ValueType','double');
freq.Metro(17) = metro_freq(1);
freq.Metro(6) = metro_freq(1);
freq.Metro(7) = metro_freq(1);
freq.Metro(1) = metro_freq(2);
freq.Metro(2) = metro_freq(2);
freq.Metro(4) = metro_freq(2);
freq.Metro(13) = metro_freq(2);
freq.Metro(3) = metro_freq(3);
freq.Metro(5) = metro_freq(3);
freq.Metro(8) = metro_freq(3);
freq.Metro(10) = metro_freq(3);

freq.Metro(9) = 0.1;
freq.Metro(11) = 0.1;
freq.Metro(12) = 0.1;
freq.Metro(14) = 0.1;
freq.Metro(15) = 0.1;
freq.Metro(16) = 0.1;
freq.Metro(18) = 0.1;

freq.Rail=rail_freq;
freq.Bike=10000; % the waiting time is negligible
freq.Car=10000;

alpha_waiting.Bus=0.0008;
alpha_waiting.Car=0;
alpha_waiting.Bike=0;
alpha_waiting.Metro=0.0005;
alpha_waiting.Rail=0.0003;

park_find_time=0.02;

% transfer time between modes: assume to be consistent across nodes
rowNames_intermode = ["Car", "Bus", "Bike", "Metro", "Rail"];
colNames_intermode = ["Car", "Bus", "Bike", "Metro", "Rail"];
data_intermode = [    0,    0.1,    1.0,    0.12,   0.12;  % from car to other modes
                                1.0,     0,      1.0,   0.06,    0.06;  % from bus to other modes
                                0.02,   0.02,   0,     0.02,   0.02;  % from bike to other modes
                                1.0,   0.06,   1.0,    0,      0.08;  % from metro to other modes
                                1.0,   0.06,   0.02,   0.08,   0];  % from rail to other modes
matrixTable_intermode = array2table(data_intermode, 'RowNames', rowNames_intermode, 'VariableNames', colNames_intermode);

% transfer time from origin/desti to modes
rowNames_ODMode = ["Origin", "Desti"];
colNames_ODMode = ["Car", "Bus", "Bike", "Metro", "Rail"];
data_ODMode = [0, 0.15, 0, 0.2, 0.25;
                             0.03, 0.06, 0, 0.09, 0.09];
matrixTable_ODmode = array2table(data_ODMode, 'RowNames', rowNames_ODMode, 'VariableNames', colNames_ODMode);

% Network layout and topology
% L_12=7.2; L_23=9.5; L_14=4.2; L_16=5.6;L_24=5.9; L_25=8.6; L_35=9.0; L_45=6.5; L_46=4.3; L_47=3.1;

% L_57=5.9; L_58=6.0; L_67=4.1; L_69=7.1; L_78=5.8; L_810=4.9; L_811=5.3; L_910=5.7; L_1011=8.7; L_710=8.4; L_34=12.9;
LLMatrix.Car = zeros(18); % Later, the matrix can be tailored for each mode
LLMatrix.Car(1,2)=7.2; LLMatrix.Car(1,12)=12.9; LLMatrix.Car(2,3)=9.5;LLMatrix.Car(1,4)=4.2;LLMatrix.Car(1,6)=5.6;
LLMatrix.Car(2,4)=5.9; LLMatrix.Car(2,5)=8.6;LLMatrix.Car(3,5)=9.0;LLMatrix.Car(4,5)=6.5;LLMatrix.Car(4,6)=4.3;LLMatrix.Car(4,7)=3.1;
LLMatrix.Car(5,7)=5.9;LLMatrix.Car(5,8)=6.0;LLMatrix.Car(6,7)=4.1;LLMatrix.Car(6,9)=7.1;LLMatrix.Car(7,8)=5.8;
LLMatrix.Car(8,10)=4.9;LLMatrix.Car(8,11)=5.3;LLMatrix.Car(9,10)=5.7;LLMatrix.Car(10,11)=8.7;LLMatrix.Car(7,10)=8.4;
LLMatrix.Car(3,4)=12.9;  LLMatrix.Car(12,13)=16.9;  LLMatrix.Car(3,15)=22.0;  LLMatrix.Car(2,18)=20.4;    
LLMatrix.Car(3,18)=21.3;LLMatrix.Car(15,18)=28.1;LLMatrix.Car(6,17)=6.7;LLMatrix.Car(9,16)=30.6;LLMatrix.Car(11,14)=25.2;
LLMatrix.Car(13,18)=18.0; LLMatrix.Car(12,18)=18.0;  LLMatrix.Car(12,17)=16.3; 
[row, col, val] = find(LLMatrix.Car);  % Get row, column indices, and values
% Copy values to symmetric coordinates
for k = 1:length(val)
    LLMatrix.Car(col(k), row(k)) = val(k);  % Copy A(i, j) to A(j, i)
end
LLMatrix.Car(LLMatrix.Car==0)=1000;  % the default distance is large

LLMatrix.Bike=LLMatrix.Car;
LLMatrix.Bus=LLMatrix.Car;

LLMatrix.Car(1,6)=1000;
LLMatrix.Car(6,1)=1000;
LLMatrix.Car(4,6)=1000;
LLMatrix.Car(6,4)=1000;
LLMatrix.Car(6,7)=1000;
LLMatrix.Car(7,6)=1000;
LLMatrix.Car(6,9)=1000;
LLMatrix.Car(9,6)=1000;
LLMatrix.Car(6,17)=1000;
LLMatrix.Car(17,6)=1000;

LLMatrix.Metro=zeros(18);
LLMatrix.Metro(1,4)=4.2;LLMatrix.Metro(2,4)=5.9;
LLMatrix.Metro(2,13)=21.2;  %% only for metro
LLMatrix.Metro(4,7)=3.1;LLMatrix.Metro(6,7)=4.1;LLMatrix.Metro(6,17)=6.7;LLMatrix.Metro(5,7)=5.9;
LLMatrix.Metro(3,5)=9.0;LLMatrix.Metro(7,8)=5.8;LLMatrix.Metro(8,10)=4.9;
[row, col, val] = find(LLMatrix.Metro);  % Get row, column indices, and values
% Copy values to symmetric coordinates
for k = 1:length(val)
    LLMatrix.Metro(col(k), row(k)) = val(k);  % Copy A(i, j) to A(j, i)
end
LLMatrix.Metro(LLMatrix.Metro==0)=1000;  % the default distance is large

LLMatrix.Rail=zeros(18);
LLMatrix.Rail(4,7)=3.1;
LLMatrix.Rail(7,17)=5.8;   %% only for rail
LLMatrix.Rail(7,8)=5.8;LLMatrix.Rail(8,11)=5.3;LLMatrix.Rail(11,14)=25.2;LLMatrix.Rail(3,4)=12.9;  %% only for rail
LLMatrix.Rail(3,15)=22.0;LLMatrix.Rail(15,18)=28.1;LLMatrix.Rail(12,17)=16.3;LLMatrix.Rail(12,13)=16.9;
LLMatrix.Rail(13,18)=18.0;
[row, col, val] = find(LLMatrix.Rail);  % Get row, column indices, and values
% Copy values to symmetric coordinates
for k = 1:length(val)
    LLMatrix.Rail(col(k), row(k)) = val(k);  % Copy A(i, j) to A(j, i)
end
LLMatrix.Rail(LLMatrix.Rail==0)=1000;  % the default distance is large

% use the neighbor nodes to generate connecting links
mode_name={"Car","Bus","Bike","Metro","Rail"};
mode_num=size(mode_name,2);

% neighbors of nodes from 1 to 18 of all the modes
node_neighbor_mode={[2 4 6 12],[1 3 4 5 13 18],[2 4 5 15 18],[1 2 3 5 6 7],[2 3 4 7 8],[1 4 7 9 17],[4 5 6 8 10 17],[5 7 10 11],[6 10 16],...
    [7 8 9 11],[8 10 14],[1 13 17 18],[2 12 18],11,[3 18],9,[6 7 12],[2 3 12 13 15]};

node_num_permode=origin_num;
nodes=cell(1, mode_num*node_num_permode); % the nodes of all the modes
conservation=cell(mode_num*node_num_permode*origin_num,1); % the conservation is for every node every OD pair
beq_modenodes=zeros(mode_num*node_num_permode*origin_num,1);
% the OD pairs with the same origin and destination nodes are excluded
k=1;
for i=1:mode_num
    mode=mode_name{i};
    for j=1:node_num_permode
        nodes{k}=mode+"_"+string(j); % all the node names
        k=k+1;
    end
end

% conservation of the OD-link flows within one mode; and the transfer links
k=1;n=1;
for i=1:mode_num
    mode=mode_name{i};
    transfer_mode=mode_name; % this variable should be specified for each node/mode for a regular case
    transfer_mode(i)=[];
    for j=1:node_num_permode
        node=nodes{n};
        for m=1:numel(origin_index)  % divide link flow based on origins: x_12_o1,x_12_o2, ...
            % parts = split(OD_pairs{m}, "to");
            origin=origin_index(m); 
            % desti=parts(2); 
            conservation{k}=node+"_Origin"+origin_set{m}+": ";
            for l=1:numel(node_neighbor_mode{j})  % add the mode links
                conservation{k}=conservation{k}+"+x_"+mode+"_"+string(node_neighbor_mode{j}(l))+"to"+string(j)+"_Origin"+origin_set{m}; % inflow
                conservation{k}=conservation{k}+"-x_"+mode+"_"+string(j)+"to"+string(node_neighbor_mode{j}(l))+"_Origin"+origin_set{m}; % outflow
            end
            for p=1:numel(transfer_mode)  % assume all the mode are connected; add transfer links
                conservation{k}=conservation{k}+"-x_"+mode+"to"+transfer_mode{p}+"_"+string(j)+"_Origin"+origin_set{m}; 
                conservation{k}=conservation{k}+"+x_"+transfer_mode{p}+"to"+mode+"_"+string(j)+"_Origin"+origin_set{m}; 
            end
            % add the origin flow if this is the origin node
            node_number=string(regexp(node, '\d+', 'match'));
            if m==j % if the origin matches its own flow
                conservation{k}=conservation{k}+"+x_O"+origin+"to"+node+"_Origin"+origin_set{m}; 
            else
                conservation{k}=conservation{k}+"-x_"+node+"toD"+string(j)+"_Origin"+origin_set{m}; 
            end
            k=k+1;
        end
        n=n+1;
    end
end

% conservation for the origin and destination nodes
conservation_origin=cell(origin_num,1);
beq_originnodes=zeros(origin_num,1);
k=1;
for i=1:origin_num   % for each origin node, only its own flow link exists
    origin=origin_index(i); 
    conservation_origin{k}="Origin_"+origin+": ";
    for m=1:mode_num
        mode=mode_name{m};
        conservation_origin{k}=conservation_origin{k}+"+x_O"+origin+"to"+mode+"_"+origin+"_Origin"+origin_set{i}; 
    end
    beq_originnodes(k)=sum(OD(i,:));  % sum all the flow originated from origin i
    k=k+1;
end

conservation_desti=cell(desti_num*(origin_num-1),1);
beq_destinodes=zeros(desti_num*(origin_num-1),1);
k=1;
for i=1:desti_num   % for each node formulate the conservation
    for j=1:origin_num  % all the origins may end at this destination
        origin=j; desti=i; 
        if origin~=desti% select the cooresponding OD pairs of the origin node: OD with the same O, 
            conservation_desti{k}="Desti_"+desti+"_Origin"+origin+": ";
            for m=1:mode_num
                mode=mode_name{m};
                conservation_desti{k}=conservation_desti{k}+"+x_"+mode+"_"+desti+"toD"+desti+"_Origin"+origin; 
            end
            beq_destinodes(k)=OD(origin,desti);
            k=k+1;
        else
            continue
        end
    end
end

conservation_all=[conservation; conservation_origin; conservation_desti];
beq=[beq_modenodes;beq_originnodes;beq_destinodes];

%% Generate the flow vector and model their cost
% First, the link within one mode
% Total number of links in one mode
elementCounts = cellfun(@numel, node_neighbor_mode);
link_number_unimode=sum(elementCounts);
x_link_unimode=cell(link_number_unimode*mode_num*origin_num,1);
time0_cost_unimode=zeros(link_number_unimode*mode_num,1);   % regardless of OD-flow
money_cost_unimode=zeros(link_number_unimode*mode_num,1);
alpha_unimode=zeros(link_number_unimode*mode_num,1);
beta_unimode=zeros(link_number_unimode*mode_num,1);
k=1;n=1;p=1;
for i=1:mode_num
    mode=mode_name{i};
    for j=1:node_num_permode
        node=nodes{n};
        for l=1:numel(node_neighbor_mode{j})  % add the mode links
            neigh=node_neighbor_mode{j}(l);
            time0_cost_unimode(p)=LLMatrix.(char(mode))(j,neigh)/v.(char(mode));  % unit: hour
            money_cost_unimode(p)=LLMatrix.(char(mode))(j,neigh)*fare.(char(mode));   
            if mode=="Car"
                alpha_unimode(p)=0.5;
                beta_unimode(p)=4;
            end
            p=p+1;
            for m=1:origin_num
                x_link_unimode{k}="x_"+node+"to"+string(node_neighbor_mode{j}(l))+"_Origin"+m;
                k=k+1;
            end
        end
        n=n+1;
    end
end

% Second, transfer links between modes; assume they are fully connected
k=1;
x_link_intermodes=cell(mode_num*node_num_permode*(mode_num-1)*origin_num,1);
walking_time_intermodes=zeros(mode_num*node_num_permode*(mode_num-1),1);
waiting_time0_intermodes=zeros(mode_num*node_num_permode*(mode_num-1),1);
parkfinding_time0_intermodes=zeros(mode_num*node_num_permode*(mode_num-1),1);
alpha_intermodes_parking=zeros(mode_num*node_num_permode*(mode_num-1),1);
alpha_intermodes_waiting=zeros(mode_num*node_num_permode*(mode_num-1),1);
beta_intermodes_parking=zeros(mode_num*node_num_permode*(mode_num-1),1);
money_cost_intermodes=zeros(mode_num*node_num_permode*(mode_num-1),1);
transfer_flow_matrix=zeros(mode_num*node_num_permode*(mode_num-1));
transfer_mode_num=strings(mode_num*node_num_permode*(mode_num-1),1);
transfer_node_num=zeros(mode_num*node_num_permode*(mode_num-1),1);
l=1;
for i=1:mode_num
    mode=mode_name{i};
    transfer_mode=mode_name; % this variable should be specified for each node/mode for a regular case
    transfer_mode(i)=[];  % exclude the mode per se
    for j=1:node_num_permode
        for p=1:numel(transfer_mode)  % assume all the mode are connected; add transfer links
            walking_time_intermodes(l)=matrixTable_intermode{mode,transfer_mode{p}}; % from mode to transfer_model{p}
            % judge the mode
            if ismember(transfer_mode{p}, ["Bike","Car","Bus","Rail"])
                freq_val = freq.(char(transfer_mode{p}));  
            else
                node_id = j;     
                freq_val = freq.(char(transfer_mode{p}))(node_id);  % Read from the map
            end
            waiting_time0_intermodes(l) = 0.5 * 1 / freq_val;
            % waiting_time0_intermodes(l)=0.5*1/freq.(char(transfer_mode{p}));  % waiting time for public transit, depend on flow

            money_cost_intermodes(l)=base.(char(transfer_mode{p}));  % base fare
            alpha_intermodes_waiting(l)=alpha_waiting.(char(transfer_mode{p}));
            if mode=="Car"
                money_cost_intermodes(l)=money_cost_intermodes(l)+c_park(j)*8;  % parking fee for leaving car mode
                parkfinding_time0_intermodes(l)=park_find_time;             % park finding time for leaving car mode
                alpha_intermodes_parking(l)=2.5;
                beta_intermodes_parking(l)=2;
            elseif mode=="Bike"
                money_cost_intermodes(l)=money_cost_intermodes(l)+0; % extra fee if taking a bike to train; unable to model the day ticket
            end
            transfer_mode_num(l)=transfer_mode{p}; % store all the transfer destination mode of the current link flow
            transfer_node_num(l)=j; % store all the transfer destination node of the current link flow
            l=l+1;
            for m=1:origin_num
                % origin=m; 
                x_link_intermodes{k}="x_"+mode+"to"+transfer_mode{p}+"_"+string(j)+"_Origin"+m;
                k=k+1;
            end
        end
    end
end
% Generate the transfer_flow_matrix
l=1;
for i=1:mode_num
    mode=mode_name{i};
    transfer_mode=mode_name; % this variable should be specified for each node/mode for a regular case
    transfer_mode(i)=[];  % exclude the mode per se
    for j=1:node_num_permode
        for p=1:numel(transfer_mode)
            sameNode = (j == transfer_node_num);  % the current transfer destination node is j
            sameTransfer = strcmp(transfer_mode{p}, transfer_mode_num); % the current transfer destination mode is p
            transfer_flow_matrix(l,:) = sameNode & sameTransfer;  % the matrix only considers the total link flow
            l=l+1;
        end
    end
end

% Third, transfer links between origin/destinations and nodes
x_link_origins=cell(origin_num*mode_num,1);
waiting_time0_OriginMode=zeros(origin_num*mode_num,1);
alpha_OriginMode_waiting=zeros(origin_num*mode_num,1);
walking_time_OriginMode=zeros(origin_num*mode_num,1);
money_OriginMode=zeros(origin_num*mode_num,1);
k=1;l=1;
for i=1:origin_num   % for each origin node
    for j=1:mode_num
        mode=mode_name{j};
        money_OriginMode(l)=base.(char(mode));  % base fare
        walking_time_OriginMode(l)=matrixTable_ODmode{"Origin",mode};
        alpha_OriginMode_waiting(l)=alpha_waiting.(char(mode));
        % waiting_time0_OriginMode(l)=0.5*1/freq.(char(mode));
        if ismember(mode, ["Bike","Car","Bus","Rail"])
            freq_val = freq.(char(mode));  
        else
            node_id = i;     
            freq_val = freq.(char(mode))(node_id);  % Read from the map
        end
        waiting_time0_OriginMode(l) = 0.5 * 1 / freq_val;
        l=l+1;
        % the total number of origin flows is: mode_number*origin_number
        x_link_origins{k}="x_O"+i+"to"+mode+"_"+i+"_Origin"+i;
        k=k+1;
    end
end

x_link_desti=cell(desti_num*(origin_num-1)*mode_num,1);
walkingtime_DestiMode=zeros(desti_num*mode_num,1);
parkfinding_time0_DestiMode=zeros(desti_num*mode_num,1);
alpha_DestiMode_parking=zeros(desti_num*mode_num,1);
beta_DestiMode_parking=zeros(desti_num*mode_num,1);
money_DestiMode=zeros(desti_num*mode_num,1);
k=1;l=1;
for i=1:desti_num   % for each origin node
    for j=1:mode_num
        mode=mode_name{j};
        walkingtime_DestiMode(l)=matrixTable_ODmode{"Desti",mode};
        money_DestiMode(l)=0;
        if mode=="Car"
            money_DestiMode(l)=money_DestiMode(l)+c_park(i)*8;  % parking fee for leaving car mode
            parkfinding_time0_DestiMode(l)=park_find_time;             % park finding time for leaving car mode
            alpha_DestiMode_parking(l)=2.5;
            beta_DestiMode_parking(l)=2;
        end
        l=l+1;
        for m=1:origin_num
            origin=m; desti=i; 
            if origin~=desti  % skip the OD with the same number
                x_link_desti{k}="x_"+mode+"_"+desti+"toD"+desti+"_Origin"+m;
                k=k+1;
            else
                continue
            end
        end
    end
end

Money_cost.money_cost_unimode=money_cost_unimode;
Money_cost.money_cost_intermodes=money_cost_intermodes;
Money_cost.money_OriginMode=money_OriginMode;
Money_cost.money_DestiMode=money_DestiMode;

Time_cost.InVehicleTimeT0=time0_cost_unimode;  % BPR function: different parameters for various modes
Time_cost.Para.alpha_unimode=alpha_unimode;
Time_cost.Para.beta_unimode=beta_unimode;

Time_cost.WalkingTime.walking_time_intermodes=walking_time_intermodes; % Constant
Time_cost.WalkingTime.walking_time_OriginMode=walking_time_OriginMode; % Constant
Time_cost.WalkingTime.walkingtime_DestiMode=walkingtime_DestiMode;  % Constant

Time_cost.parkfinding.parkfinding_time0_intermodes=parkfinding_time0_intermodes;  % BPR function
Time_cost.parkfinding.parkfinding_time0_DestiMode=parkfinding_time0_DestiMode; % BPR function
Time_cost.Para.alpha_intermodes_parking=alpha_intermodes_parking;   % the capacity C can also be specified
Time_cost.Para.beta_intermodes_parking=beta_intermodes_parking;

Time_cost.waitingtime.waiting_time0_intermodes=waiting_time0_intermodes;  % Linear function: different parameters for various modes
Time_cost.waitingtime.waiting_time0_OriginMode=waiting_time0_OriginMode; % Linear function: as above
Time_cost.Para.alpha_intermodes_waiting=alpha_intermodes_waiting;
Time_cost.Para.alpha_OriginMode_waiting=alpha_OriginMode_waiting;
Time_cost.Para.alpha_DestiMode_parking=alpha_DestiMode_parking;
Time_cost.Para.beta_DestiMode_parking=beta_DestiMode_parking;

x_link_string=[x_link_unimode;x_link_intermodes;x_link_origins;x_link_desti];
x_link = cellfun(@char, x_link_string, 'UniformOutput', false);

numRows = numel(conservation_all);
plusResults = {};  % To store substrings starting with "+"
minusResults = {}; % To store substrings starting with "-"

% Process each string row
for i = 1:numRows
    % Match substrings starting with "+" and "-"
    plusTokens = regexp(conservation_all{i}, "\+x\w*", 'match');
    minusTokens = regexp(conservation_all{i}, "\-x\w*", 'match');
    
    % Clean up "+" and "-" prefixes
    plusTokens = cellstr(strrep(plusTokens, "+", ""));
    minusTokens = cellstr(strrep(minusTokens, "-", ""));
    
    % Add tokens to results
    plusResults{i} = plusTokens;
    minusResults{i} = minusTokens;
end

% Determine the maximum number of "+" and "-" tokens for matrix size
maxPlusCols = max(cellfun(@numel, plusResults));
maxMinusCols = max(cellfun(@numel, minusResults));

% Create cell matrices, padding with empty strings where needed
plusMatrix = cell(numRows, maxPlusCols);
minusMatrix = cell(numRows, maxMinusCols);

% Fill the matrices
for i = 1:numRows
    plusMatrix(i, 1:numel(plusResults{i})) = plusResults{i};
    minusMatrix(i, 1:numel(minusResults{i})) = minusResults{i};
end

% Preallocate arrays for efficient sparse assignment
rowIndicesLocal = cell(numRows, 1);
colIndicesLocal = cell(numRows, 1);
valuesLocal = cell(numRows, 1);
xLinkMap = containers.Map(x_link, 1:numel(x_link));
% Parallel loop
for i = 1:numRows
    % Extract current row of plusMatrix and minusMatrix
    plusStrings = plusMatrix(i, :);
    minusStrings = minusMatrix(i, :);

    % Remove empty strings
    plusStrings = plusStrings(~cellfun('isempty', plusStrings));
    minusStrings = minusStrings(~cellfun('isempty', minusStrings));

    % Find indices in X for plus and minus strings
    % [~, plusIndices] = ismember(plusStrings, x_link);
    % [~, minusIndices] = ismember(minusStrings, x_link);

    plusIndices = cell2mat(cellfun(@(x) xLinkMap(x), plusStrings, 'UniformOutput', false));
    minusIndices = cell2mat(cellfun(@(x) xLinkMap(x), minusStrings, 'UniformOutput', false));

    % Collect row, column, and value information for sparse matrix
    numPlus = numel(plusIndices);
    numMinus = numel(minusIndices);

    % Store local results for the current row
    rowIndicesLocal{i} = [repmat(i, numPlus, 1); repmat(i, numMinus, 1)];
    colIndicesLocal{i} = [plusIndices'; minusIndices'];
    valuesLocal{i} = [ones(numPlus, 1); -ones(numMinus, 1)];
end

% After the loop, concatenate results from all workers
rowIndices = vertcat(rowIndicesLocal{:});
colIndices = vertcat(colIndicesLocal{:});
values = vertcat(valuesLocal{:});

% Construct the sparse matrix in one operation
Aeq = sparse(rowIndices, colIndices, values, numRows, numel(x_link));


end

