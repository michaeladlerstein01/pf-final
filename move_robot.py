# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:18:11 2022

@author: michael
"""

import numpy as np 
import pygame 
import math 
import random as r
from scipy.stats import norm


green = (0 , 255 , 0)
red = (255 , 0 , 0)
blue = (0 ,0 , 255)
white = (255 ,255 , 255)
col  = (252, 3, 219)
black = (0 ,0 ,0)

pygame.init()
dimx , dimy = 800 , 600
surface = pygame.display.set_mode((dimx , dimy))
manholes= [(100 , 200) , (300 , 400) , (400 , 200) , (500 , 500) , (200 , 500) , (206 , 200) , (300 , 80), (100 , 100) , (200  , 150) , (150 , 200) , (200  , 150) , (300 , 350) ]
              

        
def plot_manholes(manholes) :
    for point in manholes :
        draw = pygame.draw.circle(surface, green, (point[0] , point[1]) , 5)
    for i in range(1 , len( manholes)) :
        lines = pygame.draw.line(surface , white , (manholes[i-1][0],manholes[i-1][1]) ,  (manholes[i][0],manholes[i][1]) )                         
    pygame.display.flip() 
 
starting_point =  manholes[1]
location = starting_point
n = manholes.index(location)



def move(location,  n):
    if event.key == pygame.K_RIGHT :       
        step = np.random.normal(5, 1) 
        x = manholes[n+1][0] - manholes[n][0]
        y = manholes[n+1][1] - manholes[n][1]  
        grad = y/x 
        angle = np.arctan(y/x)
        if grad != 0 and manholes[n+1][0] - manholes[n][0] > 0 :                                                          
            locationx = location[0] + np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (round(locationx , 2), round(locationy , 2))   
        if grad == 0 and location[0] > manholes[n+1][0]:
            locationx = location[0] - np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (int(locationx) , int(locationy))             
        if grad == 0 and location[0] < manholes[n+1][0]:
            locationx = location[0] + np.cos(angle)*step
            locationy = location[1] + np.sin(angle)*step
            location = (int(locationx) , int(locationy))                             
        if  x < 0:
            locationx = location[0] - np.cos(angle)*step
            locationy = location[1] - np.sin(angle)*step
            location = (round(locationx , 1), round(locationy , 1))    
        return location 
        
    
def sense(location , n ):      
    distance = np.sqrt((manholes[n+1][0] - location[0])**2 + (manholes[n+1][1] - location[1])**2) + np.random.normal(0, 1) 
    if distance < 5: 
        location = manholes[n+1]
        n +=1 

        return n , location  , distance
    else:
        n = n
    return n  , location , distance 

length = len(manholes)-1 

number_particles = 10

particle_location = location
particle_angle = []
particle_list = []


def move_particles(particle_location):        
    if event.key == pygame.K_RIGHT :
        x = manholes[n+1][0] - manholes[n][0]
        y = manholes[n+1][1] - manholes[n][1]  
        grad = y/x  
        angle_particle = np.arctan(y/x) + np.random.normal(0, 0.1) 
        particle_angle.append(angle_particle)
        
        step_particle = np.random.normal(5, 1 , number_particles)    
        if grad != 0 and manholes[n+1][0] - manholes[n][0] > 0 :                                                          
            locationx = particle_location[0] + np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            particle_location = (np.round(locationx , 2), np.round(locationy , 2))   

        if grad == 0 and np.mean(particle_location[0]) > manholes[n+1][0]:
            locationx = particle_location[0] - np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            particle_location = (np.intc(locationx) , np.intc(locationy))    

        if grad == 0 and np.mean(particle_location[0]) < manholes[n+1][0]:
            locationx = particle_location[0] + np.cos(angle_particle)*step_particle
            locationy = particle_location[1] + np.sin(angle_particle)*step_particle
            particle_location = (np.intc(locationx) , np.intc(locationy))   
                      
        if  x < 0:
            locationx = particle_location[0] - np.cos(angle_particle)*step_particle
            locationy = particle_location[1] - np.sin(angle_particle)*step_particle
            particle_location = (np.round(locationx , 2), np.round(locationy , 2))
        
        particle_list.append(particle_location)  
        return particle_location 
     

def particle_sense(particle_location , n ):
    x1 = particle_location[0]
    y1 = particle_location[1]

    particle_distance = np.sqrt((manholes[n+1][0] - particle_location[0])**2 + (manholes[n+1][1] - particle_location[1])**2) + np.random.normal(0, 2) 
    return particle_distance 



weight_particle = []
def weight(distance , particle_distance):
    weight_particle  = norm.pdf(particle_distance, distance, 2 )
    return weight_particle

def resample(weight_particle , particle_location ):
    resample = r.choices(particle_distance , weight_particle , k = number_particles)
    particle_location = resample
    return particle_location
         
#def sample()
           
    
while True : 
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT :               
            pygame.quit()
            quit()      
    if event.type == pygame.KEYDOWN:        
        n , location , distance  = sense(location , n  )                     
        if n == length:    
            print('fine') 
            manholes.reverse() 
            n = 0 
            location = (manholes[0][0] , manholes[0][1])       
        else :            
            location  = move( location, n)   
            pygame.draw.circle(surface, red, (location[0]  , location[1]) , 6)

            particle_location  = move_particles(particle_location) 
            
            for i in range(number_particles-1):
                x = particle_location[0][i]
                y = particle_location[1][i]
                pygame.draw.circle(surface, col, (x , y)  , 2) 
            
            particle_distance = particle_sense(particle_location , n )
           
           # weight_particle = weight(distance , particle_distance)
            print(weight_particle)
           
            #particle_location =  resample(weight_particle , particle_location )
            #weight_particle = []
            
            

#=============================================================================   
    else :
        pygame.draw.circle(surface, red, (location[0]  , location[1]) , 6)  
        
        
#========================================================                    
    pygame.display.update()         
    surface.fill(black)                               
    pygame.time.delay(100)                  
    plot_manholes(manholes)  

   