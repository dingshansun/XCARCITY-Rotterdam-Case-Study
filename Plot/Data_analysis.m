clear
load('0521/2025-05-31-N200-before.mat')
Obj_before=Obj;
Dec_before=Dec;
load('0521/2025-05-31-N250-after.mat')
Obj_after=Obj;
Dec_after=Dec;
%% The min TTC of before intervention
% [~,min_TTC_before_index]=min(Obj_before(:,1));
% % min_TTC_before_index=74;
% solution=Dec_before(min_TTC_before_index,:);
% fprintf("The detailed flow and cost of before-intervention is: \n");
% output_before = ALSUN_Model_Single_before(solution);
% fprintf("The detailed flow and cost of after-intervention is: \n");
% output_after = ALSUN_Model_Single_after(solution);

%% The results of before-min-TTC and after-min-TTC
[~,min_TTC_before_index]=min(Obj_before(:,1));
[~,min_TTC_after_index]=min(Obj_after(:,1));
min_TTC_before_solution_B=Dec_before(min_TTC_before_index,:);
min_TTC_after_solution_A=Dec_after(min_TTC_after_index,:);
fprintf("The detailed flow and cost of solution B1 is: \n");
output_B = ALSUN_Model_Single_before_0521(min_TTC_before_solution_B);
fprintf("The detailed flow and cost of solution A1 on after-intervention is: \n");
output_A = ALSUN_Model_Single_after_0521(min_TTC_after_solution_A);
fprintf("The detailed flow and cost of solution A is: \n");
output_A = ALSUN_Model_Single_after(min_TTC_after_solution_A);
fprintf("Total cost is %d: \n", Obj_after(min_TTC_after_index,1));

%% Show the detailed flow and cost information

%% Show the relative shift of Scenario-Before optimial solutions
% num=200;
% Objective_before=nan(num,2);
% Objective_after=nan(num,3);
% 
% idx = randperm(num, num);
% % parpool(8)
% parfor i=1:num
%     % index=idx(i);
%     index=i;
%     decision=Dec_before(index,:);
%     Objective_before(i,:)=Obj_before(index,:);  % two dimension
%     Objective_after(i,:)=ALSUN_Model_Single_after_0521(decision); % three dimension
% end