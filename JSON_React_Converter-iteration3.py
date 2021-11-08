#!/usr/bin/env python
# coding: utf-8




import os
import json
from PIL import Image

textStyle=""
textDict={}

listofstyle=[]
listofimage=[]
count=0
filepath=r'D:\Fall 2021\CSE 6324\unique_uis\combined\\' #filepath for JSON and JPG file folder
filename='8'  #name of json and jpg file
imagefilename='folder'+filename
im = Image.open(filepath+filename+'.jpg')
imagefolder=r'D:\React Native\my-project\Cropped_images\\' #folder for saving cropped images

path=os.path.join(imagefolder,imagefilename) #create image separate folder for each file
if not os.path.exists(path):
    os.mkdir(path)
    
#iterate through each view and add relative components for react Native Code
def recursivelyFindChildren(prechild):
    global count
    count=count+1
    global textStyle
    global textDict   
    global listofstyle
    global listofimage
    
    elementID="null"    
    if 'resource-id' in prechild:
        elementID = prechild['resource-id'] #check if resource-id is present for the component
    
   
    rel_bound = prechild['rel-bounds']   #bounds of each component   
    bound = prechild['bounds']
    
    # Give four coordinate x,y,width, height
    elementTopx = rel_bound[0]
    elementTopY = rel_bound[1]
    elementWidth = rel_bound[2]
    elementHeight = rel_bound[3]   
    
    #add ui positions key-value pairs for stylesheet
    listofstyle.append({'left':elementTopx,'top':elementTopY,'width':elementWidth,'height':elementHeight});
   
    # add <View> elements to React Native code
    textStyle=textStyle+"<View style={styles.Children"+str(count-1)+"}>\n"
    
    elementText="null"

    
    #print(bound,elementClickable)
    if 'class' in prechild:
        elementClass= prechild['class']
        
        # add <CheckBox> to React Native code
        if 'CheckBox' in elementClass:
            textStyle=textStyle+'<CheckBox style={{color:\'green\',top:0,left:0}}/>\n'
            if 'text' in prechild:
                elementText = prechild['text']
                textStyle=textStyle+'<Text style={{position: \'relative\',width: '+str((prechild['rel-bounds'][2]-prechild['rel-bounds'][0])/1440)+'*windowWidth, height: '+str((prechild['rel-bounds'][3]-prechild['rel-bounds'][1])/2560)+'*windowHeight,left: 0, top: 0}}>'+elementText+'</Text>'
        
        # add <Switch> to React Native code
        if 'Switch' in elementClass:
            textStyle=textStyle+'<Switch style={{ position: \'absolute\' ,top: '+str(prechild['rel-bounds'][1]/2560)+'*windowHeight}}/>\n'

        # add <Text> to React Native code
        if 'TextView' in elementClass:
            elementText = prechild['text']
            textStyle=textStyle+'<Text style={{position: \'absolute\',top: '+str(prechild['rel-bounds'][1]/2560)+'*windowHeight,width: '+str((prechild['rel-bounds'][2]-prechild['rel-bounds'][0])/1440)+'*windowWidth, height: '+str((prechild['rel-bounds'][3]-prechild['rel-bounds'][1])/2560)+'*windowHeight,left: 0, top: 0}}>'+elementText+'</Text>'
        
        # add <TextInput> to React Native code
        if 'EditText' in elementClass:
            if 'text-hint' in prechild:
                hint=prechild['text-hint']
                textStyle=textStyle+'<TextInput underlineColorAndroid = "black" placeholder=\''+hint+'\' />\n'
        
        # add <Button> to React Native code
        if 'Button' in elementClass and 'ImageButton' not in elementClass:
            if 'text' in prechild:
                title=prechild['text']
                textStyle=textStyle+'<View style={{position: \'relative\', width: '+str((prechild['rel-bounds'][2]-prechild['rel-bounds'][0])/1440)+'*windowWidth, height: '+str((prechild['rel-bounds'][3]-prechild['rel-bounds'][1])/2560)+'*windowHeight,left: 0, top: 0}}>'
                textStyle=textStyle+'<Button title=\''+title+'\' onPress={() => Alert.alert(\'Button pressed\')}/>'
                textStyle=textStyle+'</View>\n'
        
        # add <TouchableOpacity> to React Native code
        if 'ImageButton' in elementClass:
            im1 = im.crop((bound[0]/1440*1080, bound[1]/2560*1920, bound[2]/1440*1080, bound[3]/2560*1920))

            im1.save(path+'\\'+'image'+str(count)+'.png')
            listofimage.append({'image'+str(count):'./Cropped_images/'+imagefilename+'/image'+str(count)+'.png'})
            textStyle=textStyle+'<TouchableOpacity activeOpacity={0.5} onPress={() => Alert.alert(\'Button pressed\')}><Image style={{position: \'relative\', width: '+str((prechild['rel-bounds'][2]-prechild['rel-bounds'][0])/1440)+'*windowWidth, height: '+str((prechild['rel-bounds'][3]-prechild['rel-bounds'][1])/2560)+'*windowHeight,left: 0, top: 0}}\nsource={image'+str(count)+'}/></TouchableOpacity>\n'
        
        # add <Image> to React Native code
        if 'ImageView' in elementClass :
            
            im1 = im.crop((bound[0]/1440*1080, bound[1]/2560*1920, bound[2]/1440*1080, bound[3]/2560*1920))

            im1.save(path+'\\'+'image'+str(count)+'.png')
            listofimage.append({'image'+str(count):'./Cropped_images/'+imagefilename+'/image'+str(count)+'.png'})
            textStyle=textStyle+'<Image\n style={{position: \'relative\',width: '+str((prechild['rel-bounds'][2]-prechild['rel-bounds'][0])/1440)+'*windowWidth, height: '+str((prechild['rel-bounds'][3]-prechild['rel-bounds'][1])/2560)+'*windowHeight,left: 0, top: 0}}\nsource={image'+str(count)+'}/>\n'
        
        
    textDict[elementID]=[elementText]
       
    if 'children' in prechild:
        childrens = prechild['children'] 
        
        for child in childrens:         #iterate through all the nested children in a json file
            
            recursivelyFindChildren(child)  
            textStyle=textStyle+"\n</View>" #end of each View element
           
    
    return 




def readJson(filename): #read json file
    global textStyle
    global count
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
    print(count)
   
    return
    

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
    global count
    global listofimage
    
    reactCode="import React, { Component,useState } from \"react\";\n"
    reactCode=reactCode+"import {\n  StyleSheet,\nSwitch,\n  Text,\n Button, \nAlert,\n View,\n  TouchableOpacity,\n  TextInput,\n CheckBox,\n  ScrollView,\n  Image,\n  PixelRatio,\n  Dimensions\n} from \"react-native\";\n\n"
    for index in range(len(listofimage)):
        for key in listofimage[index]:
            reactCode=reactCode+"import "+key+" from "+"\'"+str(listofimage[index][key])+'\';\n'
        
        
    #reactCode=reactCode+"import Logo from './logo.png';\n" #a sample image in the react native project folder
    
    reactCode=reactCode+"const windowWidth = Dimensions.get(\"window\").width;\nconst windowHeight = Dimensions.get(\"window\").height;\n"
    reactCode=reactCode+"export default class Main extends Component {\nrender(){\nreturn (\n\t<View\n\tstyle={{\n\tposition:\"absolute\",\n\twidth: windowWidth,\n\theight: windowHeight,\n\ttop: 0.0,\n\tleft: 0.0,\n}}>\n"
    reactCode=reactCode+textStyle+"</View>\n);\n}\n}\n\n"+styletext

    f = open(r'D:\React Native\my-project\\'+'App.js', "w") #path for saving React Native Code
    f.write(reactCode)
    f.close()
    

    
createReactCode();   






