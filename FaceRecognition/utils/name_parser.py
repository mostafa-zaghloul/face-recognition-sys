# take image name and handle it to be the detected face idintity name.
#called by who is it fun

def get_name(identity_string):
    file_name = identity_string
    name = file_name
    for i in file_name:
        if(i == '_' or i == '-' or i == '(' or i == ')' or i == '#' or i == '@' or i == '&' or i == '%' or i == '!' or i == '*' or i == '/' or i == '\\' or i == '^' or i == '$' or i == '?' or i == '.' or i == ',' or i == '[' or i == ']' or i == '{' or i == '}' or i == '<' or i == '>' or i == '~'):
            name = name.replace(i," ")
        elif(i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9'):
            name = name.replace(i,"")
    return name

