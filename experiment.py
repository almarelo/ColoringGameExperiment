import argparse
import uuid
import matplotlib.pyplot as plt
import graph_utils as gu

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--num-colors', required=True, type=int, help='Number of initial Nodes')
parser.add_argument('-n', '--num-nodes',   required=True, type=int, help='Number of colors')
parser.add_argument('-p', '--probability', required=False, type=float, default=1.0, help='Randomness')
parser.add_argument('-r', '--report', required=False, default="./report.csv", help='CSV file to report')

args = parser.parse_args()

# input arguments

num_colors =  args.num_colors  #2
num_nodes  =  args.num_nodes   #24
# probability of changing color in the strategy, for the nodes than can improve their payoff
prob =        args.probability #1

# round counter
rounds = 0

# Nash equilibrium current status
ne = False

# Creating a random planar 3-tree with the given number of nodes, colors and probability
G, available_colors = gu.init(num_nodes, num_colors, prob)

# Difference between sizes of the color classes in the initial coloring
initDiff = gu.max_dif_color_classes(G, available_colors)

# Total payoff in the initial coloring
initPO =  gu.total_payoff(G)

# Executing while the coloring is not a Nash equilibrium
while ne is False:
    rounds +=1

    # Applying the strategy for each node with payoff = 0, changing its color with probability prob
    gu.improve(G, available_colors, prob)
    ne = gu.is_Nash_equilibrium(G, available_colors)

# Difference between sizes of the color classes in the final coloring    
finalDiff = gu.max_dif_color_classes(G, available_colors)

# Total payoff in the initial coloring
finalPO =  gu.total_payoff(G)

# Saving results in a csv table
csv = open(args.report, 'a+')
csv.write('{},{},{},{},{},{},{},{},{}\n'.format(uuid.uuid4(),
                                                num_nodes,
                                                num_colors,
                                                prob,
                                                rounds,
                                                initPO,
                                                finalPO,
                                                initDiff,
                                                finalDiff ))
csv.close()
print('POinit',initPO)
print('POfinal',finalPO )
print('MDinit',initDiff)
print('MDfinal', finalDiff)
print('num_rounds', rounds)

# Figure 2 shows the final graph, after the total number of rounds
plt.figure(2)
gu.draw_planar(G)
plt.show()
