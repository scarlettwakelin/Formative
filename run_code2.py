import ray_IASP91_v2

ray = ray_IASP91_v2.Raytrace()

pars= [(15, "Pm", 1), (15, "Sm", 1), (5, "PmPm", 1), (5, "SmPm", 1),\
       (5, "PmSm", 1), (5, "SmSm", 1), (5, "PmPoSm", 1), (5, "SmPoSm", 1), ]

# Print travel times and defkection angles for all paths types in pars
for args in pars:
  print("Theta=", args[0], " path=", args[1])
  T, Delta = ray.trajectory(*args)
  if(T > 0) : 
      print("T=", T, " Delta=", Delta)
      ray.plot_trajectory()
      # Save to files: remove plr.show() from ray_IASP91_v2.py and uncomment:
      #ray_IASP91_v2.plt.savefig("wave_path_"+args[1]+"_theta"+str(args[0])+".eps")
      #ray_IASP91_v2.plt.close()
  else:
      print("no valid path")
      
