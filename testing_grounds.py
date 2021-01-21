from pynput import keyboard
import time



def on_press(key):
    if key == keyboard.Key.space:
        global user_input
        user_input = True
        print('pressed')

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press)
listener.start()

start_time = time.time()
c = 0
user_input = False
while (time.time() - start_time < 10) & (not user_input):
    time.sleep(1)
    c += 1
    print(f'{c} : {user_input}')
listener.stop()
print('Done')
