#include <stdio.h>
#include <string.h>
char name[0x30];
void init(void){
	setvbuf(stdin, 0LL, 2, 0LL);
  	setvbuf(stdout, 0LL, 2, 0LL);
	setvbuf(stderr, 0LL, 2, 0LL);
}
int main(void){
	init();
	char st[0x30];
	puts("what's your name?");
	read(0,name,0x20);
	puts("what do you want?");
	read(0,st,0x40);
	return 0;
}