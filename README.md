# Pohlig-Hellman in Python
## Description
A python program which uses the Pohlig-Hellman method to recover the private key x in b = a^x mod p (Discrete Log problem). 
I wrote this code to solve a Root-Me challenge (Discrete Log).


## Usage
### Argv
To use this code, you can provide a, b, p from $b = a^x mod p$ in the program arguments:
```
python attack.py <b> <a> <p>
```
And then select the otion 1 among these options:
```
Options:
	1 - read argv values
	2 - read file
```
### File
The second way to provide your params is to write into a file your parameters (no order required).
Here is an example:
```
a=2862392356922936880157505726961027620297475166595443090826668842052108260396755078180089295033677131286733784955854335672518017968622162153227778875458650593
b=6289736695712027841545587266292164172813699099085672937550442102159309081155467550411414088175729823598108452032137447608687929628597035278365152781494883808
p=7863166752583943287208453249445887802885958578827520225154826621191353388988908983484279021978114049838254701703424499688950361788140197906625796305008451719
```
When your file respect this format, you can choose the option 2:
```
Options:
	1 - read argv values
	2 - read file
```
and enter the file name.
