import logging
import socket

def checkSocket(*args, port) -> None:
  for url in set(args):
    sock = socket.socket()
    try:
      sock.connect((url,port))
      logging.info("Succesfully contacted socket on port %s for %s", port, url)
      sock.close()
    except Exception as error:
      sock.close()
      logging.error("Error %s while connecting to socket for %s", error, url)
      return False
  return True
