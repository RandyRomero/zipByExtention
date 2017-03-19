# !python3 

'''Program that ask user which type of files he wants to archive (by extention), ask for path and go through this path looking for every file with these extentions. Also user should denote if he wants to archive files with these extentions of all other files except files with these extentions'''

import os, re, shutil, sys, zipfile

def prlog(message):
	print(message)
	logFile.write(message + '\n')

def printGrid(number):
	for i in range(number):
		print('##############################################################')
		logFile.write('##############################################################\n')

def lookingForFiles(pathToSearch):
	logFile.write('There are these files in: ' + pathToSearch + '\n')
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
					#We need to use \\?\ before path that is more than 260 symbols otherwise we get an error
				totalSize += size
				allFiles.append(os.path.join(folderName, file))
				logFile.write(os.path.join(folderName, file) + '\n')

	if len(allFiles) == 0: 
		return 0			

	logFile.write('\n')
	printGrid(1)
	prlog('There are ' + str(len(allFiles)) + ' files with total size of '	+ str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.')
	printGrid(1)
	prlog('')
	
			
	return allFiles #list of all files including files in subfolders

def countAndPrintSorted(filesToCount, withOrWithoutWord):
	totalSize = 0

	for item in filesToCount:
		size = os.path.getsize(item)
		totalSize += size
		logFile.write(item + '\n')

	logFile.write('\n')
	printGrid(1)	
	prlog('There are ' + str(len(filesToCount)) + ' files ' + withOrWithoutWord + ' your extentions with total size of ' + str('%0.2f' % (totalSize / 1024 / 1024)) + ' MB.')
	printGrid(1)
	prlog('')

def addExt():
	answer2 = ''
	extList = []
	print('\nStage 3: Adding extentions to work with.')
	while True:
		answer2 = input('\nType here some extentions one by one separated by "enter".\nWhen you are done, type "d" and press enter.\nIf you want to exit, type "e" and press enter: ')
		logFile.write('Ask user for extention or a command.\n')
		if answer2 == 'd' and len(extList) > 0:
			print('Thank you.\n')
			logFile.write('User done to add extentions. List of extentions containts ' + str(len(extList)) + ' items.')
			break
		elif answer2 == 'd' and len(extList) <= 0:
			print('You didn\'t add any extesntion. Please add at least one or press "exit" to exit')
			logFile.write('User press "d" but list of extentions is empty\n' )
			continue
		elif re.search(r'^\w{2,4}$', answer2) != None:
			extList.append(answer2.upper())
			extList.append(answer2.lower())
			prlog('Extention ' + answer2 + ' was added. There are these extention to look for now: ')
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
	logFile.write('\nStart to sort out files with users\' extentions\n')
	filesToArchive = []

	if withOrWithout:
		for file in allFiles:
			if file.endswith(extList):
				filesToArchive.append(file)
		countAndPrintSorted(filesToArchive, 'with')
		return filesToArchive

	elif not withOrWithout:
		for file in allFiles:
			if not file.endswith(extList):
				filesToArchive.append(file)
		countAndPrintSorted(filesToArchive, 'without')		
		return filesToArchive

def zipFiles(filesToArchive, pathToStoreArchive):
	archive = zipfile.ZipFile(pathToStoreArchive, 'w')
	
	filesInArchive = [] #list to track files putted in archive
	for file in filesToArchive:
		# if-else here for preventing occurrence of files with the same basenames in archive 
		if os.path.basename(file) not in filesInArchive:
			archive.write(file, arcname=os.path.basename(file), compress_type=zipfile.ZIP_DEFLATED)
			filesInArchive.append(os.path.basename(file))
			# 'file' if full path to archive (could be relative if you want)
			# 'arcname' - it is basename of archive
			# here I rename files to left only its name without relative of full path
		else:
			archive.write(file, os.path.relpath(file), compress_type=zipfile.ZIP_DEFLATED)
			#if file with such basename already exists in archive - script uses not basename, but relname

		prlog('Compressing %s...' % (file))
	
	archive.close()
	prlog('Compressing is done.')	


#########################################################################

logFile = open('.\\logZipByExtention.txt', 'w', encoding='UTF-8')
logFile.write('Program has started.\n\n')

print()
printGrid(3)
prlog('Hello there! This is script for acrhiving files. Let\'s begin!')
printGrid(3)
print()

########## ask user about path to work and check it #####################

while True:
	pathToSearch = input('Stage 1: Type in path to directory where to look for your files to be zipped: \n')
	logFile.write('\nStage 1: Type in path to directory where to look for your files to be zipped: ' + pathToSearch + '\n')
	
	if os.path.exists(pathToSearch):
		if os.path.isdir(pathToSearch):
			print('Ok, this directory exists.\n')
			logFile.write('Path to direcory to zip accepted: ' + pathToSearch + '\n\n')
			allFiles = lookingForFiles(pathToSearch)
			
			if allFiles == 0:
				print('The folder is empty. Choose another')
				logFile.write(pathToSearch + ' is emptry. Restart loop\n')
				continue
			break	
		else:
			prlog('It should be folder, not a file.\n')	
			continue
	else:
		prlog('There is no such directory. Try again.\n')	
		continue

############# ask user about which files he wants to zip #############

while True:
	answer1 = input('Stage 2: Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: ')
	logFile.write('Stage 2: Would you like to \n - (1) zip files with certain extentions \n or \n - (2) zip all files except files with these extentions?\nYour answer is: \n')
	if answer1 == '1':
		#set program arcive files with user's extention
		withOrWithoutExt = True
		logFile.write('Program will archive files with users\' extentions')
	elif answer1 == '2':
		#set program to archive files without user's files
		withOrWithoutExt = False
		logFile.write('Program will archive files without users\' extentions\n')
	else:
		prlog('Input error. You should type only 1 or 2. Try again.')
		continue

	#get list of extention to sort by from user
	extList = addExt()
	#find out wich files script will put to archive
	filesToArchive = sortByExt(allFiles, extList, withOrWithoutExt)

	if len(filesToArchive) <= 0: 
		# if there is nothing to put in archive - restart loop
		print('Zero matches. Please, enter another extentions.\n')
		logFile.write('Zero matches. Restart loop.\n')
		continue
	break		

################### ask user where to store archive  ########################

while True:
	folderToStoreArchive = input('Stage 4: Please type here path to store archive: \n')
	logFile.write('\nPlease type here path to store archive: ' + folderToStoreArchive + '\n')
	
	if re.search(r'^([a-zA-Z]\:\\)', folderToStoreArchive) == None:
		prlog('Error: it should be an absolute path which starts with something like C:\\. Try again.\n')
		continue
	elif os.path.exists(folderToStoreArchive):
		print('Tnahk you.\n')
		logFile.write('Path to store archive is ' + folderToStoreArchive + '\n')
		break
	else:
		os.makedirs(folderToStoreArchive)
		print('Tnahk you.')
		logFile.write('Path to store archive is ' + folderToStoreArchive + '\n')
		break

################## ask user the name of the new archive #####################

while True:
	archiveName = input('Stage 5: Please write down name of archive. For example MyArchive: ')
	logFile.write('\nStage 5: Please write down name of archive. For example MyArchive: ' + archiveName + '\n')
	if re.search(r'[\%\#\&\{\}\\\<\>\*\?\/\$!\'\":@\+`|=]', archiveName) != None:
		prlog('Error: ' + archiveName + ' contains forbidden charachters. Choose another name.\n')
		continue
	elif os.path.exists(os.path.join(folderToStoreArchive, archiveName + '.zip')):
		prlog('Error: archive with this name already exists in this directory')
		continue
	else:
		prlog('Thank you. Path to archive is: ' + os.path.join(folderToStoreArchive, archiveName + '.zip\n'))
		break

pathToStoreArchive = os.path.join(folderToStoreArchive, archiveName + '.zip')

##############################################################################

prlog('Start to zip files')
zipFiles(filesToArchive, pathToStoreArchive)


print('\nEnd of code. It was nice to see you. Take care.')
logFile.write('Program has reached end. Auf Wiederluge!')
logFile.close()	


#260