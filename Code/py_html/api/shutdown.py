import asyncio
import logging
import os
import signal

from bot import bot_close
from flask import Blueprint, jsonify
from py_html.api.register_api import api_bp


@api_bp.route('/shutdown', methods=['GET'])
def shutdown_start():
    logging.info("Start shutdown systems")
    asyncio.run(shutdown_systems())
    
    logging.info("Exit program")
    shutdown_server()
    return jsonify({'message': 'Logout successful'})

def shutdown_server():
    # Отправка сигнала SIGINT самому себе. Откровенно говоря выглядит как хуйня
    os.kill(os.getpid(), signal.SIGINT)

async def shutdown_systems():
    logging.info("Shutdown discord bot")
    await bot_close()
