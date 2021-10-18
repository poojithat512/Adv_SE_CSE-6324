#!/usr/bin/env python
# coding: utf-8

import os
import json


textStyle=""
textDict={}

listofstyle=[]
count=0

#iterate through each view and add relative components for react Native Code
def recursivelyFindChildren(prechild):
    global count
    count=count+1
    global textStyle
    global textDict   
    global listofstyle
    
    
    elementID="null"    
    if 'resource-id' in prechild:
        elementID = prechild['resource-id'] #check if resource-id is present for the component
    
   
    bound = prechild['rel-bounds']   #bounds of each component   
   
    # Give four coordinate x,y,width, height
    elementTopx = bound[0]
    elementTopY = bound[1]
    elementWidth = bound[2]
    elementHeight = bound[3]   
    
    #add ui positions key-value pairs for stylesheet
    listofstyle.append({'left':elementTopx,'top':elementTopY,'width':elementWidth,'height':elementHeight});
   
    # add <View> elements to React Native code
    textStyle=textStyle+"<View style={styles.Children"+str(count-1)+"}>\n"
    
    elementText="null"
    if 'text' in prechild:
        elementText = prechild['text']
        textStyle=textStyle+"<Text>"+elementText+"</Text>"  # add <Text> elements to React Native code
    
        #print(bound,elementClickable)
    if 'class' in prechild:
        elementClass= prechild['class']
        if 'ImageView' in elementClass:
            
            # add <Image> elements to React Native code
            textStyle=textStyle+'<Image\n style={{width: '+str(prechild['rel-bounds'][2]/1440)+'*windowWidth, height: '+str(prechild['rel-bounds'][3]/2560)+'*windowHeight}}\nsource={Logo}/>\n'
            
    
    textDict[elementID]=[elementText]
       
    if 'children' in prechild:
        childrens = prechild['children'] 
        
        for child in childrens:         #iterate through all the nested children in a json file
            
            recursivelyFindChildren(child)  
            textStyle=textStyle+"\n</View>" #end of each View element
           
    
    return 




def readJson(filename): #read json file
    global textStyle
    try:
        
        with open(filename) as f:      
            outDict = json.load(f) #load a json file in python dictionary
                   
            bound = outDict['activity']['root']['bounds'] 
            
            x = bound[0]
            y = bound[1]
         
            childrens = outDict['activity']['root']['children'] #point to the first children
            
            
            for child in childrens:
                
                recursivelyFindChildren(child)
                textStyle=textStyle+"\n</View>" #end of Root View element       
                
    except:
        
        pass  
   
    return
    
filepath=r'D:\Fall 2021\CSE 6324\unique_uis\combined\\' #filepath for JSON file folder
filename='7'  #name of json file
readJson(filepath+filename+'.json')


styletext=""

#create StyleSheet for each View element
def createStyleSheet():
    global listofstyle
    global styletext
    styletext= "const styles = StyleSheet.create({\n"
    
    #extract UI bounds for each View and add to stylesheet
    
    for index in range(len(listofstyle)):
        styletext=styletext+'Children'+str(index)+': { position:\'absolute\',\n'
        for key in listofstyle[index]:
            if(key=='top' or key=='height'):
                styletext=styletext+key+": "+str(listofstyle[index][key]/2560)+'*windowHeight'
            else:
                styletext=styletext+key+": "+str(listofstyle[index][key]/1440)+'*windowWidth'
                
            styletext=styletext+",\n"
            
        if(index!=len(listofstyle)-1):
           styletext=styletext+"},\n"
        else:
           styletext=styletext+"}\n})"
            
       
createStyleSheet()


#create the react native code by adding elements and stylesheet

def createReactCode():
    global textStyle
    reactCode="import React, { Component } from \"react\";\n"
    reactCode=reactCode+"import {\n  StyleSheet,\n  Text,\n  View,\n  TouchableOpacity,\n  TextInput,\n  ScrollView,\n  Image,\n  PixelRatio,\n  Dimensions\n} from \"react-native\";\n\n"
    
    reactCode=reactCode+"import Logo from './logo.png';\n" #a sample image in the react native project folder
    
    reactCode=reactCode+"const windowWidth = Dimensions.get(\"window\").width;\nconst windowHeight = Dimensions.get(\"window\").height;\n"
    reactCode=reactCode+"export default class Main extends Component {\nrender(){\nreturn (\n\t<View\n\tstyle={{\n\tposition:\"absolute\",\n\twidth: windowWidth,\n\theight: windowHeight,\n\ttop: 0.0,\n\tleft: 0.0,\n\tbackgroundColor: \"#5CC5F8\",\n}}>\n"
    reactCode=reactCode+textStyle+"</View>\n);\n}\n}\n\n"+styletext

    f = open(r'D:\Fall 2021\CSE 6324\ReactCode\\'+filename+'ReactNative.js', "w") #path for saving React Native Code
    f.write(reactCode)
    f.close()

    
createReactCode();   





