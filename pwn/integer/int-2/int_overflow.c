#include<stdio.h>
#include<string.h>

char passwd_buf[500];

void check(unsigned char passwd_len,char* passwd)
{
    if(passwd_len >= 4 && passwd_len <= 8) 
    {
        printf("good!\n");
        strcpy(passwd_buf, passwd);
    } 
    else 
    {
        printf("bad!\n");
    }
}
void validate_passwd(void)
 {
    char passwd[50];
    gets(passwd);

    unsigned char passwd_len = strlen(passwd);
    check(passwd_len,passwd);
}
int main() 
{
    printf("##### Welcome to MOCSCTF #####\n");
    printf("Plz input your passwd:\n");
    validate_passwd();
    return 0;
}