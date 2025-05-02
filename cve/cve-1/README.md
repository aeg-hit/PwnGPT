# Vulnerable Packages
A repository containing docker images of vulnerable packages (e.g. backdoored vsftpd) etc. for testing exploits/scanners and to not waste time on dependencies and shit.

## Vsftpd 2.3.4 (backdoored)
It was backdoored and the trigger was `:)` in username which starts a bind shell on port **6200**, executing the shell gives remote root access to anyone connecting to that port.

#### Manually Building & Running (docker image):

```bash
git clone https://github.com/Anon-Exploiter/vulnerable-packages
cd vulnerable-packages
cd backdoored-vsftpd-2.3.4
docker build -t backdoored-vsftpd-2.3.4 .
docker run -it --rm -p 21:21 -p 6200:6200 backdoored-vsftpd-2.3.4
```

#### Cloning & running from Docker hub (docker image):
```bash
docker run -it --rm -p 21:21 -p 6200:6200 uexpl0it/vulnerable-packages:backdoored-vsftpd-2.3.4
```
