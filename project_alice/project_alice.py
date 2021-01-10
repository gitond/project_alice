# Project Alice point & Click edition v1.0

# Importing libraries
import pygame
import os
import json
import time
import re

# Current directory (for loading resources to the game)
thisDir = os.path.dirname(__file__)

def emptyInventory(ibg, x):
	iObjects = {
		"background": [ibg, [0,0]],
		"x": [x, [1110, 70]]
	}
	return iObjects

def upadateItemDescription(itemDescs, item):
	itemDescs[item]["descriptionLine1"] = itemDescs[item].pop("updateDescript1")
	itemDescs[item]["descriptionLine2"] = itemDescs[item].pop("updateDescript2")
	itemDescs[item]["descriptionLine3"] = itemDescs[item].pop("updateDescript3")


def saveGame(pInventory, itemDescs, rID):
	packToJson = {}
	invToSave = []
	for item in pInventory:
		itemToSave = []
		itemPicIdS = itemDescs[item[0]]["pictureID"].split(",")
		itemToSave.append(item[0])
		itemToSave.append(itemPicIdS[0])
		itemToSave.append(itemPicIdS[1])
		if "updateDescript1" not in itemDescs[item[0]]:
			itemToSave.append("STATUS::UPDATED")
		invToSave.append(itemToSave)
	packToJson["inventory"] = invToSave
	packToJson["roomID"] = rID

	with open(str(thisDir) + "/resources/data/savefile.json" , "w") as savefile:
		json.dump(packToJson, savefile)

def emptyChat(screen_bg, button):
	monitorObjects = {
		"background": [screen_bg, (0,0)],
		"button1": [button, (80, 550)],
		"button2": [button, (80, 610)]
	}
	return monitorObjects

def returnListIncludingSearchable(listOfLists, searchable):
	for lInList in listOfLists:
		if lInList[0] == searchable:
			return lInList

def firstInAnyList(listOfLists, searchable):
	for lInList in listOfLists:
		if lInList[0] == searchable:
			return True
	return False

def examineItems(invItems, pInventory, itemDescs, font):
	black = (0, 0, 0)
	colorTwine = (189, 129, 79)
	i = 0
	for items in pInventory:
		invItems[items[0] + "Small"] = [items[1], (752+i,475)]
		# The "big" versions of each item have to be rendered in order for renderReSorter to work. If time, optimize later.
		invItems[items[0] + "Big"] = [items[2], (60,110)]
		i += 70

	if pInventory != []:
		renderOrederReSorter = {}
		renderOrederReSorter[pInventory[0][0] + "Small"] = invItems[pInventory[0][0] + "Small"]
		renderOrederReSorter[pInventory[0][0] + "Big"] = invItems[pInventory[0][0] + "Big"]

		del invItems[pInventory[0][0] + "Small"]
		del invItems[pInventory[0][0] + "Big"]

		invItems[pInventory[0][0] + "Small"] = renderOrederReSorter[pInventory[0][0] + "Small"]
		invItems[pInventory[0][0] + "Big"] = renderOrederReSorter[pInventory[0][0] + "Big"]

		itemID = font.render(itemDescs[pInventory[0][0]]["id"], True, black, colorTwine)
		descL1 = font.render(itemDescs[pInventory[0][0]]["descriptionLine1"], True, black, colorTwine)
		descL2 = font.render(itemDescs[pInventory[0][0]]["descriptionLine2"], True, black, colorTwine)
		descL3 = font.render(itemDescs[pInventory[0][0]]["descriptionLine3"], True, black, colorTwine)

		invItems["itemTitle"] = [itemID, (700,225)]
		invItems["Line1"] = [descL1, (705,320)]
		invItems["Line2"] = [descL2, (705,361)]
		invItems["Line3"] = [descL3, (705,402)]

def dialogue(id):
	with open(str(thisDir) + "/resources/data/chat.json") as json_file:
		data = json.load(json_file)
	return data[id]

def action(inp, rID, prevRID, pInventory, currentPuzzleSolved):
	if (rID == "monitor"):
		if (inp == "x"):
			rID = "00n"
	elif (rID == "00n"):
		if (inp == "bookshelf"):
			return "GETITEM002manualROOMID00nOBJECTbookshelfSKINnoManShelf"
		elif (inp == "computer"):
			rID = "monitor"
		elif (inp == "inventory"):
			rID = "iScreen"
		elif (inp == "downA"):
			rID = "10w"
		elif (inp == "sIcon"):
			return "SAVEGAME"
		elif (inp == "lIcon"):
			return "LOADGAME"
	elif (rID == "iScreen"):
		if (inp == "x"):
			return prevRID
		elif firstInAnyList(pInventory, inp[:-5]):
			return "REMOVE" + inp[:-5]
	elif (rID == "10w"):
		if (inp == "arrow"):
			rID = "00n"
		elif (inp == "inventory"):
			rID = "iScreen"
		elif (inp == "trashCan"):
			return "GETITEM003teaROOMID10wOBJECTtrashCanSKINtrashCanNoT"
		elif (inp == "fridge"):
			return "GETITEM004potatoROOMID10wOBJECTfridgeSKINfridgeNoWeb"
		elif (inp == "teaKettle") and currentPuzzleSolved:
			return "GETITEM005keysROOMID10wOBJECTteaKettleSKINkettleWhite"
		elif (inp == "door") and firstInAnyList(pInventory, "005keys"):
			rID = "ending"
		elif (inp == "sIcon"):
			return "SAVEGAME"
		elif (inp == "lIcon"):
			return "LOADGAME"

	return rID

def gameMode(chatID, font, monitorObjects, screen, button, x):
	discussion = dialogue(chatID)
	pointer = 0
	white = (255, 255, 255)
	black = (0, 0, 0)
	screenBGDarkerBlue = (157, 194, 210)
	while pointer < len(discussion):
		#currentTime = round(time.time())
		#startTime = currentTime
		line = discussion[pointer]
		button1Index = -1
		button2Index = -1
		text = font.render(line["sender"] + ": " + line["message"], True, black, screenBGDarkerBlue)
		# Moves messages
		for object in monitorObjects:
			if object[0] == "0":
				if monitorObjects[object][1][1] - 50 < 100:
					monitorObjects[object][1][1] -= 500
				else:
					monitorObjects[object][1][1] -= 50

		monitorObjects[line["messageID"]] = [text, [80,500]]

		# Rendering here
		objList = renderObjects(screen, monitorObjects)
		pygame.display.flip()
		if "v" in line["responses"]:
			responses = line["responses"].split("v")
			buttonLine1 = discussion[min(int(re.sub("^0*", "", responses[0])), int(re.sub("^0*", "", responses[1])))-1]
			buttonLine2 = discussion[max(int(re.sub("^0*", "", responses[0])), int(re.sub("^0*", "", responses[1])))-1]
			buttonText1 = font.render(buttonLine1["message"], True, black, (193, 217, 227))
			buttonText2 = font.render(buttonLine2["message"], True, black, (193, 217, 227))
			monitorObjects["button1"][0] = buttonText1
			monitorObjects["button2"][0] = buttonText2
			objList = renderObjects(screen, monitorObjects)
			pygame.display.flip()
			playerMadeChoice = False
			while not playerMadeChoice:
				for event in pygame.event.get():
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
						for obj in objList:
							if obj[0].collidepoint(event.pos):
								if obj[1] == "button1" or obj[1] == "button2":
									playerMadeChoice = True
									if obj[1] == "button1":
										pointer = min(int(re.sub("^0*", "", responses[0])), int(re.sub("^0*", "", responses[1])))-2
									else:
										pointer = max(int(re.sub("^0*", "", responses[0])), int(re.sub("^0*", "", responses[1])))-2
		if line["responses"][0:5] == "FINAL":
			monitorObjects["button1"][0] = button
			monitorObjects["button2"][0] = button
			monitorObjects["x"] = [x, (1110, 90)]
			objList = renderObjects(screen, monitorObjects)
			pygame.display.flip()

			# returning values by appending them to monitorObjects and then removing them in main()
			# :wesmart:
			if len(line["responses"]) != 5:
				monitorObjects["response"] = line["responses"][6:]

			break
		pointer += 1
		#while currentTime < startTime + line["sleep"]:
		#	currentTime = round(time.time())

def renderObjects(screen, roomID):
	objectsInRoom = []
	for object in roomID:
		objectRect = screen.blit(roomID[object][0], roomID[object][1])
		objectsInRoom.append((objectRect, object))
	return objectsInRoom

def main():
	pygame.init()

	# Loading images, fonts and iteminfo.json
	logo = pygame.image.load(str(thisDir) + "/resources/images/logo32x32.png")
	screen_bg = pygame.image.load(str(thisDir) + "/resources/images/backgrounds/screen_bg.png")
	x = pygame.image.load(str(thisDir) + "/resources/images/objects/x.png")
	room00n = pygame.image.load(str(thisDir) + "/resources/images/backgrounds/room00n.png")
	bookshelf = pygame.image.load(str(thisDir) + "/resources/images/objects/bookshelf.png")
	noManShelf = pygame.image.load(str(thisDir) + "/resources/images/objects/bookshelf_no_man.png")
	computer = pygame.image.load(str(thisDir) + "/resources/images/objects/computer.png")
	font = pygame.font.Font(str(thisDir) + "/resources/fonts/aliceplus/aliceplus.ttf", 20)
	button = pygame.image.load(str(thisDir) + "/resources/images/objects/blank_button.png")
	inventory = pygame.image.load(str(thisDir) + "/resources/images/objects/inventory.png")
	ibg = pygame.image.load(str(thisDir) + "/resources/images/backgrounds/inventory_uinterface_placeholder.png")
	kbg = pygame.image.load(str(thisDir) + "/resources/images/backgrounds/kitchen.png")
	kettle = pygame.image.load(str(thisDir) + "/resources/images/objects/tea_kettle_yellow.png")
	kettleWhite = pygame.image.load(str(thisDir) + "/resources/images/objects/water_boiler.png")
	trashCanT = pygame.image.load(str(thisDir) + "/resources/images/objects/trash_can_tea.png")
	trashCanNoT = pygame.image.load(str(thisDir) + "/resources/images/objects/trashcan_upd.png")
	fridge = pygame.image.load(str(thisDir) + "/resources/images/objects/fridge_spiderweb.png")
	fridgeNoWeb = pygame.image.load(str(thisDir) + "/resources/images/objects/fridge.png")
	arrow = pygame.image.load(str(thisDir) + "/resources/images/objects/arrow.png")
	aDown = pygame.image.load(str(thisDir) + "/resources/images/objects/arrow_down.png")
	door = pygame.image.load(str(thisDir) + "/resources/images/objects/door.png")
	manIcon = pygame.image.load(str(thisDir) + "/resources/images/icons/manual.png")
	bigMan = pygame.image.load(str(thisDir) + "/resources/images/icons/manual_big.png")
	teaBox = pygame.image.load(str(thisDir) + "/resources/images/icons/tea.png")
	teaFrog = pygame.image.load(str(thisDir) + "/resources/images/icons/tea_meme.png")
	potatIcon = pygame.image.load(str(thisDir) + "/resources/images/icons/potato.png")
	phoTato = pygame.image.load(str(thisDir) + "/resources/images/icons/potato_photo.png")
	smallKeys = pygame.image.load(str(thisDir) + "/resources/images/icons/very_bad_looking_key.png")
	bigKeys = pygame.image.load(str(thisDir) + "/resources/images/icons/slightly_better_looking_keys.png")
	savIcon = pygame.image.load(str(thisDir) + "/resources/images/objects/save_icon.png")
	lodIcon = pygame.image.load(str(thisDir) + "/resources/images/objects/load_icon.png")
	ending = pygame.image.load(str(thisDir) + "/resources/images/backgrounds/ending_screen.png")
	with open(str(thisDir) + "/resources/data/iteminfo_v3.json") as json_file:
		itemDescs = json.load(json_file)

	# Setting up game
	pygame.display.set_icon(logo)
	pygame.display.set_caption("Project Alice")
	screen = pygame.display.set_mode((1280,720))
	previousRoomID = "monitor"
	currentRoomID = "monitor"
	previousChatID = "000"
	currentChatID = "001"
	canChat = True
	background = screen_bg
	rIDList = []
	allItemsList = []
	pInventory = []
	activeItem = []
	currentPuzzleSolved = False
	running = True

	# Rendering instructions
	with open(str(thisDir) + "/resources/data/objects.json") as json_file:
		objects = json.load(json_file)
		objects = objects["objects"]
	for room in objects:
		for obj in objects[room]:
			objects[room][obj][0] = eval(objects[room][obj][0])

	for roomID in objects:
		rIDList.append(roomID)

	for item in itemDescs:
		iInfo = itemDescs[item]["pictureID"].split(",")
		iInfo.insert(0, item)
		try:
			iInfo[1] = eval(iInfo[1])
			iInfo[2] = eval(iInfo[2])
		except NameError:
			iInfo[0] = item
			del iInfo[2]
			del iInfo[1]
		allItemsList.append(iInfo)

	# Main loop
	while running:
		if currentRoomID not in rIDList:
			if currentRoomID[0:6] == "REMOVE":
				currentRoomID = currentRoomID[6:]
				activeItem = returnListIncludingSearchable(pInventory, currentRoomID)
				del pInventory[pInventory.index(activeItem)]
				pInventory.insert(0, activeItem)
				currentRoomID = "iScreen"

			elif currentRoomID == "SAVEGAME":
				saveGame(pInventory, itemDescs, previousRoomID)
				currentRoomID = previousRoomID

			elif currentRoomID == "LOADGAME":
				objects["iScreen"] = emptyInventory(ibg, x)

				with open(str(thisDir) + "/resources/data/savefile.json") as savefile:
					loadedGame = json.load(savefile)

				for item in loadedGame["inventory"]:
					item[1] = eval(item[1])
					item[2] = eval(item[2])
					if "STATUS::UPDATED" in item:
						try:
							upadateItemDescription(itemDescs, item[0])
							item.pop(3)
							currentPuzzleSolved = True
						except KeyError:
							pass
					objects[itemDescs[item[0]]["roomid"]][itemDescs[item[0]]["object"]][0] = eval(itemDescs[item[0]]["skin"])

				for item in allItemsList:
					if not firstInAnyList(loadedGame["inventory"], item[0]):
						objects[itemDescs[item[0]]["roomid"]][itemDescs[item[0]]["object"]][0] = eval(itemDescs[item[0]]["ogSkin"])

				pInventory = loadedGame["inventory"]
				currentRoomID = loadedGame["roomID"]

			elif firstInAnyList(allItemsList, re.findall("(?<=GETITEM)(.*)(?=ROOMID)", currentRoomID)[0]) and returnListIncludingSearchable(allItemsList, re.findall("(?<=GETITEM)(.*)(?=ROOMID)", currentRoomID)[0]) not in pInventory:
				pInventory.insert(0, returnListIncludingSearchable(allItemsList, re.findall("(?<=GETITEM)(.*)(?=ROOMID)", currentRoomID)[0]))
				objects[re.findall("(?<=ROOMID)(.*)(?=OBJECT)", currentRoomID)[0]][re.findall("(?<=OBJECT)(.*)(?=SKIN)", currentRoomID)[0]][0] = eval(re.findall("(?<=SKIN)(.*)", currentRoomID)[0])
				currentRoomID = previousRoomID
			else:
				currentRoomID = previousRoomID
		else:
			"""
			If input detection returned an new location from where we can only enter a couple of pre defined locations we should update previousRoomID

			When we enter the inventory for example (roomID "iScreen") we want to return to the previous location when closing it
			so pRID shouldn't be updated

			We probably want to exclude also monitor in the future
			"""
			if currentRoomID != "iScreen":
				previousRoomID = currentRoomID

		if currentRoomID == "monitor" and canChat:
			gameMode(currentChatID, font, objects["monitor"], screen, button, x)
			if "response" in objects["monitor"]:
				if objects["monitor"]["response"] == "UNLOCK_KEYS":
					currentPuzzleSolved = True
					upadateItemDescription(itemDescs, "003tea")
				del objects["monitor"]["response"]
			canChat = False

		if currentRoomID == "iScreen":
			examineItems(objects["iScreen"], pInventory, itemDescs, font)
			if pInventory != []:
				activeItem = pInventory[0]
				currentChatID = activeItem[0][0:3]
				objects["monitor"] = emptyChat(screen_bg, button)
				canChat = True

		# Updating screen
		# NOTE!! This has to be before input handling, otherwise the program would try to detect clicks on unrendered objects
		objList = renderObjects(screen, objects[currentRoomID])
		pygame.display.flip()
		# Input handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			# Checks right mouse button for clicks
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if event.button == 1:
					for obj in objList:
						if obj[0].collidepoint(event.pos):
							if currentRoomID != action(obj[1], currentRoomID, previousRoomID, pInventory, currentPuzzleSolved) and action(obj[1], currentRoomID, previousRoomID, pInventory, currentPuzzleSolved) != None:
								currentRoomID = action(obj[1], currentRoomID, previousRoomID, pInventory, currentPuzzleSolved)

# Running the game
if __name__=="__main__":
	main()
