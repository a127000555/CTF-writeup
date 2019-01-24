#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <byteswap.h>
int main(){
	char s[1024];
	scanf("%s",s);
	unsigned int l=strlen(s);
	for(unsigned i=0;i<l;i++){
		int x = 0;
		for(int j=0;j<8;j++){
			if (s[i] & (1<<j) ){
				x |= (1<<(7-j));
			}
		}
		printf("%x | %x\n",s[i],x);
	}
	return 0;
}