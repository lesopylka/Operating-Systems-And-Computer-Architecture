import sys
#Написать скрипт, который сравнивает два числа, заданные при его запуске и выдает результат в виде строки:
# <число1> больше(меньше)(равно) <число2>

def error(inputData):
    if len(inputData.split(' ')) != 2:
        return True
    return False


def comparison(firstNumber, secondNumber):
        if firstNumber > secondNumber:
            return(f"{firstNumber} больше {secondNumber}")
        elif firstNumber < secondNumber:
            return(f"{firstNumber} меньше {secondNumber}")
        else:
            return(f"{firstNumber} равно {secondNumber}")


def main(inputData):
    if error(inputData):
        print('wrong input')

    firstNumber, secondNumber = map(int, inputData.split(' '))

    print(comparison(firstNumber, secondNumber))    

main(sys.argv[1])