#include <unistd.h>
#include <stdio.h>
char s[22000];
int main(){
	read(0,s,2000);
	int (*func)();
	func = (int (*)())s;
	(int)(*func)();
	return 0;
}