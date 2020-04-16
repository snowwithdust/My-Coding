import pulp as pul

def solve_ilp(objective , constraints) :
    #最小值pulp.LpMinimize最大值pulp.LpMaximize
    prob = pul.LpProblem('LP1' , pul.LpMinimize)
    prob += objective
    for cons in constraints :
        prob += cons
    print(prob)
    status = prob.solve()
    if status != 1 :
        return None
    else :
        return [v.varValue.real for v in prob.variables()]

   

V_NUM = 5
#变量，直接设置下限
variables = [pul.LpVariable('X%d'%i , lowBound = 0, upBound = 100000000,cat = pul.LpInteger) for i in range(0 , V_NUM)]
#目标函数
c = [446,596,822,1177,1562]
objective = sum([c[i]*variables[i] for i in range(0 , V_NUM)])
#约束条件
constraints = []

a1 = [114.3703,178.7035,257.3330,350.2589,457.4811]
constraints.append(sum([a1[i]*variables[i] for i in range(0 , V_NUM)])>=200000)

res = solve_ilp(objective , constraints)
print(res)

s = 0
for i in range(5):
        s += c[i]*res[i]
print("结果为",s)