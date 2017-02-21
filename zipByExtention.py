# !python3 

'''Program that ask user which type of files he wants to archive (by extention), ask for path and go through this path looking for every file with these extentions. Also user should denote if he wants to archive files with these extentions of all other files except files with these extentions'''

import os, re, shutil, sys, zipfile

def lookingForFiles(pathToSearch):
	logFile.write('There are these files in:\n' + pathToSearch + '\n')
	allFiles = []
	for folderName, subfolders, fileNames in os.walk(pathToSearch):
		for file in fileNames:
			if file.startswith('~$'):
				continue
			else:
				allFiles.append(os.path.join(folderName, file))
				logFile.write(os.path.join(folderName, file) + '\n')
			
	return allFiles

def sortWithExt(allFiles, extList):
	logFile.write('\nStart to sort out files with urers\' extentions\n')
	filesWithExt = []
	for file in allFiles:
		if file.endswith(extList):
			filesWithExt.append(file)

	for item in filesWithExt:
		logFile.write(item + '\n')		

#def addWithoutExt():

#def statistics():

#def zipFiles():


def addExt():
	answer2 = ''
	extList = []
	while True:
		answer2 = input('\nType here an extention.\nWhen you are done, type "d" and press enter.\nIf you want to exit, type "e" and press enter: ')
		logFile.write('Ask user for extention or a command.\n')
		if answer2 == 'd' and len(extList) > 0:
			print('Thank you. Start to sort files out')
			logFile.write('User done to add extentions. List of extentions containts ' + str(len(extList)) + ' items.')
			break
		elif answer2 == 'd' and len(extList) <= 0:
			print('You didn\'t add any extesntion. Please add at least one or press "exit" to exit')
			logFile.write('User press "d" but list of extentions is empty\n' )
			continue
		elif re.search(r'^\w{2,4}$', answer2) != None:
			extList.append(answer2)
			print('Extention ' + answer2 + ' was added. There are these extention to look for now: ')
			logFile.write('Extention ' + answer2 + ' was added. There are these extention to look for now: \n')
			for i in extList:
				print('- ' + i)
				logFile.write('- ' + i + '\n')
			continue
		elif answer2 == 'e':
			print('Goodbye')
			logFile.write('User press "e". Program is going to shut down.\n')
			logFile.close()
			sys.exit()	
		else:
			print('\n' + answer2 + ' is not appropriate extention or command. Try again.')
			logFile.write('Got an appropriate answer: ' + answer2 + '\n')
			continue

	return tuple(extList)

logFile = open('D:\\logZipByExtention.txt', 'w')

logFile.write('Program has started.\n')

########## ask user about path to work and check it #####################

while True:
	logFile.write('Type in path to directory to zip: \n')
	pathToSearch = input('Type in path to directory to zip: \n')
	if os.path.exists(pathToSearch):
		if os.path.isdir(pathToSearch):
			print('Ok, this directory exists.\n')
			logFile.write('Path to direcory to zip accepted: \n' + pathToSearch + '\n')
			break
		else:
			print('It should be folder, not a file.\n')	
			logFile.write('It should be folder, not a file.\n')	
			continue
	else:
		print('There is no such directory. Try again.\n')	
		logFile.write('There is no such directory. Try again.\n')	


############# ask user about which files he wants to zip #############

while True:
	answer1 = input('Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: ')
	logFile.write('Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: \n')
	if answer1 == '1':
		extList = addExt()
		allFiles = lookingForFiles(pathToSearch)
		filesWithExt = sortWithExt(allFiles, extList)
		#return all files from path - return list with path to these files
		#add to list only file with users' extentions
		#print some statistics of number and size of files
		#put files in archive
		break
	elif answer1 == '2':
		extList = addExt()
		allFiles = lookingForFiles(pathToSearch)
		#add to list all files except from these with users' extentions - return list with path to these files
		#print some statistics of number and size of files
		#put files in archive
		break
	else:
		print('Input error. You should type only 1 or 2. Try again.')
		continue	


logFile.close()	

#(\.\w{2,4})