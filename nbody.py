from numpy import *
from matplotlib.pyplot import *

def space(nsteps=10000):
    planetposx=[]
    planetposy=[]
    
    
    obj=[[array([0.00,150000000000.00]),array([107280000.00,0.00]),array([0.00,0.00]),5.972e28],[array([0.00,0.00]),array([0.00,0.00]),array([0.00,0.00]),1.989e30]]
    obj.append([array([0.00,50000000000.00]),array([207280000.00,0.00]),array([0.00,0.00]),3e25])
    
    for a in range(len(obj)):
        planetposx.append([])
        planetposy.append([])
    
    fobj=obj
    g=00.0008649296639999999
    while nsteps>0:
        for o in range(len(obj)):
            fobj[o][0]=obj[o][0]+obj[o][1]
            fobj[o][1]=obj[o][1]+obj[o][2]  
            
            fobj[o][2]=array([00.00,00.00])
            for a in range(len(obj)):
                if obj[o][3]!=obj[a][3]:
                    direct=obj[a][0]-obj[o][0]
                    fobj[o][2]=fobj[o][2]+((direct*g*obj[a][3])/((direct[0]**2+direct[1]**2)**(1.5)))
            
        obj=fobj
        
        for b in range(len(obj)):
            planetposx[b].append(obj[b][0][0])
            planetposy[b].append(obj[b][0][1])
        
        nsteps=nsteps-1
        
    fig = figure()
    ax=fig.add_subplot(111,aspect='equal')
    for b in range(len(obj)):
        plot(planetposx[b],planetposy[b])
    
    #plot(planet2posx,planet2posy, 'r', lw=2)
    #xlim([-1.6e11,1.6e11])
    #ylim([-1.6e11,1.6e11])
    draw()