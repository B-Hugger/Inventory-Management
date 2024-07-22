import os
import csv
#file to 2d array:
folderPath = r'/workspaces/Inventory-Management/Invertory'
def getdir(dir):
    fileNames = os.listdir(dir)
    fileNameList = []

    for fileName in fileNames:
        # splits filename and extension then retreives filename without extension
        fileName = fileName.split(".")[0]
        # remove all extensions

        # Split the file name by '_' and append the components to the inner list
        components = fileName.split('_')
        fileNameList.append(components)

    return fileNameList


list = getdir(folderPath)
print(list)

#2d array to csv file
def ArrayToCSV(array):
    with open("inventory.csv", "w+", newline = '') as csv_file:
        csv_rw = csv.writer(csv_file)
        rows = array
        csv_rw.writerows(array)
#Test output
ArrayToCSV(list)



