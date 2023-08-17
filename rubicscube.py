import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import copy
import time
 

class Cube():
    def __init__(self, enable_state_history=False):
        self.ops = ['F','U','R','D','L','B']
        self.faces = {v:k for k,v in enumerate(self.ops)}
        self.connected_faces = {
            0: [1,2,3,4],
            1: [0,4,5,2],
            2: [0,1,5,3],
            3: [0,2,5,4],
            4: [0,3,5,1],
            5: [4,3,2,1]
        } # write in clock wise ddirection
        
        self.mat = {k:self._make_face(k) for k in range(6)}
        # Define colors corresponding to Rubik's Cube colors
        self.rubiks_colors = ['red', 'green', 'blue', 'orange', 'yellow', 'purple']
        self.cmap = ListedColormap(self.rubiks_colors)
        
        self.ops_history = ""
        self.score_history = []
        self.enable_state_history = enable_state_history
        if self.enable_state_history:
            self.state_history = [copy.deepcopy(self.mat)]
#             self.visited_states = [hash(frozenset(self.mat.items()))]
        
        
    def _make_face(self,face_color):
        return np.full((3, 3), face_color)
    
    def create_seq_ops(self,seq=1):
        return [np.random.choice(self.ops) for i in range(seq)]
    
    def operate(self,op):
        #self.ops_history.append(op)

        face = self.faces[op]
        
        self.mat[face] = np.rot90(self.mat[face], k=-1)
        connected_faces = self.connected_faces[face]
        #print(connected_faces)
        #print("connected_faces[cf]",connected_faces[0])
        swap_row = list(self.mat[connected_faces[3]][0])
        #print("swap_row",swap_row)
        
        for cf in range(len(connected_faces)-1,0,-1):
            #print(cf)
            #print("connected_faces[cf]",connected_faces[cf])
            self.mat[connected_faces[cf]][0] = self.mat[connected_faces[cf - 1]][0]
        #print("mat connected_faces:0",self.mat[connected_faces[0]])
        #print("swap_row",swap_row)
        self.mat[connected_faces[0]][0] = np.array(swap_row)
        #print(self.mat)
        
        self.ops_history += op
        self.score_history.append(self.evaluate("faces"))
        if self.enable_state_history:
            self.state_history.append(copy.deepcopy(self.mat))
#             self.visited_states.append(hash(frozenset(self.mat.items())))
        return self

    
    def shuffle(self,n=50):
        ops = self.create_seq_ops(n)
        for op in ops:
            self.operate(op)
        
    
    def render(self,face=0):
        # Create a heatmap using the custom colormap
        plt.figure(figsize=(6, 6))
        plt.imshow(self.mat[face], vmin=0, vmax=5, cmap=self.cmap, interpolation='nearest', origin='lower', extent=[0, 3, 0, 3])
        # Overlay a 3x3 grid on the heatmap
        plt.grid(which='major', linestyle='-', linewidth='2', color='black')
        plt.xticks([0, 1, 2])
        plt.yticks([0, 1, 2])
        cbar = plt.colorbar(heatmap, ticks=np.arange(0, 6))
        plt.show()

    def render_full(self,state_history_index = None):  
        if not state_history_index:
            mat = self.mat
        else:
            mat = self.state_history[state_history_index]
            
        fig, axs = plt.subplots(2,3, figsize=(10, 6))
        for i in range(2):
            for j in range(3):
                face = 3*i+j
                axs[i, j].imshow(mat[face], vmin=0, vmax=5, cmap=self.cmap, interpolation='nearest', origin='lower', extent=[0, 3, 0, 3])
                axs[i, j].axis('off')  # Turn off axes
                axs[i, j].set_title(f'Face: {face} | {self.ops[face]}')  
                axs[i, j].set_xticks([0, 1, 2])
                axs[i, j].set_yticks([0, 1, 2])
                axs[i, j].grid(True, which='both', linewidth=2, color='black') 
#                 cbar = plt.colorbar(heatmap, ticks=np.arange(0, 6))
        plt.tight_layout()
        plt.show()

    def evaluate(self,mode = "complete"):
        if mode == "complete":
            all_same = True
            for v in range(6):
                all_same = all_same and np.all(self.mat[v] == v)
            return all_same

        if mode == "faces":
            count = 0
            for v in range(6):
                flattened_matrix = self.mat[v].flatten()
                count += np.count_nonzero(flattened_matrix == v)
                # print(count)
            return count




import hashlib
import numpy as np

def hash_dict(input_dict):
    hashable_dict = {}
    
    for key, value in input_dict.items():
        if isinstance(value, np.ndarray):
            hashable_dict[key] = tuple(value.flatten())
        else:
            hashable_dict[key] = value
    
    sorted_items = sorted(hashable_dict.items())
    serialized_dict = str(sorted_items).encode('utf-8')
    
    hash_value = hashlib.pbkdf2_hmac('sha256', serialized_dict, b'salt',1)
    return hash_value.hex()

# Example dictionary
sample_dict = {
    0: np.array([[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]),
    1: np.array([[4, 4, 4],
                 [1, 1, 1],
                 [1, 1, 1]]),
    2: np.array([[1, 1, 1],
                 [2, 2, 2],
                 [2, 2, 2]]),
    3: np.array([[2, 2, 2],
                 [3, 3, 3],
                 [3, 3, 3]]),
    4: np.array([[3, 3, 3],
                 [4, 4, 4],
                 [4, 4, 4]]),
    5: np.array([[5, 5, 5],
                 [5, 5, 5],
                 [5, 5, 5]])
}

# Get the hash value for the dictionary
hash_value = hash_dict(sample_dict)

print("Hash value:", hash_value)


cube = Cube(enable_state_history=True)
cube.shuffle(10000)


Qtable = dict()
episodes = 20
def Qlearning(c,op,episodes, visited_states):
    if episodes == 0:
        return 0
    episodes -= 1
    print("episodes",episodes)
    cube_copy = copy.deepcopy(c)  # Create a copy of the cube to simulate operations
    cube_copy.operate(op)
    index = hash_dict(cube_copy.mat)
    if index in visited_states:
        return 0  # To avoid infinite loop
    
    visited_states.add(index)
    
    try:
        Qtable[index][op] = cube_copy.evaluate("faces") + max([Qlearning(cube_copy,k,episodes, visited_states) for k in cube_copy.ops])
    except:
        Qtable[index] = {k:0 for k in cube_copy.ops}
    
    return Qtable[index][op]


print(cube.ops_history)
print(cube.evaluate("faces"))
visited_states = set()

# record start time
start = time.time()
val = Qlearning(c = cube,op = 'F',episodes = 4, visited_states = visited_states)
end = time.time()
print("The time of execution of above program is :",(end-start) * 10**3, "ms")
print('val',val)
print("Qtable",Qtable)
print("visited_states",len(visited_states))
