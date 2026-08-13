import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from PIL import Image

L=32
N=10000
r=1
r_b=4
v_0=2
a=0.15
it=400

X=[]
Y=[]
directions=[]
U=[]
V=[]
C=[]

for i in range(N):
    X.append(np.random.randint(0, L-1)+np.random.random())
    Y.append(np.random.randint(0, L-1)+np.random.random())
    directions.append((np.random.random()-0.5)*2*np.pi)
    U.append(np.cos(directions[i]))
    V.append(np.sin(directions[i]))
    C.append(directions[i])

X=np.array(X)
Y=np.array(Y)
directions=np.array(directions)

positions=np.ones((N,2))
for i in range(N):
   positions[i][0]=X[i]
for i in range(N):
   positions[i][1]=Y[i]

bird_of_prey=True

if bird_of_prey:
    x_Bp=np.random.randint(0, L-1)+np.random.random()
    y_Bp=np.random.randint(0, L-1)+np.random.random()
    direction_Bp=(np.random.random()-0.5)*2*np.pi
    bop_position=[x_Bp,y_Bp]
    u=np.cos(direction_Bp)
    v=np.sin(direction_Bp)
    c=direction_Bp

matplotlib.use("Agg")

for i in range(it):
    
    plt.quiver(X, Y, U, V, C)
    
    if bird_of_prey:
        plt.quiver(x_Bp, y_Bp, u, v, c)
    
    #plt.savefig(f"birds_pic\\{i}")
    
    plt.show()
    plt.clf()
    plt.close('all')
    
    birds_tree = cKDTree(positions,boxsize=[L,L])
    
    dist = birds_tree.sparse_distance_matrix(birds_tree,max_distance=r,output_type='coo_matrix')

    dist.eliminate_zeros()

    angles=directions[dist.row]

    exp_angles=np.exp(1j*angles)

    angles_matrix = coo_matrix((exp_angles, (dist.row, dist.col)), shape=dist.shape)

    sum_exp_angles = np.array(angles_matrix.sum(axis = 0)).flatten()

    random_angles=(np.random.rand(N)-0.5)*2*np.pi
    
    directions=(np.angle(sum_exp_angles)+a*random_angles)
    
    if bird_of_prey:
        
        nearest_bird=birds_tree.query(bop_position, 1)[1]
        
        list_of_nearest_birds=birds_tree.query_ball_point(bop_position, r_b)
        
        for i in range(len(list_of_nearest_birds)):
            
            dx_1=abs(X[list_of_nearest_birds[i]]-x_Bp) 
            dx_2=abs(X[list_of_nearest_birds[i]]-x_Bp-L)
            dx_3=abs(X[list_of_nearest_birds[i]]-x_Bp+L)
            dy_1=abs(Y[list_of_nearest_birds[i]]-y_Bp)
            dy_2=abs(Y[list_of_nearest_birds[i]]-y_Bp-L)
            dy_3=abs(Y[list_of_nearest_birds[i]]-y_Bp+L)
          
            if min(dx_1, dx_2, dx_3)==dx_1:
                vec1_x=X[list_of_nearest_birds[i]]-x_Bp  
                
            if min(dx_1, dx_2, dx_3)==dx_2:
                vec1_x=X[list_of_nearest_birds[i]]-x_Bp-L
            
            if min(dx_1, dx_2, dx_3)==dx_3:
                vec1_x=X[list_of_nearest_birds[i]]-x_Bp+L
            
            if min(dy_1, dy_2, dy_3)==dy_1:
                vec1_y=Y[list_of_nearest_birds[i]]-y_Bp  
                
            if min(dy_1, dy_2, dy_3)==dy_2:
                vec1_y=Y[list_of_nearest_birds[i]]-y_Bp-L
                
            if min(dy_1, dy_2, dy_3)==dy_3:
                vec1_y=Y[list_of_nearest_birds[i]]-y_Bp+L
                
            vec1=[vec1_x,vec1_y]
            vec2=[0.5,0]
            
            cosine_angle=np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))
            
            if vec1_y>=0:
                new_direction=np.arccos(cosine_angle)
            if vec1_y<0:
                new_direction=(-1)*np.arccos(cosine_angle)
            
            directions[list_of_nearest_birds[i]]=new_direction+a*((np.random.random()-0.5)*2*np.pi)
            
            direction_Bp=directions[nearest_bird]+0.0001*a*((np.random.random()-0.5)*2*np.pi)
        
        
    for i in range(N):
        X[i]=X[i]+v_0*np.cos(directions[i])*0.1
        Y[i]=Y[i]+v_0*np.sin(directions[i])*0.1
        if X[i]>L:
            X[i]=X[i]-L
        if X[i]<0:
            X[i]=X[i]+L
        if Y[i]>L:
            Y[i]=Y[i]-L
        if Y[i]<0:
            Y[i]=Y[i]+L
            
    for i in range(N):
        positions[i][0]=X[i]
    for i in range(N):
        positions[i][1]=Y[i]     
        
    U=np.cos(directions)
    V=np.sin(directions)
    C=directions
                
    if bird_of_prey:
        x_Bp=x_Bp+v_0*np.cos(direction_Bp)*0.1
        y_Bp=y_Bp+v_0*np.sin(direction_Bp)*0.1
        if x_Bp>L:
           x_Bp=x_Bp-L
        if x_Bp<0:
           x_Bp=x_Bp+L
        if y_Bp>L:
           y_Bp=y_Bp-L
        if y_Bp<0:
           y_Bp=y_Bp+L
        u=np.cos(direction_Bp)
        v=np.sin(direction_Bp)
        c=direction_Bp
        bop_position=[x_Bp,y_Bp]

# Create the frames
#frames = []
#imgs = []
#for i in range(it):
 #   imgs.append(f"birds_pic\\{i}.png")
#for i in imgs:
 #   new_frame = Image.open(i)
  #  frames.append(new_frame)
# Save into a GIF file that loops forever
#frames[0].save('mojgif_0.0001.gif', format='GIF',
 #              append_images=frames[1:],
  #             save_all=True,
   #            duration=150, loop=0)
   


