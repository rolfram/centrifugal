from rayleigh_diagnostics import Shell_Slices
import numpy
import matplotlib.pyplot as plt
from matplotlib import ticker, font_manager
import glob

rindex = 0
sizetuple=(15,8)

fig, ax = plt.subplots(ncols=3,figsize=sizetuple)
f = sorted(glob.glob('./Shell_Slices/*'))

for i in range(len(f)):
	istring = f[i]
	ss = Shell_Slices(istring, path='')
	tindex = ss.niter-1
	ntheta = ss.ntheta
	nphi = ss.nphi
	costheta = ss.costheta
	theta = numpy.arccos(costheta)
	vr = ss.vals[:,:,rindex,ss.lut[1],tindex]
	vt = ss.vals[:,:,rindex,ss.lut[3],tindex]
	vp = ss.vals[:,:,rindex,ss.lut[3],tindex]
	temp = ss.vals[:,:,rindex,ss.lut[501],tindex]
	
	img1 = ax[0].imshow(numpy.transpose(vr),extent=[0,360,-90,90],cmap='RdYlBu_r')
	img1 = ax[1].imshow(numpy.transpose(vt),extent=[0,360,-90,90],cmap='RdYlBu_r')
	img3 = ax[2].imshow(numpy.transpose(vp),extent=[0,360,-90,90],cmap='RdYlBu_r')

	ax[0].set_title('Radial Velocity')
	ax[1].set_title('Theta Velocity')
	ax[2].set_title('Phi Velocity')
	plt.tight_layout()
	plt.draw()

	if i < 10:
		savefile = './Shell_Slices_png/slice_000' + str(i) + '.png'
	elif 10 <= i <= 100:
		savefile = './Shell_Slices_png/slice_00' + str(i) + '.png'
	else:
		savefile = './Shell_Slices_png/slice_0' + str(i) + '.png'

	plt.savefig(savefile)
	plt.cla()

