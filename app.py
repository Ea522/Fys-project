from flask import Flask
import RPi.GPIO as GPIO
import time, json, logging, websockets, os, asyncio
app = Flask(__name__)

#@app.route("/")
#def index():
    #return "Index!"


GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
#linker
ldr1 = 7
ldr2 = 8
ldr3 = 10
#middelst
ldr4 = 11
ldr5 = 12
ldr6 = 13
#rechter
ldr7 = 15
ldr8 = 16
ldr9 = 18

left_arr = []
center_arr = []
right_arr = []

async def rc_time (websocket, ldr):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(ldr, GPIO.OUT)
    GPIO.output(ldr, GPIO.LOW)
    #GPIO.output(ldr1, False)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(ldr, GPIO.IN)
  
    #Count until the pin goes high
    #while (GPIO.input(ldr1) == GPIO.LOW):
    while (GPIO.input(ldr1) == 0):
        count += 1

    return count

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()
        
async def main(websocket, path):
    #Catch when script is interupted, cleanup correctly
    try:
        # Main loop
        while True:
            
            #print('ldr1', rc_time(ldr1))
            first = rc_time(websocket, ldr1)
            print('first:',rc_time(ldr1))
            time.sleep(0.5)
            second = rc_time(ldr1)
            print('second:',rc_time(ldr1))
            if second - first > 1000:
                print('ik kom van links')
            #print('ldr2',rc_time(ldr2))
            #print('ldr3',rc_time(ldr3))
            #print('ldr4',rc_time(ldr4))
            #print('ldr5',rc_time(ldr5))
            #print('ldr6',rc_time(ldr6))
            #print('ldr7',rc_time(ldr7))
            #print('ldr8',rc_time(ldr8))
            #print('ldr9',rc_time(ldr9))
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

start_server = websockets.serve(main, "localhost", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
if __name__ == "__main__":
    main()
