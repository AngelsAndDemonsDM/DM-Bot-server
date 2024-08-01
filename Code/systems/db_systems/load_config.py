import logging
from typing import Tuple

from systems.db_systems.settings import MainSettings

logger = logging.getLogger("Settings manager")

def load_config() -> Tuple[str, int, int, bool]:
    logger.info("Start load settings")
    
    host: str = "127.0.0.1"
    port: int = 5000
    socket_port: int = 5001
    auto_update: bool = False
    
    with MainSettings() as config:
        if not config.initialize_default_settings({
                "app.auto_git_update": False,
                "server.name": "dev_server",
                "server.ip": "127.0.0.1",
                "server.http_port": 5000,
                "server.socket_port": 5001,
            }):
            logger.info(f"Server name: {config.get_setting('server.name')}")
            
            host = config.get_setting("server.ip")
            logger.info(f"IP: {host}")
            
            port = config.get_setting("server.http_port")
            logger.info(f"HTTP port: {port}")
            
            socket_port = config.get_setting("server.socket_port")
            logger.info(f"Soket server port: {socket_port}")
            
            auto_update = config.get_setting("app.auto_git_update")
            logger.info(f"Auto update is enable: {auto_update}")
            
            logger.info(f"Config set.")
        
        else:
            logger.info(f"Base config set.")
        
    return host, port, socket_port, auto_update
