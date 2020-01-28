from rayleigh_diagnostics import AZ_Avgs, build_file_list, plot_azav, streamfunction
import matplotlib.pyplot as plt
import pylab
import numpy
import glob

file_dir = sorted(glob.glob('AZ_Avgs/*'))
print(len(file_dir))

for k in file_dir:
    print(k)
    files = [k]
    az = AZ_Avgs(files[0],path='')
    nfiles = len(files)
    tcount=0
    for i in range(nfiles):
        az=AZ_Avgs(files[i],path='')

        if (i == 0):
            nr = az.nr
            ntheta = az.ntheta
            nq = az.nq
            azavg=numpy.zeros((ntheta,nr,nq),dtype='float64')

        for j in range(az.niter):
            azavg[:,:,:] += az.vals[:,:,:,j]
            tcount+=1
    azavg = azavg*(1.0/tcount)

    lut = az.lut
    vr = azavg[:,:,lut[1]]
    vtheta = azavg[:,:,lut[2]]
    vphi = azavg[:,:,lut[3]]
    rhovr = azavg[:,:,lut[201]]
    rhovtheta = azavg[:,:,lut[202]]
    temperature = azavg[:,:,lut[501]]
    radius = az.radius
    costheta = az.costheta
    sintheta = az.sintheta

    #Subtrace the ell=0 component from temperature at each radius
    for i in range(nr):
        temperature[:,i]=temperature[:,i] - numpy.mean(temperature[:,i])

    #Convert v_phi to an Angular velocity
    omega=numpy.zeros((ntheta,nr))
    for i in range(nr):
        omega[:,i]=vphi[:,i]/(radius[i]*sintheta[:])

    psi = streamfunction(rhovr,rhovtheta,radius,costheta,order=0)
    #contours of mass flux are overplotted on the streamfunction PSI
    rhovm = numpy.sqrt(rhovr**2+rhovtheta**2)*numpy.sign(psi)   
    figdpi=300
    sizetuple=(5.5*3,3*3)


    tsize = 20     # title font size
    cbfsize = 10   # colorbar font size
    fig, ax = plt.subplots(ncols=3,figsize=sizetuple) # ,dpi=figdpi)
    plt.rcParams.update({'font.size': 14})

    #temperature
    #ax1 = f1.add_subplot(1,3,1)
    units = '(nondimensional)'
    plot_azav(fig,ax[0],temperature,radius,costheta,sintheta,mycmap='RdYlBu_r',boundsfactor = 2, 
          boundstype='rms', units=units, fontsize = cbfsize)
    ax[0].set_title('Temperature',fontsize=tsize)

    #Differential Rotation
    #ax1 = f1.add_subplot(1,3,2)
    units = '(nondimensional)'
    plot_azav(fig,ax[1],omega,radius,costheta,sintheta,mycmap='RdYlBu_r',boundsfactor = 1.5, 
          boundstype='rms', units=units, fontsize = cbfsize)
    ax[1].set_title(r'$\omega$',fontsize=tsize)

    #Mass Flux
    #ax1 = f1.add_subplot(1,3,3)
    units = '(nondimensional)'
    plot_azav(fig,ax[2],psi,radius,costheta,sintheta,mycmap='RdYlBu_r',boundsfactor = 1.5, 
          boundstype='rms', units=units, fontsize = cbfsize, underlay = rhovr)
    ax[2].set_title('Mass Flux',fontsize = tsize)

    plt.draw()
    
    for h in range(len(file_dir)):
        if k is file_dir[h]:
            numbering = h
        else:
            pass
   
    if numbering < 10:
        savefile = './AZ_Avgs_anim/AZ_Avg_000'+str(numbering)+'.png'
    elif 10 <= numbering < 100:
        savefile = './AZ_Avgs_anim/AZ_Avg_00'+str(numbering)+'.png'
    else:
        savefile = './AZ_Avgs_anim/AZ_Avg_0'+str(numbering)+'.png'
    #print('Saving figure to: ', savefile)
    plt.savefig(savefile)
    plt.cla()
