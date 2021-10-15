#Mohammad Abolnejadian - 98103867
#Matin Daghyani - 98106456

from scanner import Scanner

scanner = Scanner()
while(True):
    a = input()
    if a == 'a':
        scanner.print_token()
    end = scanner.get_next_token()
    if end:
        break