#!/usr/bin/env python
from pyraf import iraf
from iraf import noao, imred, ccdred, images
import os

#nombre del OB
nombreOB="OB1.fits"
#BIAS
outbias="bias"+nombreOB
print("Combinando el Bias...")
#crea el directorio que contendra los archivos
os.system("mkdir bias/ccd2")
#crea una lista con los archivos
os.system("ls bias/*.fits>list-2-out.txt")
#crea una lista con los archivos de salida
os.system("find bias/-name list-2-out.txt -exec sed
 -i s/OsirisBias/OsirisBias-CCD2/g {} \;")
iraf.imutil.imcopy(input="bias/*.fits[2]", output="@list-2-out.txt")
#borra el header de la imagenes
iraf.hedit("bias/*CCD2.fits", fields="DATASEC", verify="no", delete="yes",
 update="yes")
iraf.hedit("bias/*CCD2.fits", fields="CCDSEC", verify="no", delete="yes",
 update="yes")
#mueve los archivos a la carpeta creada
os.system("mv bias/*CCD2.fits bias/ccd2")
#crea el archivo bias maestro para la reduccion
iraf.zerocombine(input="bias/ccd2/*.fits", output=outbias,  combine="average",
 ccdtype=" ", rdnoise="4.5", gain="0.95") 
iraf.hedit("*.fits", fields="CCDSEC", verify="no", delete="yes", update="yes")

#FLATS
outflat="flat"+nombreOB
print("Combinando los flats...")
#crea el directorio que contendra los archivos
os.system("mkdir flat/ccd2")
os.system("mkdir flat/ccd2-b")
#crea una lista con los archivos
os.system("ls flat/*.fits>list-2-out.txt")
#crea una lista con los archivos de salida
os.system("find flat/-name list-2-out.txt -exec sed 
-i s/OsirisSkyFlat/OsirisSkyFlat-CCD2/g {} \;")
iraf.imutil.imcopy(input="flat/*.fits[2]", output="@list-2-out.txt")
#borra el header de la imagenes
iraf.hedit("flat/*CCD2.fits", fields="DATASEC", verify="no", delete="yes", 
update="yes")
iraf.hedit("flat/*CCD2.fits", fields="CCDSEC", verify="no", delete="yes", 
update="yes")
#crea una lista de los archivos para exraer el bias
os.system("ls flat/*CCD2.fits>list-b.txt")
os.system("find flat/-name list-b.txt -exec sed -i s/CCD2/CCD2-b/g {} \;")
#sustrae el bias al flat
iraf.noao.ccdred.ccdproc(images="flat/*CCD2.fits", output="@list-b.txt", 
max_cache="2000", fixpix="no", overscan="no", trim="no", ccdtype=" ", zerocor="yes", 
darkcor="no", flatcor="no", biassec="image", trimsec="image", zero=outbias)
#Crea el archivo flat maestro para la reduccion
iraf.noao.ccdred.flatcombine(input="flat/*b.fits", output=outflat, combine="average", 
ccdtype=" ", process="no", subsets="no", rdnoise="4.5", gain="0.95") 
#mueve los archivos a la carpeta creada
os.system("mv flat/*CCD2.fits flat/ccd2")
os.system("mv flat/*b.fits flat/ccd2-b")

#extraccion de bias a flat al objeto
os.system("mkdir object/ccd2")
os.system("mkdir object/ccd2-b")
os.system("mkdir object/ccd2-b-f")
#crea una lista con los archivos para exraer el ccd2
os.system("ls object/*.fits>ob-list-2-out.txt")
#busca y remplaza en la list
os.system("find object/-name ob-list-2-out.txt -exec sed 
-i s/OsirisBroadBandImage/Object-CCD2/g {} \;")
#extrae el ccd2
iraf.imutil.imcopy(input="object/*.fits[2]", output="@ob-list-2-out.txt")
#borra el header de la imagenes
iraf.hedit("object/*CCD2.fits", fields="DATASEC", verify="no", delete="yes",
 update="yes")
iraf.hedit("object/*CCD2.fits", fields="CCDSEC", verify="no", delete="yes", 
update="yes")
#crea una lista de los archivos para exraer el bias
os.system("ls object/*CCD2.fits>ob-list-b.txt")
os.system("find object/-name ob-list-b.txt -exec sed -i s/CCD2/CCD2-b/g {} \;")
#sustrae el bias al objeto
iraf.ccdproc(images="object/*CCD2.fits", output="@ob-list-b.txt", ccdtype=" ",  
fixpix="no", overscan="no", trim="no", zerocor="yes", darkcor="no", flatcor="no", 
biassec="image", trimsec="image", zero=outbias)
#crea una lista de los archivos para exraer el flat
os.system("ls object/*b.fits>ob-list-b-f.txt")
os.system("find object/-name ob-list-b-f.txt -exec sed -i s/CCD2-b/CCD2-b-f/g {} \;")
#sustrae los falts al objeto
iraf.ccdred.ccdproc(images="object/*b.fits", output="@ob-list-b-f.txt", ccdtype=" ",  
fixpix="no", overscan="no", trim="no", zerocor="no", darkcor="no", flatcor="yes", 
biassec="image", trimsec="image", flat=outflat)
#mueve los archivos a las carpetas
os.system("mv object/*CCD2.fits object/ccd2")
os.system("mv object/*b.fits object/ccd2-b")
os.system("mv object/*f.fits object/ccd2-b-f")

#reduccion basica estrella estandar
stan="stds"+nombreOB
carp="stds/"+stan
iraf.imutil.imcopy(input="stds/*.fits[2]", output=carp)
#borra el header
iraf.hedit("stds/*.fits", fields="DATASEC", verify="no", delete="yes", update="yes")
iraf.hedit("stds/*.fits", fields="CCDSEC", verify="no", delete="yes", update="yes")
#sustrae el bias al objeto
iraf.ccdproc(images=carp, output="stds/stds-b.fits", ccdtype=" ",  fixpix="no", overscan="no", trim="no", zerocor="yes", darkcor="no", flatcor="no", biassec="image", trimsec="image", zero=outbias)
#crea una lista de los archivos para exraer el flat
#sustrae los falts al objeto
iraf.ccdred.ccdproc(images="stds/*b.fits", output="stds/stds-b-f.fits", ccdtype=" ",  fixpix="no", overscan="no", trim="no", zerocor="no", darkcor="no", flatcor="yes", biassec="image", trimsec="image", flat=outflat)
print("All done!")
