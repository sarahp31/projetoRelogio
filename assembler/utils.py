from typing import Dict

mne =	{ 
       "NOP":   "0000",
       "LDA":   "0001",
       "SOMA":  "0010",
       "SUB":   "0011",
       "LDI":   "0100",
       "STA":   "0101",
       "JMP":   "0110",
       "JEQ":   "0111",
       "CEQ":   "1000",
       "JSR":   "1001",
       "RET":   "1010",
       "ANDI":  "1011",
       "INC":   "1100"
}

def formatToVHDL(cont, instrucaoLine, comentarioLine):
    '''
    Formata para o arquivo BIN
    Entrada => 1. JSR @14 #comentario1
    Saída =>   1. tmp(0) := x"90E";	-- JSR @14 	#comentario1
    '''

    return 'tmp(' + str(cont) + ') := "' + instrucaoLine + '";\t-- ' + comentarioLine + '\n' 

def procuraLabels(lines_asm:list) -> dict:
    '''
    Vasculha o documento por labels e adiciona
    os endereços em um dicionário
    '''
    par_label_linha: Dict[str, str] = dict()
    numero_de_linha = 0
    
    for line in lines_asm:
        if not(line.startswith('\n') or line.startswith(' ') or line.startswith('#')):
            line_instrucao = defineInstrucao(line=line)
            if ':' in line_instrucao:
                nome_label = line_instrucao.split(':')[0]
                par_label_linha[nome_label] = numero_de_linha
            numero_de_linha += 1
    
    return par_label_linha

def converteArroba(line:str, par_label_linha:dict) -> str:
    '''
    Transforma o endereço em decimal depois do arroba
    em binário com 9 bits (8 downto 0)

    Argumentos:
     - line: linha com instrução @ (ex: JSR @10)
    '''
    line = line.split('@')

    if line[0]=='011000' or line[0]=='011100' or line[0]=='100100':
        label = line[1]
        line[1] = par_label_linha[label]
        
    line[1] = bin(int(line[1]))[2:].upper().zfill(9)
    line = ''.join(line)
    return line

def  converteCifrao(line):
    '''
    Transforma o endereço em decimal depois do arroba
    em binário com 9 bits (8 downto 0)

    Argumentos:
     - line: linha com instrução $ (ex: LDI $10)
    '''
    line = line.split('$')
    line[1] = bin(int(line[1]))[2:].upper().zfill(9)
    line = ''.join(line)
    return line
        
def defineComentario(line):
    '''
    Define a string que representa o comentário
    a partir do caractere cerquilha '#'
    '''
    if '#' in line:
        line = line.split('#')
        line = line[0] + "\t#" + line[1]
        return line
    else:
        return line

def defineInstrucao(line):
    '''
    Remove o comentário a partir do caractere cerquilha '#',
    deixando apenas a instrução
    '''
    line = line.split('#')
    line = line[0]
    return line
    
def trataMnemonico(line):
    '''
    Consulta o dicionário e "converte" o mnemônico em
    seu respectivo valor em hexadecimal
    Argumentos: line
    '''
    line = line.replace("\n", "") #Remove o caracter de final de linha
    line = line.replace("\t", "") #Remove o caracter de tabulacao
    line = line.split(' ')
    line[0] = mne[line[0]]
    line = "".join(line)
    return line

def trataRegistradores(line:str):
    '''
    Trata presença de R0, R1, R2, R3
    '''
    print('Tentando com', line)
    
    line = line.replace(',', '')

    if 'R1' in line:
        line = line.replace('R1', '')
        line1 = line[:4]
        line2 = line[4:]
        line = line1 + '01' + line2
    elif 'R2' in line:
        line = line.replace('R2', '')
        line1 = line[:4]
        line2 = line[4:]
        line = line1 + '10' + line2
    elif 'R3' in line:
        line = line.replace('R3', '')
        line1 = line[:4]
        line2 = line[4:]
        line = line1 + '11' + line2
    else:
        line = line.replace('R0', '')
        line1 = line[:4]
        line2 = line[4:]
        line = line1 + '00' + line2
    
    return line
