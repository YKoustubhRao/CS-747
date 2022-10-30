import random,argparse,sys,subprocess,os
import matplotlib.pyplot as plt
import numpy as np

x_axis = []
y_axis_opt = []
y_axis_rand = []

# for b in range(15):
#     x_axis.append(15-b)


# for b in range(15):
#     runs = 10
#     balls = 15 - b
#     state_gen = "python","cricket_states.py","--runs", runs, "--balls", balls
#     f = open('state_file','w')
#     subprocess.call(state_gen,stdout=f)
#     f.close()
#     encoder = "python", "encoder.py", "--states", "state_file", "--parameters", "./data/cricket/sample-p1.txt", "--q", "0.25"
#     m = open('mdpfile','w')
#     subprocess.call(encoder,stdout=m)
#     m.close()
#     gp = open("./data/cricket/rand_pol.txt", "r")
#     gp_lines = gp.readlines(0)
#     pg = open("pol", "w")
#     for b1 in range(balls):
#         for r1 in range(runs):

#     pg.close()
#     gp.close()
#     rand = "python", "planner.py", "--mdp", "mdpfile", "--policy", "pol"
#     planner = "python", "planner.py", "--mdp", "mdpfile"
#     v = open("value_and_policy_file",'w')
#     subprocess.call(planner,stdout=v)
#     v.close()
#     decoder = "python", "decoder.py", "--value-policy", "value_and_policy_file", "--states", "state_file"
#     v = open("policyfile",'w')
#     subprocess.call(decoder,stdout=v)
#     v.close()
#     v = open("policyfile",'r')
#     y_axis_opt.append(float(v.readline().split()[2]))
#     v.close()

for Q in range(100):
    q = (Q+1)/100
    x_axis.append(q)
    encoder = "python", "encoder.py", "--states", "state_file", "--parameters", "./data/cricket/sample-p1.txt", "--q", str(q)
    m = open('mdpfile','w')
    subprocess.call(encoder,stdout=m)
    m.close()
    rand = "python", "planner.py", "--mdp", "mdpfile", "--policy", "./data/cricket/rand_pol.txt"
    v = open("policyfile",'w')
    subprocess.call(rand)
    v.close()
    v = open("policyfile",'r')
    y_axis_rand.append(float(v.readline().split()[0]))
    v.close()
    planner = "python", "planner.py", "--mdp", "mdpfile"
    v = open("value_and_policy_file",'w')
    subprocess.call(planner,stdout=v)
    v.close()
    decoder = "python", "decoder.py", "--value-policy", "value_and_policy_file", "--states", "state_file"
    v = open("policyfile",'w')
    subprocess.call(decoder,stdout=v)
    v.close()
    v = open("policyfile",'r')
    y_axis_opt.append(float(v.readline().split()[2]))
    v.close()


plt.plot(np.array(x_axis), np.array(y_axis_opt), label="opt")
plt.plot(np.array(x_axis), np.array(y_axis_rand), label="rand")
plt.xlabel("Q")  # add X-axis label
plt.ylabel("Win Probability")  # add Y-axis label
plt.title("Graph 1")  # add title
plt.savefig('graph_1.png')