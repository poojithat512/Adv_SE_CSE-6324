import os
import json
from ast import literal_eval

# Uncomment the print statements for desired UI Components.
# Do change the directory name containing JSON files, before running.
def recursivelyFindChildren(prechild):
    bound = prechild['bounds']  # bounds of each component

    # Give four coordinate x,y,width, height
    elemenTopx = bound[0]
    elementTopY = bound[1]
    elementWidth = bound[2]
    elementHeight = bound[3]

    elementText = "null"
    if 'text' in prechild:
        elementText = prechild['text']
        # print(bound,elementText) #print components with text attributes

    elementID = "null"
    if 'resource-id' in prechild:
        elementID = prechild['resource-id']  # check if resource-id is present for the component
    # print(bound,elementID) #print component bounds and id

    if 'clickable' in prechild:
        elementClickable = prechild['clickable']  # check if components are clickable
        print(bound, elementClickable)

    if 'children' in prechild:
        childrens = prechild['children'] # check if nested children exists.

        for child in childrens:  # iterate through all the nested children in a json file

            recursivelyFindChildren(child)

    return


def readJson(filename):  # read json file
    try:

        with open(filename) as f:
            outDict = json.load(f)  # load a json file in python dictionary

            bound = outDict['activity']['root']['bounds'] # accessing the bound of the root

            x = bound[0]
            y = bound[1]

            childrens = outDict['activity']['root']['children']  # point to the first children

            for child in childrens:
                recursivelyFindChildren(child)
    except:

        pass

    return


readJson("C:/Users/Poojitha Thota/Desktop/MINE/MASTERS/FALL_2021/Adv_SE/Adv_SE_project/Iteration_1/combined/8.json")