get_started_3dsctf_2016
# 32位程序给函数传递参数时，参数是在返回地址的高处的。所以payload是'a'*offset  + get_flag地址 + get_flag的返回地址 + 参数1 + 参数2

# get_flag的返回地址，这个地址不能乱写，打远程时，如果程序是异常退出了，最后是不给你回显的。所以我们得想办法让程序正常退出。（C语言有个函数是exit）

# 方法2使用mprotect将内存改为可执行