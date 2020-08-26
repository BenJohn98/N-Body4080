# LittleUniverse, v.1.1
# Adapted by Benjamin Oxley from code written by Dr. Martin Stringer, UQ.
# Submitted for assessment in PHYS4080, Semester 2, 2020, University of Queensland.
# 26/08/2020

import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D


# It plots collisionles particles moving at random in a cubic box in the main panel
# and shows the distribution of their separations in one of two other panels.

#Seed randomly generated imputs
np.random.seed(4080)

# Prompt user to set the number of spatial dimensions (must be at least 2)
Nd = int(input('Set number of spatial dimensions (at least 2):'))
print(Nd, "Spatial dimensions chosed")


# Choose projection for the main panel
project_3d = False

# Set the number of particles to simulate
Np = int(input('Set Number of Bodies to Simulate:'))
print("Simulating", Np, "bodies")

# Set number of random bodies (for correlation function purposes) to be ten times Np
Nr = Np*10

#Prompt selection of mass assignment. Either assign random masses to obtain distribution or set all mass to 1 
#!NOTE! For the purposes of this simulation, mass and distance are unitless
mmethod = int((input('Assign Random Masses (0) or Set All Mass = 1 (1):')))
if mmethod == 0:
    print("Random Masses Assigned")
    mass = (np.random.random((1,Np)))*100
if mmethod == 1:
    print("all masses =1")
    mass = np.ones((1,Np), dtype=int)

# Set the total number of timesteps
Nt = int(input('Set total number of timesteps:'))

# Set how long the animation should dispay each timestep (in milliseconds).
frame_duration = 10
print("Running for", Nt, "timesteps, at", frame_duration, "frames per millisecond")



#set method for initial positions
pmethod = int((input('Assign random positions (0), or clump (1):')))

# Set initial positions at random within box
if pmethod == 0:
    print("Random positions assigned")
    position = 1-2*np.random.random((Nd,Np))
#set clumping configuration for initial positions
if pmethod == 1:    
    print("Selected Configuration: Dual Galaxies")
    position1 = -0.75+0.25*np.random.random((Nd,int(Np/2)))
    position2 = 0.25+0.5*np.random.random((Nd,int(Np/2)))
    position = np.concatenate([position1,position2],axis=1)

#generate random positions for correlation function
randposition = 1-2*np.random.random((Nd,Nr))
 

# Set the maximum drift velocity, in units of position units per timestep
v_max= float(input('Enter Maximum Drift Velocity of Bodies:'))
print("Maximum drift velocity is", v_max)

#choose method of velocity calculation
vmethod = int(input('Set initial velocities to be zero (0), all half of maximum (1), all maximum (2), random (3), or expansion constant (4): '))

if vmethod == 0:
    #set initial velocities to zero
    velocity = 0
if vmethod == 1:
    #set initial velocities to half maximum
    velocity = v_max/2
if vmethod == 2: 
    #set initial velocities to maximum
    velocity = v_max
if vmethod == 3:
    #set initial velocities to random fractions of max
    velocity = v_max*(1-2*np.random.random((Nd,Np)))
if vmethod == 4:
    #add constant expansion velocity to initial random velocities
    velocity = v_max*(1-2*np.random.random((Nd,Np)))+0.05



def sep(p): # Function to find separations from position vectors
    s = p[:,None,:] - p[:,:,None] # find N x N x Nd matrix of particle separations
    return np.sum(s**2,axis=0)**0.5 # return N x N matrix of scalar separations



    
# Create a function to apply boundary conditions
def apply_boundary(p):
    p[p>1]-=2
    p[p<-1]+=2
    return p 

#function for calculating distances
def magdistance(x,y,z):
    return np.sqrt(x**2 + y**2 + z**2)

#function for calculating acceleration
def acceleration(p):
    r = np.zeros((Nd,Np))
    a = np.zeros((Nd,Np))
    for i in np.arange(Np):
        ipos = p[:,i]
        for j in np.arange(Np):
            if j != i:
                r[:,j]=p[:,j]-ipos
                x_pos = r[0,j]
                y_pos = r[1,j]
                z_pos = r[2,j] 
                a[:,i] += mass[:,j]*r[:,j]/(magdistance(x_pos,y_pos,z_pos))**3
    return a/10000


# Set the axes on which the points will be shown
plt.ion() # Set interactive mode on
fig = figure(figsize=(12,6)) # Create frame and set size
subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95,wspace=0.15,hspace=0.2)
# Create one set of axes as the left hand panel in a 1x2 grid
if project_3d:
    ax1 = subplot(121,projection='3d') # For very basic 3D projection
else:
    ax1 = subplot(121) # For normal 2D projection
xlim(-1,1)  # Set x-axis limits
ylim(-1,1)  # Set y-axis limits

# Create command which will plot the positions of the particles
if project_3d:
    points, = ax1.plot([],[],[],'o',markersize=4)  ## For 3D projection
else:
    points, = ax1.plot([],[],'o',markersize=4) ## For 2D projection

ax2 = subplot(222) # Create second set of axes as the top right panel in a 2x2 grid
xmax = 2 # Set xaxis limit
xlim(0,xmax) # Apply limit
xlabel('Position')
ylabel('Correlation Function')
dx=0.05 # Set width of x-axis bins
ylim(-1,1) # Reasonable guess for suitable yaxis scale    
xb = np.arange(0,xmax+dx,dx)  # Set x-axis bin edges
xb[0] = 1e-6 # Shift first bin edge by a fraction to avoid showing all the zeros (a cheat, but saves so much time!)
line, = ax2.plot([],[],drawstyle='steps-post') # Define a command that plots a line in this panel


#generate initial position plot
points.set_data(position[0,:], position[1,:]) # Show 2D projection of first 2 position coordinates
if project_3d:
    points.set_3d_properties(position[2,:]) 

# Define procedure to update positions at each timestep
def update(i):
    global position,velocity # Get positions and velocities
    velocity += acceleration(position) #Get acceleration to simulate gravity
    position += velocity # Increment positions according to their velocites
    position = apply_boundary(position) # Apply boundary conditions
    points.set_data(position[0,:], position[1,:]) # Show 2D projection of first 2 position coordinates
    if project_3d:
        points.set_3d_properties(position[2,:])  ## For 3D projection
    hdata = histogram(np.ravel(tril(sep(position))),bins=xb)[0] #generate histogram of data
    hrand = histogram(np.ravel(tril(sep(randposition))),bins=xb)[0] #generate histogram of random dataset
    cf = np.where(hrand!=0,(hdata/(hrand/100)-1),-1) #calculate correlation function and make it -1 when random separation is zero (avoid divide by zero error)
    # Make histogram of the lower triangle of the seperation matrix
    data=line.set_data(xb[:-1],cf) # Set the new data for the line in the 2nd panel
    return points,line # Plot the points and the lines
    
# Create animation
   
plt.rcParams['animation.ffmpeg_path'] = "C:/code/python/ffmpeg/bin/ffmpeg.exe"

ani = animation.FuncAnimation(fig, update, frames=Nt,interval = frame_duration)

FFwriter = animation.FFMpegWriter()

ani.save("littleuniverse.mp4", writer = FFwriter)

plt.show()

ani.save("littleuniverse.mp4")




