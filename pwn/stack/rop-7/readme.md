#解题思路
一开始认为把'sh\x00'放到rdi就可以调用system了，实际上system参数是指针，需要字符串所在地址。就想搞esp和ebp地址到栈里面，误入歧途。看别人的发现是有一个write_str函数可以利用，有个全局变量str。