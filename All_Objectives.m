function obj = All_Objectives(x)
    [TTC, flow, cost] = ALSUN_Model(x);
    obj = [TTC, flow, cost];   % 注意方向（minimization）
end

