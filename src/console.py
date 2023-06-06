from colorama import Fore
import datetime as dt
import time

class Console:
    def success(message):
        print(
          Fore.LIGHTBLACK_EX 
          + "[" 
          + dt.datetime.fromtimestamp(time.time()).strftime("%H:%M")  
          + "] " 
          + Fore.RESET 
          + Fore.GREEN 
          + "SUCCESS  " 
          + Fore.RESET 
          + message
      )
    
    def error(message):
         print(
               Fore.LIGHTBLACK_EX 
              + "[" 
              + dt.datetime.fromtimestamp(time.time()).strftime("%H:%M")  
              + "] " 
              + Fore.RESET 
              + Fore.RED 
              + "ERR  " 
              + Fore.RESET 
              + str(message)
          )
            
    def log(message):
         print(
               Fore.LIGHTBLACK_EX 
               + "[" 
              + dt.datetime.fromtimestamp(time.time()).strftime("%H:%M")  
              + "] " 
              + Fore.RESET 
              +Fore.MAGENTA 
              + "INF  " 
              + Fore.RESET 
              + message
          )