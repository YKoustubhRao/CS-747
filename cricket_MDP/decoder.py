import argparse


parser = argparse.ArgumentParser()


parser.add_argument("-vp", "--value-policy", type = str,
                    help="input value-policy file")
parser.add_argument("-s", "--states", type = str,
                    help="input state file path")


args = parser.parse_args()
state_file_path = args.states
state_fd = open(state_file_path, "rt")
state_lines = state_fd.readlines()
value_policy_file = args.value_policy
value_policy_fd = open(value_policy_file, "rt")
value_policy_lines = value_policy_fd.readlines()
balls = int(state_lines[0])//100
runs =  int(state_lines[0])%100

##bbrr
actions = [0,1,2,4,6]

for b in range(balls):
    b_r = balls-b
    for r in range(runs):
        r_r = runs-r
        split = value_policy_lines[b*runs+r].split()
        if b_r < 10:
            print("0"+str(b_r*100+r_r), actions[int(split[1])], split[0])
        else:
            print(str(b_r*100+r_r), actions[int(split[1])], split[0])