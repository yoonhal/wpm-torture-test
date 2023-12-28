from dotenv import load_dotenv

# All Configurations
def configure():
    load_dotenv()


# Takes String 'input' and returns all digit values as an int in given order
def to_numbers(input):

    if input == '':
        return 0
    
    number = ''
    for c in input:
        if (c.isdigit()):
            number = number + c
            
    if number == '':
        return 0

    return int(number)