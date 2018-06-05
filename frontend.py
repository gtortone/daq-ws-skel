from threading import Thread
import asyncio
import time
from enum import Enum
from flask_socketio import SocketIO, emit

class rcstatus(Enum):
   STOPPED = 1
   RUNNING = 2
   PAUSED = 3

class Frontend:

   def __init__(self, sio_ctx):
      self.sio = sio_ctx
      self.rcs = rcstatus.STOPPED
      self.frontend_loop = asyncio.new_event_loop()
      self.t = Thread(target=self.start_loop, args=(self.frontend_loop,))
      self.t.start()
      asyncio.run_coroutine_threadsafe(self.acquire(1), self.frontend_loop)

   def start_loop(self, loop):
      asyncio.set_event_loop(loop)
      loop.run_forever()

   def start(self):
      self.rcs = rcstatus.RUNNING
   
   def stop(self):
      self.rcs = rcstatus.STOPPED

   def pause(self):
      self.rcs = rcstatus.PAUSED 
   
   async def acquire(self, x):
      ev = 0
      while True:
         if self.rcs == rcstatus.RUNNING:
            print("ev : {}".format(ev))
            if self.sio is not None:
               self.sio.emit('event', 
                  {'data': 'DAQ event', 'evnum': ev}, namespace='/daq')
            ev = ev + 1
            await asyncio.sleep(1)
         elif self.rcs == rcstatus.PAUSED:
            await asyncio.sleep(1)
         elif self.rcs == rcstatus.STOPPED:
            await asyncio.sleep(1)

if __name__ == '__main__':

   f = Frontend(None)

   frontend_loop = asyncio.new_event_loop()
   t = Thread(target=f.start_loop, args=(frontend_loop,))
   t.start()

   f.start()

   asyncio.run_coroutine_threadsafe(f.acquire(1), frontend_loop)