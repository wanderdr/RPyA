import pyautogui
import getpass
import sys
import atexit
from datetime import datetime

class RPyA:
	def __init__(self):
		'''
		After finishing the script, the function mentioned will be called automatically.
		It is responsible to release any key that that was holded down
		'''
		atexit.register(self.__EndScript)
		
		'''
		This is the function called in the beggining of any function created here.
		If needed to change the way it get the function name and parameters, just
		have to change it here
		'''
		self.__action = "self._RPyA__StoreActions(sys._getframe().f_code.co_name, locals())"

		#Flag to store or not actions called in a list
		self.__fl_store_actions = True
		#Flag to stop on error
		self.__fl_stop_on_error = True
		#Flag to log on error
		self.__fl_log_on_error = True
		#Flag to log any information
		self.__fl_log_actions = True

		#List with actions called
		self.__actions = []
		#Log file
		self.__log_file = 'c:\\users\\' + getpass.getuser() + '\\documents\\LogRPyA.txt'
		
		#Key that can be holded or released
		self.__keys_list = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+',
		',', '-', '.', '/', '0','1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
		'@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
		'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept',
		'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites',
		'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock',
		'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down',
		'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16',
		'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
		'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji',
		'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply',
		'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8',
		'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print',
		'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
		'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown',
		'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']
		
		#List of keys holded during execution
		self.__key_down_list = []
		self.__mouse_holding = False

	####################################################################################################
	################################# GET AND SET EXECUTION PARAMETERS #################################
	####################################################################################################

	##### DEFINES #####

	def setLogFile(self, file: str):
		self.__log_file = file

	def setLogActions(self, fl_log_actions: bool):
		self.__fl_log_actions = fl_log_actions

	def setLogOnError(self, fl_log_on_error: bool):
		self.__fl_log_on_error = fl_log_on_error

	def setStopOnError(self, fl_stop_on_error: bool):
		self.__fl_stop_on_error = fl_stop_on_error

	def setStoreActions(self, fl_store_actions: bool):
		self.__fl_store_actions = fl_store_actions

	##### ACTIONS RELATED #####

	def getActions(self):
		return self.__actions

	def getActionsText(self):
		text = ''
		for action in self.__actions:
			action[2].pop('self', None)
			text = ('' if len(text) == 0 else text + '\n') + '[{date}] {function} - {params}'.format(date=action[0], function=action[1], params=action[2])
		return text

	def getNumberOfActions(self):
		return len(self.__actions)

	##### TIME RELATED #####

	def getStartOfExecution(self):
		if len(self.__actions) > 0:
			return self.__actions[0][0]
		return 'No information'

	def getEndOfExecution(self):
		if len(self.__actions) > 0:
			return self.__actions[-1][0]
		return 'No information'

	def getTimeOfExecution(self):
		if len(self.__actions) == 1:
			return 'Just one action was called'
		elif len(self.__actions) > 1:
			fmt = '%Y-%m-%d %H:%M:%S.%f'
			return datetime.strptime(self.__actions[-1][0], fmt) - datetime.strptime(self.__actions[0][0], fmt)
		return 'No information'

	def getFunctions(self):
		return sorted([func for func in dir(self) if callable(getattr(self, func)) and not func.startswith("__") and not func.startswith("_RPyA__")])

	def getKeyList(self):
		return sorted(self.__keys_list)

	##### PRIVATE FUNCTIONS #####

	def __StoreActions(self, function: str, params: dict):
		time = str(datetime.now())
		if self.__fl_store_actions:
			self.__actions.append([time, function, params])

		if self.__fl_log_actions:
			fh = open(self.__log_file, 'a')
			fh.write('[{date}] Calling function \'{function}\'\n'.format(date=time, function=function))
			fh.close()

	def __Exception(self, error: str):
		if self.__fl_log_on_error:
			fh = open(self.__log_file, 'a')
			fh.write('\nEXCEPTION:\n{error}\n\n'.format(date=str(datetime.now()), error=error))
			fh.close()

		if self.__fl_stop_on_error:
			raise Exception(error)

	def __EndScript(self):
		for key in self.__key_down_list:
			print('keying up {key}'.format(key=key))
			self.KeyUp(key)

	def __MouseClick(self, button: int):
		if button == 0:
			return 'left'
		elif button == 1:
			return 'middle'
		elif button == 2:
			return 'right'

	####################################################################################################
	############################################ ACTION LIST ###########################################
	####################################################################################################

	def moveMouse(self, x: int, y: int):
		eval(self.__action)
		size = pyautogui.size()
		if (x <= 0 or x > size[0]) or (y <= 0 or y > size[1]):
			self.__Exception('Index out of bounds (x: {x}, y: {y})'.format(x=x, y=y))
		else:
			pyautogui.moveTo(x, y)

	def moveMouseAndClick(self, x: int, y: int, button: int = 0):
		eval(self.__action)
		size = pyautogui.size()
		error = False
		if (x < 0 or x > size[0]) or (y < 0 or y > size[1]):
			self.__Exception('Index out of bounds')
		else:
			if button == 0:
				button = 'left'
			elif button == 1:
				button = 'middle'
			elif button == 2:
				button = 'right'
			else:
				error = True
				self.__Exception('No button found')

			if not error:
				pyautogui.click(x=x, y=y, button=button)

	def click(self, button: int = 0):
		eval(self.__action)
		error = False
		if button == 0:
			button = 'left'
		elif button == 1:
			button = 'middle'
		elif button == 2:
			button = 'right'
		else:
			error = True
			self.__Exception('No button found')

		if not error:
			pyautogui.click(x=x, y=y, button=button)

	def getScreenResolution(self):
		eval(self.__action)
		size = pyautogui.size()
		return {'x': size[0], 'y': size[1]}
		
	def write(self, string: str, delay: int = 0.1):
		eval(self.__action)
		pyautogui.typewrite(string, delay)

	def keyUp(self, key: str):
		eval(self.__action)
		if key in self.__keys_list:
			pyautogui.keyUp(key)
			if key in self.__key_down_list:
				self.__key_down_list.remove(key)
		else:
			self.__Exception('Key \'{key}\' not in list (get the key list with the function \'GetKeyList()\')'.format(key=key))

	def keyDown(self, key: str):
		eval(self.__action)
		if key in self.__keys_list:
			pyautogui.keyDown(key)
			if key not in self.__key_down_list:
				self.__key_down_list.append(key)
		else:
			self.__Exception('Key \'{key}\' not in list (get the key list with the function \'GetKeyList()\')'.format(key=key))
	
	def copy(self):
		eval(self.__action)
		pyautogui.hotkey('ctrl', 'c')
	
	def paste(self):
		eval(self.__action)
		pyautogui.hotkey('ctrl', 'v')

	def keyCombination(self, key_list: list):
		eval(self.__action)
		command = ''
		for key in key_list:
			if key.lower() not in self.__keys_list:
				self.__Exception('Key \'{key}\' not in list (get the key list with the function \'GetKeyList()\')'.format(key=key))
				break
			else:
				command = ('{command}, '.format(command=command) if len(command) > 0 else '') + '\'{key}\''.format(key=key)

		if len(command) == 0:
			self.__Exception('There is no key passed to the function')
		else:
			eval('pyautogui.hotkey(' + command + ')')
	
	def getMousePosition(self):
		eval(self.__action)
		return pyautogui.position()

	def screenshot(self, location: str = ""):
		eval(self.__action)
		if len(location) == 0:
			location = self.__log_file.replace('.txt', '.png')
		pyautogui.screenshot(location)

	def screenshotArea(self, location: str = "", left : int = 0, top : int = 0, width : int = 0, height : int = 0):
		eval(self.__action)
		size = pyautogui.size()
		if len(location) == 0:
			location = self.__log_file.replace('.txt', '.png')
		
		if (left <= 0 or left > size[0]) or (top <= 0 or top > size[1]):
			self.__Exception('Index out of bounds (left: {left}, top: {top})'.format(left=left, top=top))
		elif width <= 0 or height <= 0:
			self.__Exception('Width or height cannot be equal or less than 0 (width: {width}, height: {height})'.format(width=width, height=height))
		elif (left + width > size[0]) or (top + height > size[1]):
			self.__Exception('Index out of bounds (left + width: {left}, top + height: {top})'.format(left=(left + width), y=(y + height)))
		else:
			pyautogui.screenshot(location, region=(left, top, width, height))

	def imageRecognition(self, base_image: str, image: str):
		eval(self.__action)

	def imageRecognitionOnScreen(self, image: str, move_mouse: bool = False, click_mouse: bool = False):
		eval(self.__action)

	def imageRecognition(self, base_image: str, image: str):
		eval(self.__action)
		
	def waitUntilImageAppears(self, image: str, wait_miliseconds: int):
		eval(self.__action)

	def getPixelOnScreen(self, x: int, y: int):
		eval(self.__action)

	def waitPixelOnScreen(self, x: int, y: int, color: str, limit_seconds: int = 60):
		eval(self.__action)

	def waitPixelOnScreen(self, x: int, y: int, color: str, limit_seconds: int = 60):
		eval(self.__action)

	####################################################################################################
	#################################### WINDOWS ACTION LIST ###########################################
	####################################################################################################

	def listWindows(self, name: str = ''):
		eval(self.__action)

	def getWindow(self, name: str = '', id: int = 0):
		eval(self.__action)

	def windowMove(self, window: Window, x: int, y: int):
		eval(self.__action)

	def windowResize(self, window: Window, x: int, y: int):
		eval(self.__action)

	def windowMaximiza(self, window: Window):
		eval(self.__action)

	def windowMinimize(self, window: Window):
		eval(self.__action)

	def windowMove(self, window: Window, x: int, y: int):
		eval(self.__action)

	def windowRestore(self, window: Window):
		eval(self.__action)

	def windowClose(self, window: Window):
		eval(self.__action)

	def windowPosition(self, window: Window, x: int, y: int):
		eval(self.__action)

	def windowMoveRelative(self, window: Window, x: int, y: int):
		eval(self.__action)

	def windowClickRelative(self, window: Window, x: int, y: int, button: int = 0):
		eval(self.__action)

	'''
	pyautogui.getWindows() # returns a dict of window titles mapped to window IDs
	pyautogui.getWindow(str_title_or_int_id) # returns a “Win” object
	win.move(x, y)
	win.resize(width, height)
	win.maximize()
	win.minimize()
	win.restore()
	win.close()
	win.position() # returns (x, y) of top-left corner
	win.moveRel(x=0, y=0) # moves relative to the x, y of top-left corner of the window
	win.clickRel(x=0, y=0, clicks=1, interval=0.0, button=’left’)



	TASKLIST /FI "windowtitle eq How to access*"

	Image Name                     PID Session Name        Session#    Mem Usage
	========================= ======== ================ =========== ============
	firefox.exe                   1196 Console                    1    289.132 K

	'''

a = RPyA()
a.ScreenshotArea("", 10, 100, 200, 100)