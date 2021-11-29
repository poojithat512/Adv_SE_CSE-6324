#!/usr/bin/env python
# coding: utf-8

# In[47]:


import collections
import cv2 as cv
import numpy as np
import PIL
from sklearn.cluster import KMeans
import json
from PIL import Image
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
from collections import Counter

textStyle = ""
textDict = {}

listofstyle = []
listofimage = []
count = 0
classcount = 0
filepath = r'D:\Fall 2021\CSE 6324\unique_uis\combined\\' # filepath for JSON and JPG file folder
filename = '618'  # name of json and jpg file
imagefilename = 'folder' + filename
im = Image.open(filepath + filename + '.jpg')
imagefolder = r'D:\React Native\my-project\Cropped_images\\'  # folder for saving cropped images

path = os.path.join(imagefolder, imagefilename)  # create image separate folder for each file
if not os.path.exists(path):
    os.mkdir(path)
    
clt = KMeans(n_clusters=3) #cluster size for KMEANS algorithm

img = cv.imread(filepath + filename + '.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

backgroundColor = ""
fontColor = ""
dominantColor = []
secondDominantColor = []


# In[48]:


#extract background and font color from image

def palette_perc(k_cluster):
    global backgroundColor
    global fontColor
    global dominantColor
    global secondDominantColor
    width = 300
    palette = np.zeros((50, width, 3), np.uint8)

    n_pixels = len(k_cluster.labels_)
    counter = Counter(k_cluster.labels_)  # count how many pixels per cluster
    perc = {}
    for i in counter:
        perc[i] = np.round(counter[i] / n_pixels, 2)
    perc = dict(sorted(perc.items()))

    dicts = {}

    for idx, centers in enumerate(k_cluster.cluster_centers_):
        dicts[perc[idx]] = centers
    od = collections.OrderedDict(sorted(dicts.items()))
    key = []
    for i in od:
        key.append(i)
        print(i, od[i])

    dominantColor = od[key[2]] #background color 
    secondDominantColor = od[key[1]]  #font-color

    step = 0

    for idx, centers in enumerate(k_cluster.cluster_centers_):
        palette[:, step:int(step + perc[idx] * width + 1), :] = centers
        step += int(perc[idx] * width + 1)

    return palette


# In[49]:


clt_1 = clt.fit(img.reshape(-1, 3))
palette_perc(clt_1)

#convert rgb to hex codes for colors
def rgb_to_hex(r, g, b):
    return ('{:X}{:X}{:X}').format(r, g, b)


backgroundColor = (rgb_to_hex(int(dominantColor[0]), int(dominantColor[1]), int(dominantColor[2])))
fontColor = (rgb_to_hex(int(secondDominantColor[0]), int(secondDominantColor[1]), int(secondDominantColor[2])))


# In[51]:


#visit each children in json file
def recursivelyFindChildren(prechild):
    global count
    count = count + 1
    global textStyle
    global textDict
    global listofstyle
    global listofimage
    global classcount
    text_bckgrnd = ""
    global fontColor
    elementID = "null"
    if 'resource-id' in prechild:
        elementID = prechild['resource-id']  # check if resource-id is present for the component

    rel_bound = prechild['rel-bounds']  # bounds of each component
    bound = prechild['bounds']

    # Give four coordinate x,y,width, height
    elementTopx = rel_bound[0]
    elementTopY = rel_bound[1]
    elementWidth = rel_bound[2]
    elementHeight = rel_bound[3]
    view_start_tag = '<View style={{position: \'absolute\', width: ' + str(
        (prechild['bounds'][2] - prechild['bounds'][0]) / 1440) + '*windowWidth, height: ' + str(
        (prechild['bounds'][3] - prechild['bounds'][1]) / 2560) + '*windowHeight,left: 0, top: 0}}>'
    view_end_tag = '</View>\n'  # add ui positions key-value pairs for stylesheet

    listofstyle.append({'left': elementTopx, 'top': elementTopY, 'width': elementWidth, 'height': elementHeight});

    # add <View> elements to React Native code
    textStyle = textStyle + "<View style={styles.Children" + str(count - 1) + "}>\n"

    elementText = "null"

    # print(bound,elementClickable)
    if 'class' in prechild:
        elementClass = prechild['class']
        classcount = classcount + 1

        # add <CheckBox> to React Native code
        if 'CheckBox' in elementClass:
            textStyle = textStyle + view_start_tag + '<CheckBox style={{color:\'green\',top:0,left:0}}/>\n'
            if 'text' in prechild:
                elementText = prechild['text']
                textStyle = textStyle + view_start_tag + '<Text style={{position: \'relative\',color: \'#' + fontColor + '\',  fontSize: 50,width: ' + str(
                    (prechild['rel-bounds'][2] - prechild['rel-bounds'][0]) / 1440) + '*windowWidth, height: ' + str((
                                                                                                                                 prechild[
                                                                                                                                     'rel-bounds'][
                                                                                                                                     3] -
                                                                                                                                 prechild[
                                                                                                                                     'rel-bounds'][
                                                                                                                                     1]) / 2560) + '*windowHeight,left: 0, top: 0}}>' + elementText + '</Text>'
                textStyle = textStyle + view_end_tag
            textStyle = textStyle + view_end_tag
        # add <Switch> to React Native code
        if 'Switch' in elementClass:
            textStyle = textStyle + view_start_tag + '<Switch style={{ position: \'absolute\' ,top: ' + str(
                prechild['rel-bounds'][1] / 2560) + '*windowHeight}}/>\n'
            textStyle = textStyle + view_end_tag
        # add <Text> to React Native code
        if 'TextView' in elementClass:
            elementText = prechild['text']

            textStyle = textStyle + view_start_tag + '<Text style={{position: \'absolute\',color: \'#' + fontColor + '\',width: ' + str(
                (prechild['rel-bounds'][2] - prechild['rel-bounds'][0]) / 1440) + '*windowWidth, height: ' + str((
                                                                                                                             prechild[
                                                                                                                                 'rel-bounds'][
                                                                                                                                 3] -
                                                                                                                             prechild[
                                                                                                                                 'rel-bounds'][
                                                                                                                                 1]) / 2560) + '*windowHeight,left: 0, top: 0}}>' + elementText + '</Text>'
            textStyle = textStyle + view_end_tag
        # add <TextInput> to React Native code
        if 'EditText' in elementClass:
            if 'text-hint' in prechild:
                hint = prechild['text-hint']
                textStyle =  textStyle + view_start_tag + '<TextInput underlineColorAndroid = "black" placeholder=\'' + hint + '\' style = {{height: 40, borderColor: \'black\', borderWidth: 1}} />\n'
                textStyle = textStyle + view_end_tag
        # add <Button> to React Native code
        if 'Button' in elementClass and 'ImageButton' not in elementClass:
            if 'text' in prechild:
                title = prechild['text']
                textStyle = textStyle + view_start_tag
                textStyle = textStyle + '<Button title=\'' + title + '\' onPress={() => Alert.alert(\'Button pressed\')}/>'
                textStyle = textStyle + view_end_tag

        # add <TouchableOpacity> to React Native code
        if 'ImageButton' in elementClass:
            try:
                im1 = im.crop((bound[0] / 1440 * im.size[0], bound[1] / 2560 * im.size[1], bound[2] / 1440 * im.size[0],
                               bound[3] / 2560 * im.size[1]))
                # print((bound[0]/1440*1080, bound[1]/2560*1920, bound[2]/1440*1080, bound[3]/2560*1920))
                im1.save(path + '\\' + 'image' + str(count) + '.png')
                listofimage.append(
                    {'image' + str(count): './Cropped_images/' + imagefilename + '/image' + str(count) + '.png'})
                textStyle = textStyle + '<TouchableOpacity activeOpacity={0.5} onPress={() => Alert.alert(\'Button pressed\')}><Image style={{position: \'relative\', width: ' + str(
                    (prechild['rel-bounds'][2] - prechild['rel-bounds'][0]) / 1440) + '*windowWidth, height: ' + str((                                                                                                                             prechild[
                                                                                                                                     'rel-bounds'][
                                                                                                                                     3] -
                                                                                                                                 prechild[
                                                                                                                                     'rel-bounds'][
                                                                                                                                     1]) / 2560) + '*windowHeight,left: 0, top: 0}}\n resizeMode= \'contain\'\n source={image' + str(
            count) + '}/></TouchableOpacity>\n'
            except:
                print("An exception occurred")
        # add <Image> to React Native code
        if 'ImageView' in elementClass:
            try:
                im1 = im.crop((bound[0] / 1440 * im.size[0], bound[1] / 2560 * im.size[1], bound[2] / 1440 * im.size[0],
                               bound[3] / 2560 * im.size[1]))
                # print(bound)
                # print((bound[0]/1440*im.size[0],bound[1]/2560*im.size[1],bound[2]/1440*im.size[0], bound[3]/2560*im.size[1]))
                im1.save(path + '\\' + 'image' + str(count) + '.png')
                listofimage.append(
                    {'image' + str(count): './Cropped_images/' + imagefilename + '/image' + str(count) + '.png'})
                textStyle = textStyle + view_start_tag + '<Image\n style={{position: \'absolute\',width: ' + str(
                    (rel_bound[2] - rel_bound[0]) / 1440) + '*windowWidth, height: ' + str(
                    (rel_bound[3] - rel_bound[1]) / 2560) + '*windowHeight,left: 0, top: 0}}\n resizeMode= \'contain\'\n source={image' + str(
                    count) + '}/>\n'
                textStyle = textStyle + view_end_tag

            except:
                print("An exception occurred")

    textDict[elementID] = [elementText]

    if 'children' in prechild:
        childrens = prechild['children']

        for child in childrens:  # iterate through all the nested children in a json file

            recursivelyFindChildren(child)
            textStyle = textStyle + "\n</View>"  # end of each View element
    # textStyle=textStyle+"\n</View>"

    return


# In[52]:



def readJson(filename):  # read json file
    global textStyle
    global count
    try:

        with open(filename) as f:
            outDict = json.load(f)  # load a json file in python dictionary

            bound = outDict['activity']['root']['bounds']

            x = bound[0]
            y = bound[1]

            childrens = outDict['activity']['root']['children']  # point to the first children

            for child in childrens:
                recursivelyFindChildren(child)
                textStyle = textStyle + "\n</View>"  # end of Root View element
            # textStyle=textStyle+"\n</View>"
    except:

        pass
    print(count)

    return


readJson(filepath + filename + '.json')


# In[ ]:


styletext = ""


# create StyleSheet for each View element
def createStyleSheet():
    global listofstyle
    global styletext

    styletext = "const styles = StyleSheet.create({\n"

    # extract UI bounds for each View and add to stylesheet

    for index in range(len(listofstyle)):
        styletext = styletext + 'Children' + str(index) + ': { position:\'absolute\',\n'
        for key in listofstyle[index]:
            if (key == 'top' or key == 'height'):
                styletext = styletext + key + ": " + str(listofstyle[index][key] / 2560) + '*windowHeight'
            else:
                styletext = styletext + key + ": " + str(listofstyle[index][key] / 1440) + '*windowWidth'

            styletext = styletext + ",\n"

        if (index != len(listofstyle) - 1):
            styletext = styletext + "},\n"
        else:
            styletext = styletext + "}\n})"


createStyleSheet()


# In[91]:


# create the react native code by adding elements and stylesheet

def createReactCode():
    global textStyle
    global count
    global listofimage
    global backgroundColor
    reactCode = "import React, { Component,useState } from \"react\";\n"
    reactCode = reactCode + "import {\n  StyleSheet,\nSwitch,\n  Text,\n Button, \nAlert,\n View,\n  TouchableOpacity,\n  TextInput,\n CheckBox,\n  ScrollView,\n  Image,\n  PixelRatio,\n  Dimensions\n} from \"react-native\";\n\n"
    for index in range(len(listofimage)):
        for key in listofimage[index]:
            reactCode = reactCode + "import " + key + " from " + "\'" + str(listofimage[index][key]) + '\';\n'

    # reactCode=reactCode+"import Logo from './logo.png';\n" #a sample image in the react native project folder

    reactCode = reactCode + "const windowWidth = Dimensions.get(\"window\").width;\nconst windowHeight = Dimensions.get(\"window\").height;\n"
    reactCode = reactCode + "export default class Main extends Component {\nrender(){\nreturn (\n\t<View\n\tstyle={{\n\tposition:\"absolute\",\n\twidth: windowWidth,\n\theight: windowHeight,\n\ttop: 0.0,\n\tleft: 0.0,backgroundColor:\'#" + backgroundColor + "\'\n}}>\n"
    reactCode = reactCode + textStyle + "</View>\n);\n}\n}\n\n" + styletext

    f = open(r'D:\React Native\my-project\\'+'App.js', "w")  # path for saving React Native Code
    f.write(reactCode)
    f.close()
    return reactCode


createReactCode();

import socketserver

#show the generated code in localhost
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', "text/plain")
        self.end_headers()
        message = createReactCode()
        self.wfile.write(bytes(message, "utf8"))
with socketserver.TCPServer(("", 8080), handler) as httpd:
    print("serving at port", 8080)
    httpd.serve_forever()


# In[ ]:




