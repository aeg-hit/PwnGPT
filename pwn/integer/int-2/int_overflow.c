#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <sys/mman.h>

char passwd_buf[500];

void check(unsigned char passwd_len,char* passwd)
{
    if(passwd_len >= 4 && passwd_len <= 8) 
    {
        printf("good!\n");
        strcpy(passwd_buf, passwd);
        // 获取 passwd_buf 所在页的起始地址
        void *page_start = (void *)((unsigned long)passwd_buf & ~(getpagesize()-1));
        // 将该页设置为可读、可写、可执行
        if (mprotect(page_start, getpagesize(), PROT_READ | PROT_WRITE | PROT_EXEC) == -1)
        {
            perror("mprotect");
            exit(1);
        }
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
    printf("##### Welcome to LLM4CTF #####\n");
    printf("Plz input your passwd:\n");
    validate_passwd();
    return 0;
}