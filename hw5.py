from numpy import *
from matplotlib.pyplot import *
import scipy.constants as sc
import copy
import scipy.integrate as integ

# test sun/earth with hw5(1.989e30,5.972e24,149.6e6,0.0167,1000)
def hw5(m1, m2, a, e, tmax, tstep=0.001, tplot=0.025, method='leapfrog'):
    if method != 'leapfrog' and method != 'odeint':
        print("That's not a method")
        return()

    # initialize commonly used variables
    period = sqrt((4*(pi**2)*(a**3)) / (sc.G*(m1 + m2)))
    dt = period*tstep

    # initialize objects at time 0
    q = m1 / m2
    r0 = (1-e)*a/(1+q)
    v0 = (1/(1+q))*sqrt((1+e)/(1-e))*sqrt(sc.G*(m1+m2)/a)
    rv = array([r0, 0, 0, v0, -q*r0, 0, 0, -q*v0])
    
    # set up figure
    figure(1)
    gca().set_aspect('equal')
    xlim([-2*a, 2*a])
    ylim([-2*a, 2*a])
    
    rv_list = []
    if method == 'leapfrog':
        timeCounter = 0
        frameCounter = 0
        while timeCounter < tmax:
            # plot positions if tplot time has passed
            if frameCounter >= tplot:
                frameCounter = 0
                rv_list.append(copy.deepcopy(rv))
                
            # calc positions
            rv[0] = rv[0] + rv[2]*dt
            rv[1] = rv[1] + rv[3]*dt
            rv[4] = rv[4] + rv[6]*dt
            rv[5] = rv[5] + rv[7]*dt
            
            # calc acceleration
            r = array([rv[0] - rv[4], rv[1] - rv[5]])
            force = ((sc.G*m1*m2)/(np.linalg.norm(r)**2))*(r/np.linalg.norm(r))
            
            # calc velocity
            rv[2] = rv[2] - (force[0]/m1)*dt
            rv[3] = rv[3] - (force[1]/m1)*dt
            rv[6] = rv[6] + (force[0]/m2)*dt
            rv[7] = rv[7] + (force[1]/m2)*dt
            
            # increment counters
            timeCounter += tstep
            frameCounter += tstep
            
        # plot final position
        rv_list.append(copy.deepcopy(rv))
        rv_list_plot = rv_list
    else:
        # odeint
        rv_list = integ.odeint(deriv, rv, arange(0, tmax*period, dt), (m1, m2))
        # needed to calculate using tstep, but we want to plot
        # using tplot,
        t_interval = tplot / tstep
        rv_list_plot = rv_list[::t_interval]

    # plot
    for i in range(len(rv_list_plot)):
        plot(rv_list_plot[i][0],rv_list_plot[i][1],'bo')
        plot(rv_list_plot[i][4],rv_list_plot[i][5],'go')
        draw()

def deriv(rv, dt, m1, m2):
    # calc position deriv
    rv_copy = zeros(8)
    rv_copy[0] =  rv[2]
    rv_copy[1] =  rv[3]
    rv_copy[4] =  rv[6]
    rv_copy[5] =  rv[7]
    
    # calc velocity deriv
    r = array([rv[0] - rv[4], rv[1] - rv[5]])
    force = ((sc.G*m1*m2)/(np.linalg.norm(r)**2))*(r/np.linalg.norm(r))

    rv_copy[2] =  - (force[0]/m1)
    rv_copy[3] =  - (force[1]/m1)
    rv_copy[6] =  + (force[0]/m2)
    rv_copy[7] =  + (force[1]/m2)
    
    return rv_copy
