# !python3 

'''Program that ask user which type of files he wants to archive (by extention), ask for path and go through this path looking for every file with these extentions. Also user should denote if he wants to archive files with these extentions of all other files except files with these extentions'''

import os, re, shutil, sys, zipfile

def lookingForFiles(pathToSearch):
	logFile.write('There are these files in:\n' + pathToSearch + '\n')
	allFiles = []
	totalSize = 0
	for folderName, subfolders, fileNames in os.walk(pathToSearch):
		filesNames = [f for f in fileNames if not f[0] == '.'] #create list that doesn't have hidden files
		subfolders[:] = [s for s in subfolders if not s[0] == '.'] #change list to exclude hidden folders

		for file in fileNames:
			if file.startswith('~$'):
				continue
			else:
				try:
					size = os.path.getsize(os.path.join(folderName, file))
				except FileNotFoundError:
					size = os.path.getsize(os.path.join('\\\\?\\' + folderName, file))
				totalSize += size
				allFiles.append(os.path.join(folderName, file))
				logFile.write(os.path.join(folderName, file) + '\n')

	#We need to use \\?\ before path that is more than 260 symbols
	#otherwise we get an error			

	print('There are ' + str(len(allFiles)) + ' files with total size of '	+ str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.\n')
	logFile.write('There are ' + str(len(allFiles)) + ' files with total size of '	+ str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.\n\n')
			
	return allFiles #list of all files including files in subfolders

def countAndPrintSorted(filesToCount, withOrWithoutWord):
	totalSize = 0

	for item in filesToCount:
		size = os.path.getsize(item)
		totalSize += size
		logFile.write(item + '\n')

	print('There are ' + str(len(filesToCount)) + ' files ' + withOrWithoutWord + ' your extentions with total size of ' + str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.\n')
	logFile.write('There are ' + str(len(filesToCount)) + ' files ' + withOrWithoutWord + ' your extentions with total size of ' + str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.\n\n')	

def addExt():
	answer2 = ''
	extList = []
	while True:
		answer2 = input('\nType here an extention.\nWhen you are done, type "d" and press enter.\nIf you want to exit, type "e" and press enter: ')
		logFile.write('Ask user for extention or a command.\n')
		if answer2 == 'd' and len(extList) > 0:
			print('\nThank you.')
			logFile.write('User done to add extentions. List of extentions containts ' + str(len(extList)) + ' items.')
			break
		elif answer2 == 'd' and len(extList) <= 0:
			print('You didn\'t add any extesntion. Please add at least one or press "exit" to exit')
			logFile.write('User press "d" but list of extentions is empty\n' )
			continue
		elif re.search(r'^\w{2,4}$', answer2) != None:
			extList.append(answer2.upper())
			extList.append(answer2.lower())
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

def sortByExt(allFiles, extList, withOrWithout):
	logFile.write('\nStart to sort out files with urers\' extentions\n')
	filesWithExt = []
	filesWithoutExt = []
	for file in allFiles:
		if file.endswith(extList): #you can compare with list
			filesWithExt.append(file)
		else:
			filesWithoutExt.append(file)	
	
	if withOrWithout: #if it is True
		withOrWithoutWord = 'with'
		countAndPrintSorted(filesWithExt, withOrWithoutWord)
		return filesWithExt
	else:
		withOrWithoutWord = 'without'
		countAndPrintSorted(filesWithoutExt, withOrWithoutWord)
		return filesWithoutExt

#def zipFiles():

logFile = open('.\\logZipByExtention.txt', 'w', encoding='UTF-8')
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
		continue


allFiles = lookingForFiles(pathToSearch)
#return all files from path - return list with paths to these files

############# ask user about which files he wants to zip #############

while True:
	answer1 = input('Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: ')
	logFile.write('Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: \n')
	if answer1 == '1':
		extList = addExt()
		#get list of extention to sort by from user
		filesByExt = sortByExt(allFiles, extList, True)
		#add to list only file with users' extentions
		
		#put files in archive
		break
	elif answer1 == '2':
		extList = addExt()
		filesByExt = sortByExt(allFiles, extList, False)
		#add to list all files except from these with users' extentions - return list with path to these files
		#print some statistics of number and size of files
		#put files in archive
		break
	else:
		print('Input error. You should type only 1 or 2. Try again.')
		continue	


######## ask user where to store archive and name of new archive ########

while True:
	pathToStoreArchive = input('Please type here path to store archive: \n')
	
	if re.search(r'^([a-zA-Z]\:\\)', pathToStoreArchive) == None:
		print('Error: it should be an absolute path which starts with something like C:\\. Try again')
		continue
	elif os.path.exists(pathToStoreArchive):
		print('Tnahk you.')
		logFile.write('Path to store archive is ' + pathToStoreArchive + '\n')
		break
	else:
		os.mkdir(pathToStoreArchive)
		print('Tnahk you.')
		print('Path to store archive is ' + os.path.abspath(pathToStoreArchive))
		logFile.write('Path to store archive is ' + os.path.abspath(pathToStoreArchive) + '\n') 
		break

while True:
	archiveName = input('Please write down name of archive. For example MyArchive: ')
	logFile.write('Archive name is: ' + archiveName + '\n')
	if re.search(r'[\%\#\&\{\}\\\<\>\*\?\/\$!\'\":@\+`|=]', archiveName) != None:
		print('Error: ' + archiveName + ' contains forbidden charachters. Choose another name')
		logFile.write('Error: ' + archiveName + ' contains forbidden charachters. Choose another name\n')
		continue
	elif os.path.exists(os.path.join(pathToStoreArchive, archiveName, '.zip')):
		print('Error: archive with this name already exists in this directory')
		logFile.write('Error: archive with this name already exists in this directory\n')
		continue
	else:
		print('Thank you. Name was accepted')
		logFile.write('Name of archive was accepted\n')
		break

print('End of code. It was nice to see you. Take care')
logFile.write('Program has reached end. Auf Wiederluge!')
logFile.close()	

#(\.\w{2,4})