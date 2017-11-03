import numpy as np
import matplotlib.pyplot as plt

RE = 6371.0 # Earth Radius
RM = 3482.0 # Bottom of mantel radius
RC = 1217.1 # Inner core radius
# Slowness as function of r
#

class Raytrace:

    def __init__(self):
        self.list_r = []  # list of values for radial coordinates
        self.list_th= []  # list of values for theta  coordinates
        self.list_wave = [] # list of wave types
       
    def Vp(self, r):
        """ Vp as a function of radial position
            SOURCE: DOI: http://doi.org/10.2312/GFZ.NMSOP_r1_DS_2.1

        : param r : distance from Earth centre
        """
        x = r/RE
        if(r <1217.1):
            v=11.24094-4.09689*x*x
        elif(r<3482):
            v=10.03904+3.75665*x-13.67046*x*x
        elif(r<3631):
            v=14.49470-1.47089*x
        elif(r<5611):
            v=25.1486-41.1538*x+51.9932*x*x-26.6083*x*x*x
        elif(r<5711):
            v=25.96984-16.93412*x
        elif(r<5961):
            v=29.38896-21.40656*x
        elif(r<6161):
            v=30.78765-23.25415*x
        elif(r<6251):
            v=25.41389-17.69722*x
        elif(r<6336):
            v=8.78541-0.74953*x
        elif(r<6351):
            v=6.50
        else:
            v=5.80
        return(v)

    def Vs(self, r):
        """ Vs as a function of radial position
            SOURCE: DOI: http://doi.org/10.2312/GFZ.NMSOP_r1_DS_2.1

        : param r : distance from Earth centre
        """
        x = r/RE
        if(r <1217.1):
            v=3.56454-3.45241*x*x
        elif(r<3482):
            v=0.0
        elif(r<3631):
            v=8.16616-1.58206*x
        elif(r<5611):
            v=12.9303-21.2590*x+27.8988*x*x-14.1080*x*x*x
        elif(r<5711):
            v=20.76890-16.53147*x
        elif(r<5961):
            v=17.70732-13.50652*x
        elif(r<6161):
            v=15.24213-11.08552*x
        elif(r<6251):
            v=5.75020-1.27420*x
        elif(r<6336):
            v=6.706231-2.248585*x
        elif(r<6351):
            v=3.75
        else:
            v=3.36
        return(v)

    def u(self, r, wave):
        """ Return slowness for the specified wave and position

        : param r : distance from Earth centre
        : param wave : wave type : 'P' and 'S'
        """
        if(wave=='P') : return(1./self.Vp(r))
        return(1./self.Vs(r))

### MARKING coding 1
    def T_Delta_Int(self, r, p, wave):
        RU2 = (r * self.u(r, wave)) ** 2
        T = RU2 / (r * (RU2 - (p ** 2) ) ** 0.5)
        D = p / (r * (RU2 - (p ** 2)) ** 0.5)
        return (T, D)
### END MARKING

    def Int(self, dr, p, wave):
        """ Integrate function T_Delta_Int from RE to bottom.
        Save the values of r, Delta and wave in the class lists 'list_r', 
        'list_th' and 'list_wave', used by 'plot_trajectory' to generate figures
        Return [T,Delta] for the path or [-1, 0] if the path does not exist.

        :param dr: radial step
        :param p : ray parameter
        :param wave : type of wave: 'P' or 'S'
        """
        V = np.array([0., 0.])
        r = RE
        self.list_r.append(r)
        self.list_th.append(0)
        self.list_wave.append(wave)
        r+= dr*0.5 # move to middle of segment

        while(r*self.u(r, wave) > p): # while still going down
          V += self.T_Delta_Int(r, p, wave)*dr
          r -= dr
          self.list_r.append(r)
          self.list_th.append(V[1])
          self.list_wave.append(wave)
          
        r += dr  # gone too far: move back
### MARKING coding 1
        while(r < RE):
### END MARKING
          V += self.T_Delta_Int(r, p, wave)*dr
### MARKING coding 1
          r += dr
### END MARKING
          self.list_r.append(r)
          self.list_th.append(V[1])
          self.list_wave.append(wave)
          if((wave == "S") and (r < RM)): # no S wave in outer core
            return(np.array([-1, 0]))

        return(V)
    
### MARKING: coding 2
    #def Int_mPm(self, dr, p, wave):
    #def Int_mSm(self, dr, p, wave):
    #def Int_mPoSm(self, dr, p, wave):     
### END MARKING

### MARKING coding 1
    def plot_VpVs(self):
        rs =np.linspace(0, RE, 1000)
        vps, vss = [], []
        for r in rs:
            vps.append(self.Vp(r))
            vss.append(self.Vs(r))
        plt.plot(rs, vps, color="blue", label="Vp")
        plt.plot(rs, vss, color="red", label="Vs")
        plt.xlabel("r", fontsize=12)
        plt.ylabel("Vs, Vp", fontsize=12)
        plt.legend()
        plt.show()
### END MARKING
        
    def plot_circle(self, R, col):
        """ Plot a circle of radius R in colour col

        :param R : circle radius
        :param col : circle color ('r', 'g', 'b', 'k', 'c', 'm', or 'y')
        """
        circle2 = plt.Circle((0, 0), R, color=col, fill=False, linewidth=2)
        ax = plt.gca()
        #ax.cla() # clear things for fresh plot
        ax.add_artist(circle2)

    def trajectory(self, theta, wave, dr):
        """ Compute the trajectory of the specified wave 
            Return Traveling time and angle (T, Delta)

        :param theta : incident angle in degrees
        :param path : Pm PmPm PmSm PmPoSm Sm SmPm SmSm SmPoSm
        :param dr : integration step in km
        """
        self.list_r = []
        self.list_th = []
        self.list_wave = []
        self.theta=theta
        self.path=wave

### MARKING coding 2
        th = np.radians(theta)
        p = RE*self.u(RE, wave)*np.sin(th)

        T, DeltaP = self.Int(dr, p, wave)
### END MARKING

        return(T, np.degrees(DeltaP))
    
    
    def plot_trajectory(self):
        """ Plot the Earth Radius in green the boundary between the mantel and
            the outer core in magenta and the boundary between the 2 cores in
            red. Then plot the trajectory of the waves in black for P waves
            and blue for S waves.
        """
        self.plot_circle(RE, "g")
        self.plot_circle(RM, "m")
        self.plot_circle(RC, "r")
    
        xl = []
        yl = []
        thmax = self.list_th[-1]*0.5 # to generate symmetric figure
        n = len(self.list_r)         # number of data points
        wave = self.list_wave[0]     # wave type

### MARKING coding 1
        # POPULATE xl and yl with data
        for x in range(0, n-1):
            xl.append(self.list_r[x] * np.sin(self.list_th[x] - thmax))
            yl.append(self.list_r[x] * np.cos(self.list_th[x] - thmax))
### END MARKING
        
        # select colour
        if(wave == "P") : col = "k"
        else: col = "b"
        
        plt.title(r'$\theta=$'+str(self.theta)+", path="+self.path)
        plt.plot(xl, yl, col)
        plt.axis([-8500, 8500, -6500, 6500], 'equal')
        plt.show()

        
### MARKING coding 3
    # def plot_multi_trajectory(self, nocircle=False):
### END MARKING
