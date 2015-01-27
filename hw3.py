#Steven Morad
#January, 2015. Winter
#Astro 119.

#Group members: 
#    Ghassemi, Elliot
#    Kerslager, Forrest
#    Smithers, Ben
#    Rodriguez, Kevin

#Routine imports
from numpy import *
from matplotlib.pyplot import *

#Special import, as we'll be downloading files from the web
import urllib2 

#Because we like neat color maps
import matplotlib.cm as cm


#Definition of our fetch_file function
def fetch_file(url='https://sites.google.com/a/ucsc.edu/krumholz/teaching-and-courses/ast119_w15/homework-3/hw3.npy', localfile='hw3.npy'):
    #establishing a connection with server at "url"
    urlptr=urllib2.urlopen(url) 
    
    rawdata=urlptr.read()
    
    #closing connection with server, not necessary from here on
    urlptr.close() 
    
    #Since .npy files are essentially binary files with headers, we will create a 
    #   binary file of the given name.
    
    #Inside the binary file, we will write down the 1's and 0's that stream 
    #   down from the given url.
    
    fp=open(localfile,'wb')
    fp.write(rawdata)
    fp.close()
    
    
def hw3():
    #Let's see if hw3.npy exists
    try:
        #Here, we try to load the file which may have been made previously in
        #   the fetch_file function. If it's there, we load it. 
        data=load('hw3.npy')
    except IOError:
        print("Warning: file hw3.npy not found; retrieving from the web")
        fetch_file()
        data=load('hw3.npy')
        #If it was not made earlier, we call the fetch_file function and
        #   immediately load it into memory. 
    
    #The data variable is now a 2D array. 
    
    #To begin: we will now create two evenly spaced arrays over [-1,1]
    #   with a number of elements equal to the size of data
    x=linspace(-1,1,len(data[0])) #the [0] refers to the columns
    y=linspace(-1,1,len(data))    #lack of the [0] assumes rows. 
    
    
    #Creating the first figure. 
    figure(1)
    
    #The imshow command draws our data in a square diagram, using the lower left 
    #    as the origin. We draw on a 2x2 board with corners (-1,-1) and (1,1)
    #    For aesthetics, we use the heat map as a color pallet
    
    imshow(data,aspect='equal',origin='lower',extent=(-1,1,-1,1),cmap=cm.hot)
    #Adding the colorbar
    colorbar()
    #Adding the pizzazz 
    xlabel('x')
    ylabel('y')
    xlim([-1,1])
    ylim([-1,1])
    draw()
    savefig('hw3a.png')
    
    
    #These will be our placeholders for the means of rows and columns
    meanofrows=zeros(len(data))  #len(data) tells us how many rows there are
    #len(data[0]) tells us how many columns there are
    meanofcolumns=zeros(len(data[0])) 
    
    
    #Although a for loop would be the best option in this case, I ran into
    #   many issues using one. Deciding that functionality is more favorable to
    #   aesthetics, I opted to instead use while loops.
    
    #Here we define r and c, the number of rows and columns repectively. 
    #These will be used in the while loops to go and address each
    #   row and column individually. 
    #The -1 is in place as arrays are addressed starting from 0. 
    
    r=len(data)-1
    c=len(data[0])-1
    
    #Here come the while loops. 
    while r>=0:
        #For a given row R, we take it's mean and assign it to R's value in the
        #   array meanofrows.
        meanofrows[r]=mean(data[r,:])  
        r=r-1
    while c>=0:
        #This takes the mean of  column "c"
        meanofcolumns[c]=mean(data[:,c])   
        c=c-1
    
    #Now we have collected the means of rows and columns into their own neat little
    #   arrays: meanofrows and meanofcolumns
    
    #Now we want to find the maximum value between both of these arrays
    #   To do this, we take the maximum of the maximum of each.
    xm=max(max(meanofrows),max(meanofcolumns))
    
    #Creating our second figure. It will be different from the last.
    figure(2)
    
    #We choose to have two subplots, arranged vertically. 
    #We will start with the top one. 
    subplot(2,1,1)
    plot(x,meanofcolumns,'y',lw=3) #yellow.
    ylim([0,1.5*xm])
    xlabel('x')
    ylabel('Density')
    legend(['X-mean'])
    
    #Odd note, if one uses say...
    #   legend(('X-mean'))
    #   in lieu of the aboved used command, the returned legend holds only a
    #   capitalized letter X
    
    subplot(2,1,2)
    plot(y,meanofrows, 'c', lw=3) #cyan
    ylim([0,1.5*xm])
    xlabel('y')
    ylabel('Density')
    legend(['Y-mean'])
    
    #Reticulating splines 
    #           .... and adjusting the space between subplots.
    subplots_adjust(hspace=0.3)
    draw()
    
    savefig('hw3b.png')

    
    
    
    
