from re import sub
from xml.etree.ElementTree import SubElement


number = -0.841600711036728
long = -73.99116596577247


def divide (number):
    number = number/3
    return number

def subtract (number):
    number = number - 3.14
    return number

def add (number):
    number = number + 5
    return number
    
def multiply (number):
    number = number * 1 * 2 * 3 * 4 * 5
    return number

with open('latitude.txt', 'w') as file:

    file.write(str((divide(subtract(add(multiply(number)))))))

    file.write('\n')

    file.write(str((divide(subtract(multiply(add(number)))))))

    file.write('\n')

    file.write(str((divide(add(subtract(multiply(number)))))))

    file.write('\n')

    file.write(str((divide(add(multiply(subtract(number)))))))

    file.write('\n')

    file.write(str((divide(multiply(add(subtract(number)))))))

    file.write('\n')

    file.write(str((divide(multiply(subtract(add(number)))))))

    file.write('\n')

    file.write(str((subtract(multiply(add(divide(number)))))))

    file.write('\n')

    file.write(str((subtract(multiply(divide(add(number)))))))

    file.write('\n')    

    file.write(str((subtract(divide(multiply(add(number)))))))

    file.write('\n')

    file.write(str((subtract(divide(add(multiply(number)))))))

    file.write('\n')

    file.write(str((subtract(add(multiply(divide(number)))))))

    file.write('\n')

    file.write(str((subtract(add(divide(multiply(number)))))))

    file.write('\n')

    file.write(str((add(subtract(divide(multiply(number)))))))

    file.write('\n')

    file.write(str((add(subtract(multiply(divide(number)))))))

    file.write('\n')

    file.write(str((add(multiply(subtract(divide(number)))))))

    file.write('\n')

    file.write(str((add(multiply(divide(subtract(number)))))))

    file.write('\n')

    file.write(str((add(divide(multiply(subtract(number)))))))

    file.write('\n')

    file.write(str((add(divide(subtract(multiply(number)))))))

    file.write('\n')

    file.write(str((multiply(add(divide(subtract(number)))))))

    file.write('\n')

    file.write(str((multiply(add(subtract(divide(number)))))))

    file.write('\n')

    file.write(str((multiply(subtract(add(divide(number)))))))

    file.write('\n')

    file.write(str((multiply(subtract(divide(add(number)))))))

    file.write('\n')

    file.write(str((multiply(divide(subtract(add(number)))))))

    file.write('\n')

    file.write(str((multiply(divide(add(subtract(number)))))))


