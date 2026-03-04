import os

searchTerms = []

def checkFile(path, detailedOutput, totalContains):
    detailedContains = []
    contains = False
    if (detailedOutput):
        for i in range(len(searchTerms)):
            detailedContains.append(0)
    try:
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as file:
            for line in file:
                stripped = line.strip().lower()
                for i in range(len(searchTerms)):
                    term = searchTerms[i]
                    if term in stripped:
                        if (not contains):
                            totalContains += 1
                        contains = True
                        if (detailedOutput):
                            if (detailedContains[i] == 0):
                                print(f"Search term \"{term}\" discovered in file {path}.")
                            detailedContains[i] += stripped.count(term)
                        else:
                            break
                if (contains and not detailedOutput):
                    print(f"Search terms discovered in file {path}. Take action as needed.")
                    return True, totalContains
            file.close()
            if (not contains):
                print(f"File {path} is clean!")

            if (detailedOutput):
                return detailedContains, totalContains
            else:
                return contains, totalContains
    except ValueError:
        print("File invalid.")
        return None, totalContains
    except IOError:
        print("File unable to be read.")
    
def printResult(files, contains, detailedOutput, fileCount, totalContains):
    print(str(fileCount) + " files discovered (" + str(totalContains) + " requiring action).")
    if (len(files) == len(contains)):
        for i in range(len(files)):
            if (detailedOutput):
                if (len(searchTerms) == len(contains[i])):
                    for j in range(len(searchTerms)):
                        if (contains[i][j]):
                            print(f"Search term \"{searchTerms[j]}\" found in file {files[i]} {contains[i][j]} times.")
                else:
                    print("Error: Operation did not cover all search terms.")
            else:
                if (contains[i]):
                    print(f"Search terms discovered in file {files[i]}. Take action as needed.")
    else:
        print("Error: Operation did not cover all files in directory.")


def main():
    detailedOutput = False
    print("Current working directory: ", os.getcwd())
    root = ""
    pathExists = False
    while (not pathExists):
        folderName = input("Please input the path of the folder to search.\n")
        if (os.path.exists(folderName)):
            pathExists = True

            root = os.path.abspath(folderName)
            print("Root directory: " + root)
        else:
            print("You silly, that path doesn't exist!")
    
    exitTrigger = False
    while (not exitTrigger):
        userInput = input("Please input any terms you would like to search files for. Press ENTER when finished.\n").lower()
        if (userInput):
            if (not (userInput in searchTerms)):
                searchTerms.append(userInput)
            else:
                print("You have already added this search term.")
        elif (len(searchTerms) > 0):
            print("Thank you!")
            print("Terms: " + str(searchTerms))
            exitTrigger = True

    exitTrigger = False
    while (not exitTrigger):
        userInput = input("Turn on detailed output? y/n\n")
        if (userInput == "y" or userInput == "Y"):
            detailedOutput = True
            exitTrigger = True
        elif (userInput == "n" or userInput == "N"):
            exitTrigger = True
    
    finished = False
    while (not finished):
        allFiles = []
        globalContains = []
        fileCount = 0
        totalContains = 0
        for subdir, dirs, files in os.walk(root):
            for file in files:
                fileCount += 1
                allFiles.append(os.path.join(subdir, file))
                contains, totalContains = checkFile(os.path.join(subdir, file), detailedOutput, totalContains)
                globalContains.append(contains)
        
        printResult(allFiles, globalContains, detailedOutput, fileCount, totalContains)
        exitTrigger = False
        while (not exitTrigger):
            userInput = input("Would you like to run the program again using the same settings? y/n\n")
            if (userInput == "y" or userInput == "Y"):
                exitTrigger = True
            elif (userInput == "n" or userInput == "N"):
                finished = True
                exitTrigger = True
    print("Finished. Thank you for using Thorax Hembleecker's Certified Awesome Data Sanitizing Assistant!")

if __name__ == "__main__":
    main()