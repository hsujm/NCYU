//============================================================================
// Name        : 1023008-hw3.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
using namespace std;

int mul_n2one( int n ){
	if( n == 1 )
		return 1;
	return n* mul_n2one(n-1);
}

int main(void) {
	int num;
	cout << "Please input a number n, The program will give you n!. If input the zero, exit the program.\n";
	while( cin >> num ){
		if( !num )
			return 0;
		cout << "n!=" << mul_n2one( num ) << endl;
		cout << "\nPlease input a number n, The program will give you n!. If input the zero, exit the program.\n";
	}
}
