#imports
import pandas as pd
import pygame
import random

#constants
RED = (255, 0, 0)

#functions

#data cleanup and manipulation
def createDict():
    #reading scraped data
    data = pd.read_csv('data.txt' , sep=';')
    #iterating through each row
    for i in range(0,len(data)):
        #x represents follower count
        x = data['Followers'][i]
        #finding index of any non number character
        indexC = x.find(",")
        indexK = x.find("K")
        indexM = x.find("M")
        num = 0
        #removing comma
        if indexC > 0 :
            num = x[0:indexC]
            num += x[indexC+1]
            num = float(num)
        #removing K
        elif indexK > 0:
            num = float(x[0:indexK])
            num *= 100
        #removing M
        elif indexM > 0:
            num = float(x[0:indexM])
            num *= 1000000
        # converting to float
        else:
            num = float(x)
        #replacing the df's element with num
        data['Followers'][i] = num
    #finding the frequence of each artist and sorting the series
    count = data.groupby('Artist').size().sort_values(0, ascending=False)
    Dict = {}
    #getting only the top 35 artists
    try:
        for i in range (0 , 35):
            artistName = count.index[i]
            indexOfFollowers = data[data['Artist'] == artistName].index[0]
            #using artist name as key and num of followers as value in a hashmap
            Dict[artistName] = data["Followers"][indexOfFollowers]
    except:
        print("you dont have enough artist you can change this on line 45")
    #saving artistFreq to csv
    csv = count
    csv.to_frame().to_csv('artistFreq.csv')
    return Dict

#seperating the dictionary by follower count
def seperateDict(Dict):
    one = []
    two = []
    three = []
    four = []
    five = []
    six = []
    seven = []
    eight = []
    #iterating through dictionary and comparing the value, while adding it to the corresponding list
    for key in Dict.keys() :
        value = Dict[key]
        if value >= 5000000:
            one.append(key)
        elif value >= 1000000:
            two.append(key)
        elif value >= 500000:
            three.append(key)
        elif value >= 100000:
            four.append(key)
        elif value >= 50000:
            five.append(key)
        elif value >= 10000:
            six.append(key)
        elif value >= 1000:
            seven.append(key)
        else:
            eight.append(key)
    #combinding all lists into a 2D array 
    seperated = [one , two , three , four , five , six , seven , eight]
    return seperated


pygame.init()

#defining window size, caption, background, font and other parameters
size = (900, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Souncloud Iceburgify")
done = False
clock = pygame.time.Clock()
bg = pygame.image.load("Iceburgify.Jpg")
bg = pygame.transform.scale(bg,size)
seperated = seperateDict(createDict())
font = pygame.font.Font('freesansbold.ttf', 20)

while not done:
    #drawing background
    screen.blit(bg,(0,0))
    #drawing the lines
    for i in range (0 , 7) :
        pygame.draw.line(screen,RED, (0,60 + i*80), (size[0], 60 + i*80))
    #text should alternate between being display up or down 
    up = True
    for i in range (0 , len(seperated)):
        for j in range (0 , len(seperated[i])):
            #only displays first 7 
            if (j < 7) :
                #display artist name
                text = font.render(seperated[i][j], True, RED)
                textRect = text.get_rect()
                if (up):
                    textRect.center = (90 + j * 125 , 30 + i*80)
                    up = False
                else :
                    textRect.center = (90 + j * 125 , 5 + i*80)
                    up = True
                screen.blit(text, textRect)
    #allowing user to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()