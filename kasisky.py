import sys
import math
from collections import Counter
from tokenize import String

program_name = ""

def searchRepeated(ciphertext , vvFlag ):
   
    found_substrings = {}                               #Diccionario pra almacenar substrings válidos e sua cantidade de repeticions
    res=[]                                              #Lista dos strings repetidos       

    for length in range(len(ciphertext), 2, -1):            #Itera sobre diferentes lonxitudes de substring, empezando dende os mais longos
        counts = {
            k: v 
            for k, v 
            in Counter(
                ''.join(tup) 
                for tup 
                in zip(
                    *(
                    ciphertext[i:] 
                        for i 
                            in range(length)
                    )
                )
            ).items() if v > 1
        }
    
    for k, v in counts.items():                                     #Filtrar substrings que non están dentro dos substrings mais largos xa engadidos
        
        if not any(k in larger for larger in found_substrings):     #Verifica se non hai substrings maiss largos que o contenñan
            found_substrings[k] = v 

    for substring, count in found_substrings.items():
        res.append(substring)
        if vvFlag:                                
                print(f"'{substring}': {count}\n")                    #Modo verboso , para ensinar o proceso
    
    return res

def findDistances(ciphertext, substrings_list , vvFlag ):
    distances = []                                                  #Lista pra almacenar as distancias entre substrings
    
    for substring in substrings_list:                               #Encontra todas as posicions nas que aparece o substring no texto orixinal
        
        positions = [i for i in range(len(ciphertext)) if ciphertext.startswith(substring, i)]
        
        if len(positions) > 1:                                      #Calcula as distancias entre as ocurrencias consecutivas do substring
            for i in range(1, len(positions)):
                distances.append(positions[i] - positions[i - 1])
    
    if vvFlag:
        print(distances)
    return distances

def calculateMCD(distances):
    
    gcds = []                                                       #Lista pra almacear os MCD encontrados
    
    for i in range(len(distances)):                                 #Calcula os MCD para cada par de distancias consecutivas
        for j in range(i + 1, len(distances)):
            gcd = math.gcd(distances[i], distances[j])
            gcds.append(gcd)
    
    return gcds

def analyzeMCD(gcds):
    
    gcd_counts = Counter(gcds)                                      #Conta as ocurrencias de cada MCD
    
    total = sum(gcd_counts.values())
    
    gcd_percentages = {gcd: round((count / total) * 100, 2) for gcd, count in gcd_counts.items()}
    
    
    gcd_percentages = dict(sorted(gcd_percentages.items(), key=lambda item: item[1], reverse=True)) #Ordena os porcentaxes de maior a menor
    
    
    print("Os 10 resultados mais factibles para o tamaño da lonxitude da clave:")                  #Mostrar os primeiros 10 resultados en formato identado
    for i, (gcd, percentage) in enumerate(gcd_percentages.items()):
        if i >= 10:
            break
        print(f"  {gcd}: {percentage}%")

def tryKeySize(length , ciphertext ,vvFlag):

    if (length < 2 or length > 100):
        print("Error: a lonxitude de clave é invalida\n")
        exit(0)

    subalfabetos = ['' for _ in range(length)]
    for i, letra in enumerate(ciphertext):
            subalfabetos[i % length] += letra
    
    for i, letra in enumerate(ciphertext):                                                      #Crea os subalfabetos
        subalfabetos[i % length] += letra

    
    letras_frecuentes = 'EAOSRNIDUTLCPMHGBQVJXZYKWF'                                            #Tecnica EAOS

    claves_posibles = ['' for _ in range(length)]
    
    for i,subalfabeto in enumerate(subalfabetos):                                               #Analisis de cada subalfabeto
        
        if vvFlag:
            print("Subalfabeto numero "+str(i+1))
            print(subalfabeto)
            print("\n")


        contador = Counter(subalfabeto)
        letras_mas_frecuentes = [letra for letra, _ in contador.most_common(8)]                 #Modificar para axustar nivel de precision

        if vvFlag:
            print("Letras mais comuns do alfabeto numero "+str(i+1)+" :")
            print(letras_mas_frecuentes)
            print("\n")

        if len(letras_mas_frecuentes) < 2:                                                      #Non hai suficientes datos pra determinar o desplazamento
            print(f"Subalfabeto {i+1} ten menos de duas letras frecuentes. Sera omitido.\n")
            continue  

        segunda_mas_frecuente = letras_mas_frecuentes[1]
        tercera_mas_frecuente = letras_mas_frecuentes[2]
        
        # Probar cada letra frecuente como posible mapeo a 'E' o 'A'
        for letra_frecuente in letras_mas_frecuentes:
            # Asumir que la letra frecuente corresponde a 'E'
            shift_e = (ord(letra_frecuente) - ord('E')) % 26
            matchE = []
            matchE.append(chr(ord('E') + shift_e))                            #E
            matchE.append(chr(ord('A') + shift_e))                            #A
            matchE.append(chr(((ord('O') + shift_e)-ord('A'))%26 + ord('A'))) #O
            matchE.append(chr(((ord('S') + shift_e)-ord('A'))%26 + ord('A'))) #S

            
        
            if vvFlag:
                    print(f"Hipotesis es que '{letra_frecuente}' corresponde a 'E'. Desplazamiento: {shift_e}. Letras mas proabables: {matchE[1]}-->({'A'}) , {matchE[2]}-->({'O'}) y {matchE[3]}-->({'S'})\n")

            if ( compareFrec(matchE,letras_mas_frecuentes)>=3 ) :
                # Clave encontrada asumiendo 'E'
                clave = chr(shift_e + ord('A'))
                claves_posibles[i]= clave
                if vvFlag:
                    print(f"Hipoteis verificada '{letra_frecuente}' corresponde a 'E'. Desplazamiento: {shift_e}. Letra clave: {clave}")
                    print("\n\n")
                break  # Se encontró la clave para este subalfabeto

            # Asumir que la letra frecuente corresponde a 'A'
            shift_a = (ord(letra_frecuente) - ord('A')) % 26
            matchA = []
            matchA.append(chr((ord('E') + shift_a)))                          #E
            matchA.append(chr(ord('A') + shift_a))                            #A
            matchA.append(chr(((ord('O') + shift_a)-ord('A'))%26 + ord('A'))) #O
            matchA.append(chr(((ord('S') + shift_a)-ord('A'))%26 + ord('A'))) #S
            
            if vvFlag:
                    print(f"Hipotesis es '{letra_frecuente}' corresponde a 'A'. Desplazamiento: {shift_a}. Letras mas proabables: {matchA[0]}-->({'E'}) , {matchA[2]}-->({'O'}) y {matchA[3]}-->({'S'})\n")

            if ( compareFrec(matchA,letras_mas_frecuentes)>=3 ) :
                # Clave encontrada asumiendo 'A'
                clave = chr(shift_a + ord('A'))
                claves_posibles[i]= clave
                if vvFlag:
                    print(f"Hipoteis verificada '{letra_frecuente}' corresponde a 'A'. Desplazamiento: {shift_a}. Letra clave: {clave}")
                    print("\n\n")
                break  # Se encontró la clave para este subalfabeto

            # Asumir que la letra frecuente corresponde a 'O'
            shift_o = (ord(letra_frecuente) - ord('O')) % 26
            matchO = []
            matchO.append(chr(((ord('E') + shift_o)-ord('A'))%26 + ord('A'))) #E
            matchO.append(chr(((ord('A') + shift_o)-ord('A'))%26 + ord('A'))) #A
            matchO.append(chr(ord('O')+shift_o))                              #O
            matchO.append(chr(((ord('S') + shift_o)-ord('A'))%26 + ord('A'))) #S
            
            if vvFlag:
            
                    print(f"Hipotesis es '{letra_frecuente}' corresponde a 'O'. Desplazamiento: {shift_o}.  Letras mas proabables: {matchO[1]}-->({'A'}) , {matchO[0]}-->({'E'}) y {matchO[3]}-->({'S'})\n")


            if ( compareFrec(matchO,letras_mas_frecuentes)>=3 ) :
                # Clave encontrada asumiendo 'O'
                clave = chr(shift_o + ord('A'))
                claves_posibles[i]= clave
                if vvFlag:
                
                    print(f"Hipoteis verificada '{letra_frecuente}' corresponde a 'O'. Desplazamiento: {shift_o}. Letra clave: {clave}")
                    print("\n\n")
                break  # Se encontró la clave para este subalfabeto

            # Asumir que la letra frecuente corresponde a 'S'
            shift_s = (ord(letra_frecuente) - ord('S')) % 26
            matchS = []
            matchS.append(chr(((ord('E') + shift_s)-ord('A'))%26 + ord('A'))) #E
            matchS.append(chr(((ord('A') + shift_s)-ord('A'))%26 + ord('A'))) #A
            matchS.append(chr(((ord('O') + shift_s)-ord('A'))%26 + ord('A'))) #O
            matchS.append(chr(ord('S')+shift_s))                              #S
            
            if vvFlag:
            
                    print(f"Hipotesis es '{letra_frecuente}' corresponde a 'S'. Desplazamiento: {shift_s}.  Letras mas proabables: {matchS[0]}-->({'E'}) , {matchS[1]}-->({'A'}) y {matchS[2]}-->({'O'})\n")


            if ( compareFrec(matchS,letras_mas_frecuentes)>=3 ) :
                # Clave encontrada asumiendo 'O'
                clave = chr(shift_s + ord('A'))
                claves_posibles[i]= clave
                if vvFlag:
                
                    print(f"Hipoteis verificada '{letra_frecuente}' corresponde a 'S'. Desplazamiento: {shift_s}. Letra clave: {clave}")
                    print("\n\n")
                break  # Se encontró la clave para este subalfabeto
            break

    return claves_posibles

def compareFrec(str1,str2):

    cnt=0
    
    for i in range(len(str2)):

        for z in range(len(str1)):
            if ord(str2[i])==ord(str1[z]):
                cnt=cnt+1
    return cnt

def isValidChar(text):

    validChars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    chars = list(text)
    for char in chars:
     try:
        validChars.index(char)
     except:
         print("Erro: o texto ou chave contéñen un caracter NON permitido. Consulta o alfabeto permitido con --alphabet\n")
         print(char+" in position "+str(text.index(char)))
         exit(0)

def auxFileName(list):
    try:
        return list.index("--file")+1
    except:
        return -1

def cli(args):

    vvFlag=False                                            #Modo verboso , para unha maior comprension do programa

    if len(sys.argv[1:]) == 0:
        print("\nFaltan parametros , proba con --help")
        exit(1)

    while 1:
        for arg in sys.argv[1:]:
         match arg:
            case "--help":
                print(f"\nAnaliza un texto cifrado con Vignere para obter a lonxitude da clave coa que se cifrou:"
                      f"\n\n{{ --verbose | --vv }}"                                  
                      f"\t\t\t\tModo de execucion con informacion adicional do proceso de criptnoalise. ( Debe especificarse antes de --file )\n"
                      f"\t\t\t\t\t\tADVERTENCIA: este modo devolvera unha GRAN cantidade de informacion."
                      f"\n\n{{ --file NOME_ARQUIVO  }}"                                  
                      f"\t\t\tEspecifica o nome do arquivo que conten o texto cifrado , debe estar no alfabeto permitido ( --alphabet )\n"
                      f"\n\n{{ --trylen TAMAÑO_CLAVE  NOME_ARQUIVO}}"                                  
                      f"\t\tObten unha posible clave para un tamaño de clave dado\n")
                exit(0)

            case "--alphabet":
                print(f"\nO alfabeto permitido consta de 26 caracteres en MAIUSCULA:"
                      f"\n\n\tA B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n")
                exit(0)


            case "--file":

                currPos= sys.argv[1:].index(arg)                                    #Colle a posicion do actual elemento entre os argumentos de entrada. Indexado dende CERO.
                argsLen= len(sys.argv[1:])                                          #Colle o numero de todos os argumentos pasados por liña de comandos.
                repTokens = []                                                      #Os strings repetidos no texto cifrado
                distances = []                                                      #AS distancias dos strings repetidos no texto cifrado

                if ( currPos+1 == argsLen ):                                        #Comproba que quede polo menos un argumento mais 
                    print("Erro: non se achega unha fonte para analizar\n")
                    exit(0)
                                                            
                
                with open(sys.argv[1:].pop(currPos+1), 'r') as file:
                        content = file.read()

                isValidChar(content)
                repTokens=searchRepeated(content,vvFlag)
                distances=findDistances(content,repTokens,vvFlag)
                analyzeMCD(calculateMCD(distances))
                
                exit(0)

            case "--verbose":
                 vvFlag=True
            case "--vv":
                 vvFlag=True    
            case "--trylen":

                currPos= sys.argv[1:].index(arg)                                    #Colle a posicion do actual elemento entre os argumentos de entrada. Indexado dende CERO.
                argsLen= len(sys.argv[1:])                                          #Colle o numero de todos os argumentos pasados por liña de comandos.
                res = ""

                if ( currPos+2 == argsLen ):                                        #Comproba que quede polo menos dous argumentos mais 
                    print("Erro: non se achega unha fonte ou tamaño de clave para analizar\n")
                    exit(0)

                with open(sys.argv[1:].pop(currPos+2), 'r') as file:
                        content = file.read()

                isValidChar(content)
                res=tryKeySize(int(sys.argv[1:].pop(currPos+1)),content , vvFlag)
                print("Clave posibles para longitud "+sys.argv[1:].pop(currPos+1)+":\n")
                print(res)

                exit(0)

            case _:
                 exit(0)
                     

if __name__ == "__main__":
    cli(sys.argv)
