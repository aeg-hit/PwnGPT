# COMPFEST CTF 2020: Binary Exploitation is Ez

# Solve
this is an easy challenge, there is buffer overflow in edit_mem().
```c
void edit_meme()	{
	unsigned int idx;
	printf("Index: ");
	idx = read_int();
	if(memes[idx] == NULL)	{
		puts("There's no meme there!");
		return;
	}
	printf("Enter meme content: ");
	gets(memes[idx]->content); //here
	puts("Done!");
}
```
and my_print() is stored on the heap that close to our input
```c
void new_meme()	{
	unsigned int size;
	printf("Enter meme size: ");
	size = read_int();
	if(size > 0x200)	{
		puts("Please, noone wants to read the entire bee movie script");
		exit(-1);
	}
	int i = 0;
	while(memes[i] != NULL && ++i < 8);
	if(i == 8)	{
		puts("No more memes for you!");
		exit(-1);
	}
	memes[i] = malloc(8);
	memes[i]->func = &my_print; //here
	memes[i]->content = malloc(size);
	printf("Enter meme content: ");
	fgets(memes[i]->content, size, stdin);
	puts("Done!");
}
```
in print_meme() function, my_print() is being called to print our content from heap
```c
void print_meme()	{
	unsigned int idx;
	printf("Index: ");
	idx = read_int();
	if(memes[idx] == NULL)	{
		puts("There's no meme there!");
		return;
	}
	(*(memes[idx]->func))(memes[idx]->content);
}
```
so, we can use buffer overflow in edit_mem() to overwrite my_print() with EZ_WIN() function and then call print_mem(), so that we can get a shell