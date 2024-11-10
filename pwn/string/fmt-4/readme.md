# 动态链接
call scanf —> scanf的plt表 —>scanf的got表
把获取数据段存放函数地址的那一小段代码称为PLT（Procedure Linkage Table）
过程链接表存放函数地址的数据段称为GOT（Global Offset Table）全局偏移表

1. findstraddr.py通过pwntool获取`格式字符串`在printf函数里参数的顺序 
2. `p32(printf_got)+b'%6$s'`读数据
3. `fmtstr_payload(6,{printf_got:system_addr})`构造往`printf_got`地址中写入`system_addr`的字符串（通过%n）
4. 最后调用printf时由于got表被替换为了`system_addr`，变为输入"/bin/sh\0"调用system函数