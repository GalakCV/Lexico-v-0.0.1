import re
import sys

token_specs = [
    ("NUMERO_REAL", r"\d+\.\d+"),
    ("NUMERO_INTEIRO", r"\d+"),
    ("PALAVRA_RESERVADA", r"\b(inteiro|real|se|entao|senao|enquanto|repita|ate|ler|mostrar)\b"),
    ("OPERADOR", r"==|!=|<=|>=|\+|\-|\*|/|=|<|>|\|\||&&"),
    ("DELIMITADOR", r"[;,(){}]"),
    ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NOVA_LINHA", r"\n"),
    ("ESPACO", r"[ \t]+"),
    ("MISMATCH", r".")  
]

token_regex = "|".join(f"(?P<{nome}>{regex})" for nome, regex in token_specs)

def get_token(codigo):
    
    linha = 1
    for m in re.finditer(token_regex, codigo):
        tipo = m.lastgroup
        valor = m.group()
        if tipo == "NOVA_LINHA":
            linha += 1
        elif tipo == "ESPACO":
            continue
        elif tipo == "MISMATCH":
            raise RuntimeError(f"Caractere inválido '{valor}' na linha {linha}")
        else:
            yield (tipo, valor, linha)

def main():
    if len(sys.argv) < 2:
        print("Uso: python lexer.py <arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)

    for tipo, valor, linha in get_token(codigo):
        print(f"('{tipo}', '{valor}', linha {linha})")

if __name__ == "__main__":
    main()
