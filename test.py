import os
import random

smile = ''
for i in range(random.randint(5, 10)):
    smile += 'ha '

while True:
    os.system('say "tell me a joke"')
    raw_input('hit enter')
    os.system('say "%s"' % smile)
    raw_input('hit enter')
