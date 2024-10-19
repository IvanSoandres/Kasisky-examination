# Kasisky-examination
### A Python-based implementation of the Kasisky method for cracking a Vignere ciphered text.
### Usage:

```
python.exe kasisky.py --file FILE_NAME.txt

```

A successful execution will yield a list of the **10 most probable key lengths** for the given texts, displaying the ones with the highest percentage first. Additionally, a verbose flag ( --vv ) may be used to see the repeated tokens and their G.C.D.

```

python.exe kasisky.py --trylen KEY_LENGTH  FILE_NAME.txt

```

A successful execution will yield the most likely key to the specified length. Verbose mode is **strongly recommended** for this operation as it will display each operation made, such as creating an array composed of the most frequent characters and then trying to match them with the most frequent characters in the alphabet. 

>NOTICE:
The code is set to work for the most frequent characters in the [castillian-spanish alphabet](https://es.wikipedia.org/wiki/Frecuencia_de_aparici%C3%B3n_de_letras) however this may be easily modified inside _tryKeySize_ method.

