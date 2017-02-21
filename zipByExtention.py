# !python3 

'''Program that ask user which type of files he wants to archive (by extention), ask for path and go through this path looking for every file with these extentions. Also user should denote if he wants to archive files with these extentions of all other files except files with these extentions'''

import os, shutil, zipfile

#def askUserExt():

#def lookingForFiles(path):

#def addExt(filepath):

#def addWithoutExt(filepath)

logFile = open('D:\\YandexDisk\\Studies\\Python\\Chapter 9\\zipByExtention\\logZipByExtention.txt', 'w')

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
		print('There is no such directory. Try again.')	
		logFile.write('There is no such directory. Try again.\n')	


############# ask user about which files he wants to zip #############

while True:
	answer1 = input('Would you like (1) to zip file with certanin extentions or (2) to zip all files except files with certain extention? Your answer is: ')
	logFIle.write('Would you like (1) to zip file with certanin extentions or (2) to zip all files except files with certain extention? Your answer is: ')
	if answer1 == '1':
		#add extentions
		#zip certain extentions
		break
	elif answer1 == '2':
		#add extentions
		#zip files except files with this extention
		break
	else:
		print('Input error. You should type only 1 or 2. Try again.')
		continue	


logFile.close()	