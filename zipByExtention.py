# !python3 

'''Program that ask user which type of files he wants to archive (by extention), ask for path and go through this path looking for every file with these extentions. Also user should denote if he wants to archive files with these extentions of all other files except files with these extentions'''

import os, re, shutil, sys, zipfile

#def lookingForFiles(path):

#def askWithExt():

#def addWithoutExt():

#def statistics():

#def zipFiles():


def addExt():
	answer2 = ''
	extList = []
	while True:
		answer2 = input('\nType here an extention.\nWhen you are done, type "d" and press enter.\nIf you want to exit, type "e" and press enter: ')
		if answer2 == 'd' and len(extList) > 1:
			print('Thank you. Start to sort files out')
			break
		elif answer2 == 'd' and len(extList) <= 0:
			print('You didn\'t add any extesntion. Please add at least one or press "exit" to exit')
			continue
		elif re.search(r'^\w{2,4}$', answer2) != None:
			extList.append(answer2)
			print('Extention ' + answer2 + ' was added. There are these extention to look for now: ')
			for i in extList:
				print('- ' + i)
			continue
		elif answer2 == 'e':
			print('Goodbye')
			sys.exit()	
		else:
			print('\n' + answer2 + ' it is not appropriate extention or command. Try again.')	



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
	logFile.write('Would you like (1) to zip file with certain extentions or (2) to zip all files except files with these extentions? Your answer is: ')
	if answer1 == '1':
		extList = addExt()
		#return all files from path - return list with path to these files
		#add to list only file with users' extentions
		#print some statistics of number and size of files
		#put files in archive
		break
	elif answer1 == '2':
		extList = addExt()
		#return files from path
		#add to list all files except from these with users' extentions - return list with path to these files
		#print some statistics of number and size of files
		#put files in archive
		break
	else:
		print('Input error. You should type only 1 or 2. Try again.')
		continue	


logFile.close()	

#(\.\w{2,4})