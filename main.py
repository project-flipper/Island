import loguru
from fastapi import FastAPI

from island.routes import router
from island.core.events import create_start_app_handler, create_stop_app_handler

print ("""
                                                                 
                                                                 
   ,---,              ,--,                                       
,`--.' |            ,--.'|                                 ,---, 
|   :  :            |  | :                     ,---,     ,---.'| 
:   |  '  .--.--.   :  : '                 ,-+-. /  |    |   | : 
|   :  | /  /    '  |  ' |     ,--.--.    ,--.'|'   |    |   | | 
'   '  ;|  :  /`./  '  | |    /       \  |   |  ,"' |  ,--.__| | 
|   |  ||  :  ;_    |  | :   .--.  .-. | |   | /  | | /   ,'   | 
'   :  ; \  \    `. '  : |__  \__\/: . . |   | |  | |.   '  /  | 
|   |  '  `----.   \|  | '.'| ," .--.; | |   | |  |/ '   ; |:  | 
'   :  | /  /`--'  /;  :    ;/  /  ,.  | |   | |--'  |   | '/  ' 
;   |.' '--'.     / |  ,   /;  :   .'   \|   |/      |   :    :| 
'---'     `--'---'   ---`-' |  ,     .-./'---'        \   \  /   
                             `--`---'                  `----'    
                                                                 
       """)

app = FastAPI()
app.include_router(router)

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))