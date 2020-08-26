# LittleUniverse
N-Body simulation project for PHYS4080, University of Queensland, Semester 2, 2020.

- Source code is available on Github
- This README file is best viewed on Github

## Documentation
- Can be found on Github repository: https://github.com/BenJohn98/N-Body4080

Two main documentation files are provided in .pdf form. The first contains a breif, one-page description of the physics/methods used to generate the N-body sim. The second contains a walkthrough of various interesting situations produced by different combinations of input options in order to explain the physics concepts to a non-expert. If starting from scratch, I recommend reading nbody_physics.pdf followed by nbody_presentation.pdf to obtain a complete presentation of


## Running LittleUniverse.py
There are various input options which the user will be prompted to enter upon running the code. They are described in detail here. Various interesting situations and the imput options required to run them are shown in nbody_presentation.pdf. Each time an imput is required a message is printed to the terminal. Once an imput is entered another message is printed to confirm the code has responded. In most python environments and the linux terminal, the user must simply type their desired value and press enter. The code will not continue unless a valid input is entered. Selecting an invalid input will result in an error message specific to the environment being used. 

- Input options explained
##### Number of spatial dimensions
The first prompt asks the user to enter the number the number of spatial dimensions. For accuracy to our universe, it is recommended that you input 3 (the simulation is projected onto 2D anyway). Regardless, at least 2 dimensions are required.

##### Number of particles
This is where the user can choose exactly what the value of N in this N body simulation will be. The only requirement is that this be an integer. The number of particles is restricted by the memory of the computer on which the code is being run and larger numbers of particles will take much longer to run.

##### Mass distribution
There are two options for mass distributions in this simulation. By inputting '0', the code will assign random masses to each particle between 1 and 100 (unitless). Alternatively, mass variations can be removed from consideration by selecting '1', which sets the massess of all particles to 1. Mass in this simulation (as well as distance) is given as a unitless quantity. The main takeaway of changing these options should be the ability to analyse systems in which the smallest bodies are interacting with others up to 100 times more massive (for example a system of galaxies or stars), as well as the ability to look at systems where all bodies have the same mass (such as the approximation for dark matter particles- more info included in nbody_physics.pdf).

##### Timesteps
Chooses how many timesteps of evolution should be calculated in the simulation. Essentially, how long the simulation will last. The user always has the option to input the total number of timesteps however each frame (timestep) is always printed for 100 milliseconds in the animation, which should be kept in mind when choosing total timesteps. 

##### Initial Positions
Allows for setting two initial configurations. One for random positions and another for clumping particles in two groups.

##### Velocity
Fist the user will be asked to input maximum drift velocity (in units of position per timestep). This places a limit on the drift speed of each particle such that velocities do not increase rapidly. Next, the user is asked to choose a velocity distribution for the particles. The options given are basic but provide an extra level of customisability for the user. '0' sets initial velocities to be zero, '1' sets all initial velocities to be half of the given maximum, '2' sets sets all initial velocities to be exactly the given maximum, '3' sets velocities to be random fractions of the maximum.

- The Algorithm

Once each of the inputs has been taken, the code then computes the acceleration due to gravity on each of the particles. The algorithm itself is fairly simple consisting of only a few functions. The function **sep** is required to generate the correlation function and simlply takes the position arrays (dependant on the selected position configuration) and generates a matrix of particle separations. The function **apply_boundary** defines the periodic boundary conditions of the box. The function **magdistance** simply computes the 3D distance for each particle. Then, **acceleration** returns the acceleration at a given timestep for each particle individually, calling **magdistance** to determine the magnitude of separation for each particle. The final function, **update**, updates and plots the position and velocity of each particle given the acceleration at each timestep. Included in this function is the plot of the correlation function at each timestep. 


- Output

The final block of code is used to create an animation using the plots generated at each timestep. In a second panel, the correlation function is plotted for each timestep to easily compare with the distribution. ffmpeg is required to generate and view these animations and can be downloaded from... The path to where ffmpeg is saved needs to be specified in line 182 The animation is saved automatically as an mp4 file 'littleuniverse.mp4' in the same directory as the source code is being run. 

## Some extra notes and things to watch out for
Can improve smoothness of animation by decreasing frames per timestep however code will take longer to run.

The correlation function quite noisy, however, patterns can still be deduced (see nbody_presentation).



