import sys

def error(inputData):
    if len(inputData.split(' ')) != 2:
        return True
    return False


def file_handling(command, fileName, message):
    if command == 'start':
        o = open(fileName, "r+")
        content = o.read()
        o.seek(0, 0)
        o.write(message.rstrip('\r\n') + " " + content)
        o.close()
    elif command == 'end':
        o = open(fileName, "a")
        o.write(" " + message)
        o.close()
    else:
        return 'wrong argument'


def main(inputData, message):
    if error(inputData):
        print('wrong input')

    fileName, command = inputData.split(' ')

    file_handling(command, fileName, message)

main(sys.argv[1], sys.argv[2])