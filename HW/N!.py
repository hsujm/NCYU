'''
Created on 2015年10月18日

@author: root
'''

def main():
    while True:
        num = input( 'Please input a number n, The program will give you n!. If input the zero, exit the program.\n' )
        if num == 0:
            break
        n = 1
        for x in range( 1, int(num) ):
            n *= x
        print( 'n! = {}\n'.format( n ) )
            

if __name__ == '__main__':
    main()
