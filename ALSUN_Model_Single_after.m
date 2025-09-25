function  output = ALSUN_Model_Single_after(decisions)
%ALSUN_MODEL 
% decision variables include car speed, 

gamma=10;
max_iter=2000;
% [multi,~]=size(decision_variable);
% TTC_all=nan(multi,1);
% car_flow=nan(multi,1);
% cost=nan(multi,1);
    % decisions=decision_variable(i,:);
    count=0;
    converge_count=0;
    [Aeq, beq, Money_cost, Time_cost, para, transfer_flow_matrix] = Setup_after(decisions);
    dimension=size(Aeq,2);  % the dimension of the optimization variable
    lb=zeros(dimension,1);  % the low bound of link flows
    epsilon_TTC=100  ;
    epsilon_x=0.1; 
    converge=false;
    X_link=10.*rand(dimension,1);
    % X=X_link;
    H=speye(dimension);
    model = struct();
    model.Q=0.5.*H;
    model.A=Aeq;
    model.rhs=beq;
    model.sense='=';
    model.lb=lb;
    model.modelsense='min';
    params = struct();
    params.outputflag=0;
    TTC=0;
    TTC_st=TTC;
    
    while ~converge
        % projection
        [total_cost,~]=Link_cost_func_bush(X_link, para, Time_cost, Money_cost, transfer_flow_matrix);
        Hf=gamma*(total_cost+0/(count+1)*X_link)-X_link;
        model.obj=Hf;
        % model.start=X_link;
        result=gurobi(model,params);
        X_link_bar=result.x;
        % disp(result.status);
        % adaption
        [total_cost,~]=Link_cost_func_bush(X_link_bar, para, Time_cost, Money_cost, transfer_flow_matrix);
        Hf_est=gamma*(total_cost+0/(count+1)*X_link_bar)-X_link;
        model.obj=Hf_est;
        % model.start=X_link_bar;
        result=gurobi(model,params);
        X_link_=result.x;        

        % disp(result.status);
        % convergence judgement
        Error_x=abs(X_link-X_link_);
        if all(Error_x<=epsilon_x)
            converge_count=converge_count+1;
        else
            converge_count=0;
        end
        [UE_cost,~]=Link_cost_func_bush(X_link_, para, Time_cost, Money_cost, transfer_flow_matrix);
        TTC_=X_link_'*UE_cost;
        Error_TTC=TTC_-TTC;
        % epsilon=X_link_*1e-3;
        % if all(Error<=epsilon)
        if converge_count>=10 && Error_TTC<=epsilon_TTC
            converge=true;
        end
        % save results
        % X=[X X_link];
        X_link=X_link_;
        TTC=TTC_;
        TTC_st=[TTC_st TTC];
        count=count+1;
        if count>=max_iter
            converge=true;
        end
    end
    [UE_cost, ~]=Link_cost_func_bush(X_link, para, Time_cost, Money_cost, transfer_flow_matrix);
    % Link_cost_details(X_link, para, Time_cost, Money_cost, transfer_flow_matrix, decisions);
    TTC_all=X_link'*UE_cost;
    car_flow=sum(X_link(1:1260));
    %
    % origin_num=para.OD_dimension.origin;
    % money_cost_unimode=Money_cost.money_cost_unimode;
    % money_cost_intermodes=Money_cost.money_cost_intermodes;    
    % % divide the x_link into four categories
    % link_dimension_unimode=size(money_cost_unimode,1);
    % link_dimension_intermode=size(money_cost_intermodes,1);
    % link_dimension_noOD_extended=(link_dimension_unimode+link_dimension_intermode)*origin_num;
    
    % X_link_noOD_extended=X_link(1:link_dimension_noOD_extended);
    % X_link_noOD=sum(reshape(X_link_noOD_extended,origin_num,[]),1)';
    % X_link_unimode_before=X_link_noOD(1:link_dimension_unimode);
    % X_link_intermode_before=X_link_noOD(link_dimension_unimode+1:link_dimension_unimode+link_dimension_intermode);
    % save("Plot_data/Link_flow_before.mat", "X_link_unimode_before", "X_link_intermode_before");

    % v_car=decisions(1);  % km/h; range is 20-60 km/h;
    % bus_freq=decisions(2); % range is 3-10
    % metro_freq=decisions(4); % veh/h range is 3-15
    % rail_freq=decisions(3);   % range is 2-10
    % c_fuel=decisions(5); % fuel cost per km; also including vehicle depreciation cost and road pricing strategy. It ranges from 0.2-0.5
    % c_park_low=decisions(6); % half parking fee for single trip; range from 0-5
    
    bus_freq=8;
    rail_freq=6;
    metro_freq=mean(decisions(6:8)); % we just take the avarage value to calculate

    metro_cost=200.*metro_freq+4000;
    rail_cost=300.*rail_freq+5000;
    bus_cost=50.*bus_freq+1000;
    cost_ope=metro_cost+rail_cost+bus_cost;
    
    cost=cost_ope;
    output = [TTC_all, car_flow, cost];
end

