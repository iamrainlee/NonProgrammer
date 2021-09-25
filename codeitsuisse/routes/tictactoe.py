import logging
import json
import asyncio
import aiohttp
from aiosseclient import aiosseclient
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
async def tictactoe():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    battleId = data.get("battleId")
    board = ['NW','N','NE','W','C','E','SW','S','SE']
    played = ['','','','','','','','','']
    youAre = ""
    gameOn = True
    while gameOn :
        async for event in aiosseclient('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/'+battleId):
            # r = requests.get('https://cis2021-arena.herokuapp.com/tic-tac-toe/start/'+battleId)
            data = event
            logging.info("data sent from arena {}".format(data))
            # data = json.loads(msg.data.replace("'",'"'))
            if type(data) is str:
                data = json.loads(data)
            try:
                logging.info(data['youAre'])
                if( data['youAre'] != ""):
                    youAre = data['youAre']
                    if(data['youAre'] == "O"):
                        logging.info("Prepare to makemove")
                        makemove(board,played,youAre,battleId)
            except:
                try:
                    if(data['player'] == youAre):
                        continue
                    else:
                        played[board.index(data['position'])] = data['player']
                        logging.info("Prepare to makemove")
                        makemove(board,played,youAre,battleId)
                except:
                    try:
                        if(data['winner'] == "draw" or data['winner'] == "O"):
                            logging.info("Win game !")
                        else:
                            logging.info("Possibly lost game !")
                        gameOn = False
                    except:
                        gameOn = False
                        continue
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def makemove(board,played,youAre,battleId):
    data = {}
    data['action'] = "putSymbol"
    if(played.count('') == 9):
        data["position"] = "NW"
    else:
        for i in range(len(played)):
            if(played[i] == ''):
                data["position"] = board[i]
                break
    logging.info("My move :{}".format(data))
    requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/play/"+battleId, data = json.dumps(data))
