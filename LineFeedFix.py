#!/usr/bin/python

import sys
import subprocess
import os
import glob
import re

print(os.getcwd())

subprocess.call(["mkdir", "regexTest"])
subprocess.call(["unzip", sys.argv[1], "-d", "regexTest"])

os.chdir("regexTest")

#formatting filename
#need to escape [] () {}
ebookFilename = sys.argv[1]

ebookFilename.replace("[", "\\[")
ebookFilename.replace("]", "\\]")
ebookFilename.replace("(", "\\(")
ebookFilename.replace(")", "\\)")
ebookFilename.replace("{", "\\{")
ebookFilename.replace("}", "\\}")

print(ebookFilename)

#for multi line matching we have to make sure that we view the whole file at once
#and we don't go line by line!!!
for files in os.listdir("."):
	#print("*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*" + files)
	if(re.search('\(ebook-txt\) Star Trek - TOS - Ashes Of Eden_split_\d+.htm', files) != None):
		regexFile = open(files, 'r').read()

		lastline = ""
		m = re.findall('<p.*?>.*?</p>', regexFile, re.S)
		for matches in m:
			m2 = re.search('<p.*?>', matches, re.S)
			#print(str(m2.start()) + ", " + str(m2.end()))
			matches = matches[m2.end():-4]
			while(matches.find("<span>") != -1):
				matches = matches[:matches.find("<span>")] + matches[matches.find("<span>")+len("<span>"):]
			while(matches.find("</span>") != -1):
				matches = matches[:matches.find("</span>")] + matches[matches.find("</span>")+len("</span>"):]
			
			m3 = re.search('\d+', matches)
			if(m3 != None):
				if(len(matches) == m3.end() - m3.start()):
					matches = matches[:m3.start()] + matches[m3.end():]

			m4 = re.search('\d+\s+\d+|\s+\d+|\s+', matches)
			if(m4 != None and m4.end() == len(matches)):
				continue


			nbspChange = False
			lastcharList = ""
			lastchar = ""
			for c in matches:
				if(c.isspace()):
					if(ord(c)==160 and (len(lastchar)==0 or ord(lastchar)==160)):
						lastcharList = lastcharList + c
				lastchar = c

			#removing preceeding & trailing whitespace
			matches = matches.strip()

			#removing double page numbers
			m7 = re.search('^\s*\d+\s+\d+\s*$', matches)
			if(m7 != None):
				continue

			#removing single page numbers
			m8 = re.search('^\s*\d+\s*$', matches)
			if(m8 != None):
				continue

			#new paragraphs start with " 
			if(len(lastcharList)>1 or (len(matches) > 0 and matches[0] == "\"")):
				print("\n\t", end="")

			#chapter locating
			chapterTile = True
			for c in matches:
				if(not(c.isupper()) and True):
					chapterTile = False

			#display the line
			if(chapterTile):
				print("\nChapter Title " + matches)
			elif(len(matches)>1):
				print(matches, end="")

			#correct quote spacing
			if(lastline != ""):
				if(lastline[:] == "\"" and (len(lastline) > 0 and lastline[0] != "\"")):
					print("\n\t", end="")

			lastline = matches

os.chdir("..")
