import sqlite3
import os

# Caminho correto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def cadastrar_uf():
    nome_estado = ['Acre',
'Alagoas',
'Amapá',
'Amazonas',
'Bahia',
'Ceará',
'Distrito Federal',
'Espirito Santo',
'Goiás',
'Maranhão',
'Mato Grosso do Sul',
'Mato Grosso',
'Minas Gerais',
'Pará',
'Paraíba',
'Paraná',
'Pernambuco',
'Piauí',
'Rio de Janeiro',
'Rio Grande do Norte',
'Rio Grande do Sul',
'Rondônia',
'Roraima',
'Santa Catarina',
'São Paulo',
'Sergipe',
'Tocantins'] 
    uf_estado = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    for nome, uf in zip(nome_estado, uf_estado):
        cursor.execute("INSERT INTO painel_estados (nome, uf) VALUES (?, ?)", (nome, uf))
        print(f"Adicionado estado: {nome} - {uf}")
    conn.commit()
    print(f"\nTotal de {len(nome_estado)} estados adicionados com sucesso!")

def cadastrar_tipo_conselho():
    tipos = ['CRM', 'CRP', 'CRN', 'CREFITO']
    for tipo in tipos:
        cursor.execute("INSERT INTO painel_tipo_conselho (nome) VALUES (?)", (tipo,))
        print(f"Adicionado tipo de conselho: {tipo}")
    conn.commit()
    print(f"\nTotal de {len(tipos)} tipos de conselho adicionados com sucesso!")


def cadastrar_especialidades():
    especialidades = ['Pediatra', 'Cardiologista', 'Dermatologista', 'Oftalmologista', 'Ortopedista', 'Neurologista', 'Psicólogo', 'Psicóloga', 'Psiquiatra', 'Fisioterapeuta']
    for especialidade in especialidades:
        cursor.execute("INSERT INTO painel_especialidades (nome) VALUES (?)", (especialidade,))
        print(f"Adicionada especialidade: {especialidade}")
    conn.commit()
    print(f"\nTotal de {len(especialidades)} especialidades adicionadas com sucesso!")


def cadastrar_clinicas():
    clinica1 = { 'nome': 'Clinica 1', 'cep': '00000-000', 'rua': 'Rua 1', 'numero': '1', 'bairro': 'Bairro 1', 'cidade': 'Cidade 1', 'estado_id': '1' }
    clinica2 = { 'nome': 'Clinica 2', 'cep': '00000-000', 'rua': 'Rua 2', 'numero': '2', 'bairro': 'Bairro 2', 'cidade': 'Cidade 2', 'estado_id': '2' }
    
    cursor.execute("INSERT INTO painel_clinicas (nome, cep, rua, numero, bairro, cidade, estado_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (clinica1['nome'], clinica1['cep'], clinica1['rua'], clinica1['numero'], clinica1['bairro'], clinica1['cidade'], clinica1['estado_id']))
    cursor.execute("INSERT INTO painel_clinicas (nome, cep, rua, numero, bairro, cidade, estado_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (clinica2['nome'], clinica2['cep'], clinica2['rua'], clinica2['numero'], clinica2['bairro'], clinica2['cidade'], clinica2['estado_id']))
    conn.commit()
    print(f"\nClinicas adicionadas com sucesso!")
    
def cadastrar_salas():
    nome = 'Sala 1'
    clinica_id = 1
    sublocador_id = 1
    segunda = 'manhã,tarde,noite'
    terca = ''
    quarta = ''
    quinta = 'manhã'
    sexta = 'tarde'
    cursor.execute("INSERT INTO painel_salas (nome, clinica_id, sublocador_id, segunda, terca, quarta, quinta, sexta) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nome, clinica_id, sublocador_id, segunda, terca, quarta, quinta, sexta))
    conn.commit()
    
    nome = 'Sala 2'
    clinica_id = 1
    sublocador_id = 2
    segunda = ''
    terca = 'tarde'
    quarta = ''
    quinta = ''
    sexta = ''
    cursor.execute("INSERT INTO painel_salas (nome, clinica_id, sublocador_id, segunda, terca, quarta, quinta, sexta) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nome, clinica_id, sublocador_id, segunda, terca, quarta, quinta, sexta))
    conn.commit()
    
    
    print(f"\nSalas adicionadas com sucesso!")
if __name__ == '__main__':
    #cadastrar_uf()
    # cadastrar_tipo_conselho()
    # cadastrar_especialidades()
    #cadastrar_clinicas()
    cadastrar_salas()