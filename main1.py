import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

# Enviroments Variables
NAuserIds = os.environ['NAuserIds'].split(',')
NAauthkeys = os.environ['NAauthkeys'].split(',')
NAsecretkeys = os.environ['NAsecretkeys'].split(',')
NAfate_region = os.environ['NAfateRegion']
NAwebhook_discord_url = os.environ['NAwebhookDiscord']
NAUA = os.environ['NAUserAgent']

if UA != 'nullvalue':
    fgourl.user_agent_ = NAUA

userNums = len(NAuserIds)
authKeyNums = len(NAauthkeys)
NAsecretkeyNums = len(NAsecretkeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def get_latest_verCode():
    endpoint = ""

    if NAfate_region == "NA":
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/NA/VerCode.json"
    else:
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/JP/VerCode.json"

    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    if userNums == authKeyNums and userNums == NAsecretkeyNums:
        logger.info('Getting Lastest Assets Info')
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(NAuserIds[i], NAauthkeys[i], NAsecretkeys[i])
                time.sleep(3)
                logger.info('Loggin into account!')
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                logger.info('Throw daily friend summon!')
                instance.drawFP()
                time.sleep(2)
            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
