import argparse
import pulp as p
import numpy as np
parser = argparse.ArgumentParser()

class Solve():
    def __init__(self, path, algo, policy):
        self.path = path
        mdp = self.get_mdp()
        # start = time.time()
        if policy != "none":
            V, pi = self.val_finder(mdp, policy)
        elif algo == "vi":
            V, pi = self.vi_solve(mdp)
        elif algo == "hpi":
            V, pi = self.hpi_solve(mdp)
        elif algo == "lp":
            V, pi = self.lp_solve(mdp)
        # end = time.time()
        # print("Elapsed time: ", end - start)
        self.output(V, pi)

    def get_mdp(self):
        mdp = dict()
        data = open(self.path).read().strip().split("\n")
        mdp["start"] = 0
        for line in data:
            flag, *content = line.split()
            if flag == "transition":
                s, a, s_next, r, p = map(eval, content)
                mdp["R"][s, a, s_next], mdp["T"][s, a, s_next] = r, p
            elif flag == "numStates":
                mdp["ns"] = int(content[-1])
            elif flag == "numActions":
                mdp["na"] = int(content[-1])
                mdp["T"] = np.zeros((mdp["ns"], mdp["na"], mdp["ns"]))
                mdp["R"] = np.zeros((mdp["ns"], mdp["na"], mdp["ns"]))
            elif flag == "end":
                mdp["end"] = list(map(int, content))
            elif flag == "mdptype":
                mdp["mdptype"] = content[-1]
            elif flag == "discount":
                mdp["gamma"] = float(content[-1])
        return mdp

    def vi_solve(self, mdp):
        V = np.zeros(mdp["ns"])
        V_old = V
        while (1):
            V = np.max(np.sum(mdp["T"] * (mdp["R"] + mdp["gamma"] * V_old), axis=-1), axis=-1)
            if np.allclose(V, V_old, rtol=0, atol=1e-11):
                break
            V_old = V
        policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["gamma"] * V), axis=-1), axis=-1)
        return V, policy

    def hpi_solve(self, mdp):
        pi = np.random.randint(low=0, high=mdp["na"], size=mdp["ns"])
        pi_old = pi
        while (1):
            T_pi = mdp["T"][np.arange(mdp["ns"]), pi_old]
            R_pi = mdp["R"][np.arange(mdp["ns"]), pi_old]
            V = np.squeeze(np.linalg.inv(np.eye(mdp["ns"]) - mdp["gamma"] * T_pi)
                           @ np.sum(T_pi * R_pi, axis=-1, keepdims=True))
            pi = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["gamma"] * V), axis=-1), axis=-1)
            if np.array_equal(pi, pi_old):
                break
            pi_old = pi
        return V, pi

    def lp_solve(self, mdp):
        prob = p.LpProblem('MDP', p.LpMinimize)
        V = np.array(list(p.LpVariable.dicts("V", [i for i in range(mdp["ns"])]).values()))
        prob += p.lpSum(V)  # Objective function
        # Constraints
        for s in range(mdp["ns"]):
            for a in range(mdp["na"]):
                prob += V[s] >= p.lpSum(mdp["T"][s, a] * (mdp["R"][s, a] + mdp["gamma"] * V))

        prob.solve(p.apis.PULP_CBC_CMD(msg=0))
        V = np.array(list(map(p.value, V)))
        policy = np.argmax(np.sum(mdp["T"] * (mdp["R"] + mdp["gamma"] * V), axis=-1), axis=-1)
        return V, policy

    def val_finder(self, mdp, policy):
        prob = p.LpProblem('MDP', p.LpMinimize)
        policy_fd = open(policy, "rt")
        action_lines = policy_fd.readlines()
        pi_opt = np.zeros((mdp["ns"]), dtype=int)
        i = 0
        for ac in action_lines:
            pi_opt[i] = int(ac.split()[0])
            i += 1

        V = np.array(list(p.LpVariable.dicts("V", [i for i in range(mdp["ns"])]).values()))
        prob += 1  # Objective function
        # Constraints
        for s in range(mdp["ns"]):
            ac = pi_opt[s]
            prob += V[s] == p.lpSum(mdp["T"][s, ac] * (mdp["R"][s, ac] + mdp["gamma"] * V))

        prob.solve(p.apis.PULP_CBC_CMD(msg=0))
        V = np.array(list(map(p.value, V)))
        return V, pi_opt

    def output(self, V, pi):
        V = list(map('{0:.6f}'.format, list(V)))
        pi = list(map(str, pi))
        output = ""
        for i in range(len(V)):
            output += V[i] + " " + pi[i] + "\n"
        print(output.strip())


if __name__ == "__main__":
    parser.add_argument("--mdp", type=str, default="./data/mdp/continuing-mdp-50-20.txt")
    parser.add_argument("--algorithm", type=str, default="vi")
    parser.add_argument("-pol", "--policy", type = str, default="none", help="input policy file (optional)")
    args = parser.parse_args()

    Solve(args.mdp, args.algorithm, args.policy)
    
    