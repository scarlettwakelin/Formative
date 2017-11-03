import ray_IASP91_v2
import numpy as np

pars = ["Pm", "Sm", "PmPm", "SmPm", "PmSm", "SmSm", "PmPoSm", "SmPoSm" ]

# Create ray object
ray = ray_IASP91_v2.Raytrace()

# Plot figures Vp(r) and Vs(r)
ray.plot_VpVs()

# Generate figures of trajectories for all paths types in pars 
for path in pars:
  nocircle = False
  # plot all paths for incident angle 1 to 89 degree 
  for theta in np.linspace(1, 89, 89):
    #print(theta)
    T, Delta = ray.trajectory(theta, path, 1)
    if(T > 0) : # Only plot trajectory if it exists
        ray.plot_multi_trajectory(nocircle)
        nocircle=True
  # Uncomment line below to save figure in files
  #ray_IASP91_v2.plt.savefig("wave_reach_"+path+".eps")
  #ray_IASP91_v2.plt.close()
  ray_IASP91_v2.plt.show() # display figure on screen.

pars2= [(15, "Pm", 1), (15, "Sm", 1), (5, "PmPm", 1), (5, "SmPm", 1),\
       (5, "PmSm", 1), (5, "SmSm",1 ), (5, "PmPoSm", 1), (5, "SmPoSm", 1), ]

# Print travel times and defkection angles for all paths types in pars2 
for args in pars2:
  print("Theta=",args[0]," path=",args[1])
  T, Delta = ray.trajectory(*args)
  if(T > 0) : 
      print("T=",T, " Delta=",Delta)
      #ray.plot_trajectory()
      # Save to files: remove plr.show() from ray_IASP91_v2.py and uncomment:
      #ray_IASP91_v2.plt.savefig("wave_path_"+args[1]+"_theta"+str(args[0])+".eps")
      #ray_IASP91_v2.plt.close()
  else:
      print("no valid path")
