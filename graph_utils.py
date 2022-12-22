import random
import networkx as nx
import matplotlib.pyplot as plt

TOTAL_COLORS = ('blue', 'red', 'yellow', 'green', 'orange', 'purple', 'brown', 'pink', 'cyan', 'magenta')
OPTIONS = {"edgecolors": "tab:gray", "alpha": 0.9, "font_size": 10
           #, "font_color":"whitesmoke"
}

def frozen2list(s):
    ans = []
    for i in s:
        sub = []
        for j in i:
            sub.append(j)
        ans.append(sub)
    return ans

def get_faces(P):
    faces = set()
    for start,end in P.edges():
        #print(start, end)
        faces.add(frozenset(P.traverse_face(start, end)))
    return faces

def random_face(G):
    O, P = nx.check_planarity(G)
    F = get_faces(P)
    faces = frozen2list(F)
    R = random.choice(faces)
    return R

def add_node_in_cycle(G):
    R= random_face(G)
    num_nodes= len(G.nodes)
    for i in R:
        G.add_edge(i,num_nodes, width=2.0, alpha=0.5)
    return

    
def random_coloring(G, available_colors):
     for index in G.nodes:
         G.nodes[index]["color"] = random.choice(available_colors)
     return


def planar_3tree(k):
    if k<3:
        print("A planar 3-tree requires at least 3 vertices")
    G = nx.complete_graph(3)
    for i in range (k-3):
        add_node_in_cycle(G)
    return G

def draw_planar(G):
    colors = []
    print(G.nodes)
    for index in G.nodes():
        node = G.nodes[index]
        # G.nodes[index]["color"] = "blue"
        color = node.get('color')
        if color is None:
            colors.append('gray')
        else:
            colors.append(color)
    pos=nx.planar_layout(G)
    nx.draw(G, pos=pos, with_labels=True, node_color = colors, **OPTIONS)
    return

def assign_payoff_proper(node, G):
    payoff = 1
    ne = G.neighbors(node)
    for nei in ne:
        if G.nodes[node]['color'] == G.nodes[nei]['color']:
            payoff = 0
            break
    G.nodes[node]['payoff'] = payoff

def assign_payoff_faces(node, G):
    O, P = nx.check_planarity(G)
    payoff = 1
    ne = G.neighbors(node)
    for nei in ne:
        for i in P.traverse_face(node, nei):
            if i != node and G.nodes[node]['color'] == G.nodes[i]['color']:
                payoff = 0
                break
        
    G.nodes[node]['payoff'] = payoff

def assign_payoff_mono(node, G):
    O, P = nx.check_planarity(G)
    payoff = 1
    ne = G.neighbors(node)
    for nei in ne:
        count = 1
        face = P.traverse_face(node, nei)
        for i in face:            
            if i != node and G.nodes[node]['color'] == G.nodes[i]['color']:
                count+=1
        
        if count == len(face):
            payoff = 0
            break
    
    G.nodes[node]['payoff'] = payoff
 
def assign_payoff_poly(node, G, colors):
    O, P = nx.check_planarity(G)
    payoff = 1
    ne = G.neighbors(node)
    sc = set(colors)
    for nei in ne:
        face = P.traverse_face(node, nei)
        cc=set()
        for i in face:
            cc.add(G.nodes[i]['color'])
                    
        if cc != sc:
            payoff = 0
            break
    return  payoff

def payoff_poly_can_improve(node, G, colors):
    
    if  G.nodes[node]['payoff']==1:
        return (False, None)
    else:

         O, P = nx.check_planarity(G)
         ne = G.neighbors(node)
         sc = set(colors)
         new = set()
 
         for nei in ne:
             face = P.traverse_face(node, nei)
             cc=set()
             for i in face:
                  if i != node:
                      cc.add(G.nodes[i]['color'])
             A = sc - cc         
             if len(A) > 1:
                 print('A', A)
                 return  (False, None)
             else:
                 
                 new = new | A
         if len(new) != 1:
              print('new', new)
              return  (False, None)
         else:
              new = new.pop()
              print(node, "can improve", new)
              return (True, new)

def random_strategy_poly(node, G, colors, prob):
    color = G.nodes[node]['color']
    can_improve, new_c = payoff_poly_can_improve(node, G, colors)
    p = random.uniform(0,1)
    if can_improve and p < prob:
        color = new_c
    #print(p)    
    return  can_improve,  color

def apply_strategies(G, colors, prob):
    for node in G.nodes():
        G.nodes[node]['improve'], G.nodes[node]['color'] = random_strategy_poly(node, G, colors, prob)
    return
 
def is_Nash_equilibrium(G, colors):
    for node in G.nodes():
        if payoff_poly_can_improve(node, G, colors)[0]:
            return False
    print('this coloring is a Nash-equilibrium for polychromatic-game')
    return True

def total_payoff(G):
    sum = 0
    for node in G.nodes():
        sum += G.nodes[node]['payoff']
    return sum

def size(G, color):
    s= 0
    for node in G.nodes():
        if G.nodes[node]['color'] == color:
            s+= 1
    return s

def max_dif_color_classes(G, colors):
    dif= []
    for i in colors:
        for j in colors:
            if i<j:
                s_i=size(G, i)
                s_j=size(G, j)
                a = abs(s_i - s_j)
                dif.append(a)
                print('diff', i, j, a)
    return max(dif)         
            
def assign_payoffs(G, colors):
    for node in G.nodes:
        G.nodes[node]['payoff'] = assign_payoff_poly(node, G, colors)
    return
    
def debug(G, available_colors, prob):
     for node in G.nodes:
        print("{} : {}".format(node, G.nodes[node]))
        print(node,'strategy', random_strategy_poly(node, G, available_colors, prob))        

def evaluate(G, available_colors):    
    #ne = is_Nash_equilibrium(G, available_colors)
    maxdif= max_dif_color_classes(G, available_colors)
    po =  total_payoff(G)
    print('maxdif', maxdif)
    print('totalPO', po)
    return maxdif, po

def init(num_nodes, num_colors, prob):
    G = planar_3tree(num_nodes)
    available_colors = TOTAL_COLORS[0:num_colors]

    random_coloring(G, available_colors)
    assign_payoffs(G, available_colors)
    #maxdiff, po = evaluate(G, available_colors) 
    debug(G, available_colors, prob)
    # Figure 1 shows the initial random graph
    plt.figure(1)
    draw_planar(G)
    return (G, available_colors)   
    
def improve(G, available_colors, prob):  
    apply_strategies(G, available_colors, prob)
    assign_payoffs(G, available_colors)
    #maxdiff, po = evaluate(G, available_colors)  
    debug(G, available_colors, prob)
    return

