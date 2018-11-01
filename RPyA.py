from datetime import datetime
import pyautogui
import getpass
import atexit
import math
import time
import os

class RPyA:
    def __init__(self):
        """
        Class created to simplify some pyautogui functions and some other usefull stuffs.
        """

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
            self.__Exception('Key \'{key}\' not in list (get the key list with the function \'getKeyList()\')'.format(key=key))

    def keyDown(self, key: str):
        eval(self.__action)
        if key in self.__keys_list:
            pyautogui.keyDown(key)
            if key not in self.__key_down_list:
                self.__key_down_list.append(key)
        else:
            self.__Exception('Key \'{key}\' not in list (get the key list with the function \'getKeyList()\')'.format(key=key))

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
                self.__Exception('Key \'{key}\' not in list (get the key list with the function \'getKeyList()\')'.format(key=key))
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

    def imageRecognition(self, base_image: str, image: str, all_results: bool = False, grayscale: bool = False):
        eval(self.__action)

        if not os.path.isfile(image):
            self.__Exception('Base image do not exist ({base})'.format(base=base_image))
        elif not os.path.isfile(image):
            self.__Exception('Image do not exist ({image})'.format(image=image))
        else:
            if not all_results:
                position = pyautogui.locate(image, base_image, grayscale=grayscale)
                position = [position[0], position[1]] if position is not None else None
            else:
                position = []
                positions = pyautogui.locateAll(image, base_image, grayscale=grayscale)
                for i in positions:
                    position.append([i[0], i[1]])
                position = position if len(position) > 0 else None

            if position is None:
                self.__Exception('Image not found on base image'.format(image=image))
                return None
            return position

    def imageRecognitionOnScreen(self, image: str, center: bool = True, all_results: bool = False, grayscale: bool = False):
        eval(self.__action)

        if not os.path.isfile(image):
            self.__Exception('Image do not exist ({image})'.format(image=image))
        else:
            if not all_results:
                if not center:
                    position = pyautogui.locateOnScreen(image, grayscale=grayscale)
                else:
                    position = pyautogui.locateCenterOnScreen(image, grayscale=grayscale)
                position = [position[0], position[1]] if position is not None else None
            else:
                position = []
                positions = pyautogui.locateAllOnScreen(image, grayscale=grayscale)
                for i in positions:
                    '''
                    PyAutoGui don't have a function to locate all center on screen, so,
                    improvise, adapt, overcome!
                    '''
                    x, y = i[0], i[1]
                    if center:
                        x = x + math.floor(i[2] / 2)
                        y = y + math.floor(i[3] / 2)
                    position.append([x, y])
                position = position if len(position) > 0 else None

            if position is None:
                self.__Exception('Image not found on base image'.format(image=image))
                return None
            return position

    def clickImageOnScreen(self, image: str, center: bool = True, button: int = 0, grayscale: bool = False):
        eval(self.__action)

        if not os.path.isfile(image):
            self.__Exception('Image do not exist ({image})'.format(image=image))
        else:
            if not center:
                position = pyautogui.locateOnScreen(image, grayscale=grayscale)
            else:
                position = pyautogui.locateCenterOnScreen(image, grayscale=grayscale)

            if position is not None:
                self.moveMouseAndClick(position[0], position[1], button)
                return True
            return False

    def waitUntilImageAppears(self, image: str, limit_seconds: int, grayscale: bool = False):
        eval(self.__action)

        found = False
        start_time = time.time()

        while not found:
            position = pyautogui.locateOnScreen(image, grayscale=grayscale)
            found = True if position is not None else False
            if not found:
                if time.time() - start_time < limit_seconds:
                    time.sleep(1)
                else:
                    break

        return True

    def getPixelOnScreen(self, x: int, y: int):
        eval(self.__action)

        image = pyautogui.screenshot()
        return list(image.getpixel((x, y)))

    def waitPixelOnScreen(self, x: int, y: int, rgb: list, limit_seconds: int = 60):
        eval(self.__action)

        found = False
        start_time = time.time()

        while not found:
            image = pyautogui.screenshot()
            found = list(image.getpixel((x, y))) == rgb
            if not found:
                if time.time() - start_time < limit_seconds:
                    time.sleep(1)
                else:
                    break

        return found

    ####################################################################################################
    #################################### WINDOWS ACTION LIST ###########################################
    ####################################################################################################

    def listWindows(self):
        eval(self.__action)
        windows = list(filter(None, pyautogui.getWindows().keys()))
        return windows

    def getWindow(self, name: str = '', id: int = 0):
        eval(self.__action)
        window = None
        temp = id if id > 0 else name
        if temp == '':
            self.__Exception('You must specify a name or ID')
        else:
            window = pyautogui.getWindow(temp)
        return window

    def getWindowSize(self, window: pyautogui._window_win.Window):
        eval(self.__action)

        positions = window.get_position()
        return [positions[2] - positions[0], positions[3] - positions[1]]

    def setWindowFocus(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        window.set_foreground()

    def windowMove(self, window: pyautogui._window_win.Window, x: int, y: int):
        eval(self.__action)
        size = pyautogui.size()
        if (x <= 0 or x > size[0]) or (y <= 0 or y > size[1]):
            self.__Exception('Index out of bounds (x: {x}, y: {y})'.format(x=x, y=y))
        else:
            window.move(x, y)

    def windowResize(self, window: pyautogui._window_win.Window, width: int, height: int):
        eval(self.__action)
        if x <= 0 or y <= 0:
            self.__Exception('Width or height not valid (width: {width}, height: {height})'.format(width=width, height=height))
        else:
            window.resize(width, height)

    def windowMaximiza(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        window.maximize()
    
    def windowMinimize(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        window.minimize()
    
    def windowRestore(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        window.restore()
    
    def windowClose(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        window.close()

    def windowPosition(self, window: pyautogui._window_win.Window):
        eval(self.__action)
        return list(window.get_position())

    def windowMoveRelative(self, window: pyautogui._window_win.Window, x: int, y: int):
        eval(self.__action)

        size = pyautogui.size()
        position = window.get_position()
        if (position[0] + x > size[0]) or (position[1] + y > size[1]):
            self.__Exception('Index out of bounds (x: {x}, y: {y})'.format(x=x, y=y))
        else:
            window.move(position[0] + x, position[1] + y)


    def windowClickRelative(self, window: pyautogui._window_win.Window, x: int, y: int, button: int = 0):
        eval(self.__action)

        size = pyautogui.size()
        #We have to restore it because we can't get the position/size with it minimized
        window.restore()
        position = window.get_position()
        if (position[0] + x > size[0]) or (position[1] + y > size[1]):
            self.__Exception('Index out of bounds (x: {x}, y: {y})'.format(x=x, y=y))
        else:
            #Put the window on focus before move mouse and click
            window.set_foreground()
            pyautogui.click(x=position[0] + x, y=position[1] + y, button='left')
