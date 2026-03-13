import faker
import sqlite3
import os
import random

# Caminho correto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

fake = faker.Faker('pt_BR')

def estados():
    # Estados
    estados = [
        ('Acre', 'AC'),
        ('Alagoas', 'AL'),
        ('Amapá', 'AP'),
        ('Amazonas', 'AM'),
        ('Bahia', 'BA'),
        ('Ceará', 'CE'),
        ('Distrito Federal', 'DF'),
        ('Espírito Santo', 'ES'),
        ('Goiás', 'GO'),
        ('Maranhão', 'MA'),
        ('Mato Grosso', 'MT'),
        ('Mato Grosso do Sul', 'MS'),
        ('Minas Gerais', 'MG'),
        ('Pará', 'PA'),
        ('Paraíba', 'PB'),
        ('Paraná', 'PR'),
        ('Pernambuco', 'PE'),
        ('Piauí', 'PI'),
        ('Rio de Janeiro', 'RJ'),
        ('Rio Grande do Norte', 'RN'),
        ('Rio Grande do Sul', 'RS'),
        ('Rondônia', 'RO'),
        ('Roraima', 'RR'),
        ('Santa Catarina', 'SC'),
        ('São Paulo', 'SP'),
        ('Sergipe', 'SE'),
        ('Tocantins', 'TO')
    ]
    
    for nome, uf in estados:
        cursor.execute("INSERT OR IGNORE INTO painel_estados (nome, uf) VALUES (?, ?)", (nome, uf))
    
    conn.commit()
    print(f"\nTotal de {len(estados)} estados adicionados com sucesso!")
    
def especialidades():
    # Especialidades
    especialidades = [
        'Cardiologista',
        'Dermatologista',
        'Ginecologista',
        'Oftalmologista',
        'Ortopedista',
        'Pediatra',
        'Psiquiatra',
        'Urologista',
        'Psicólogo(a)'
    ]
    
    for nome in especialidades:
        cursor.execute("INSERT OR IGNORE INTO painel_especialidades (nome) VALUES (?)", (nome,))
    
    conn.commit()
    print(f"\nTotal de {len(especialidades)} especialidades adicionadas com sucesso!")


def tipo_conselho():
    # Tipo de conselho
    tipos_conselho = [
        'CRM',
        'CRN',
        'CREFITO',
        'CRP'

    ]
    
    for nome in tipos_conselho:
        cursor.execute("INSERT OR IGNORE INTO painel_tipo_conselho (nome) VALUES (?)", (nome,))
    
    conn.commit()
    print(f"\nTotal de {len(tipos_conselho)} tipos de conselho adicionados com sucesso!")

def clinicas():
    # Criar múltiplas clínicas
    for i in range(5):  # Criar 5 clínicas
        nome = fake.company()
        cnpj = fake.cnpj()
        email = fake.email()
        celular = fake.phone_number()
        celular2 = fake.phone_number()
        
        # endereço
        cep = fake.postcode()
        rua = fake.street_name()
        numero = fake.building_number()
        bairro = fake.city()
        cidade = fake.state()
        estado_id = random.randint(1, 27)
        
        created_at = fake.date_time()
        updated_at = fake.date_time()
        
        clinica = (nome, cnpj, celular, celular2, email, cep, rua, numero, bairro, cidade, estado_id, created_at, updated_at)
        
        cursor.execute("INSERT INTO painel_clinicas (nome, cnpj, celular, celular2, email, cep, rua, numero, bairro, cidade, estado_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", clinica)
        print(f"Adicionado clinica: {nome}")
    
    conn.commit()
    print(f"\nTotal de 5 clínicas adicionadas com sucesso!")


def salas():
    # Salas
    for i in range(10):
        nome = f'Consultório {i+1}'
        clinica_id = 2
        
        cursor.execute("INSERT INTO painel_salas (nome, clinica_id) VALUES (?, ?)", (nome, clinica_id))
        print(f"Adicionado sala: {nome}")
    
    conn.commit()
    print(f"\nTotal de {10} salas adicionadas com sucesso!")

def vagas():
    # Vagas para cada sala (manhã, tarde, noite)
    salas_query = "SELECT id, clinica_id FROM painel_salas"
    cursor.execute(salas_query)
    salas_data = cursor.fetchall()
    
    turnos = ['manhã', 'tarde', 'noite']
    vagas_adicionadas = 0
    vagas_ignoradas = 0
    
    for sala_data in salas_data:
        sala_id = sala_data[0]
        clinica_id = sala_data[1]
        
        for turno in turnos:
            # Verificar se a vaga já existe
            check_query = "SELECT COUNT(*) FROM painel_vagas WHERE sala_id = ? AND turno = ?"
            cursor.execute(check_query, (sala_id, turno))
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Inserir apenas se não existir (agora com clinica_id)
                cursor.execute(
                    "INSERT INTO painel_vagas (sala_id, clinica_id, status, turno) VALUES (?, ?, ?, ?)",
                    (sala_id, clinica_id, 'disponível', turno)
                )
                print(f"Adicionada vaga: Sala {sala_id} - Clínica {clinica_id} - {turno}")
                vagas_adicionadas += 1
            else:
                print(f"Vaga já existe: Sala {sala_id} - Clínica {clinica_id} - {turno} (ignorada)")
                vagas_ignoradas += 1
    
    conn.commit()
    print(f"\nTotal de {vagas_adicionadas} vagas adicionadas com sucesso!")
    if vagas_ignoradas > 0:
        print(f"Total de {vagas_ignoradas} vagas já existentes foram ignoradas.")

def pacientes():
    #Pacientes
    for i in range(100):
        nome = fake.name()
        cpf = fake.cpf()
        celular = fake.phone_number()
        email = fake.email()
        data_nascimento_obj = fake.date_of_birth()
        data_nascimento = data_nascimento_obj.strftime('%Y-%m-%d')  # Formato ISO para o banco
        sexo = fake.random_element(['Masculino', 'Feminino'])

        # endereço
        cep = fake.postcode()
        rua = fake.street_name()
        numero = fake.building_number()
        bairro = fake.city()
        cidade = fake.state()
        estado_id = random.randint(1, 27)

        role = 'paciente'
        created_at = fake.date_time()
        updated_at = fake.date_time()

        paciente = (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, role, created_at, updated_at)
        
        cursor.execute("INSERT INTO painel_paciente (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, role, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", paciente)
        print(f"Adicionado paciente {i+1}: {nome}")
    
    conn.commit()
    print(f"\nTotal de {100} pacientes adicionados com sucesso!")

def medico():
    for i in range(10):
        
        
        # dados pessoais
        nome = fake.name()
        cpf = fake.cpf()
        celular = fake.phone_number()
        email = fake.email()
        data_nascimento_obj = fake.date_of_birth()
        data_nascimento = data_nascimento_obj.strftime('%Y-%m-%d')  # Formato ISO para o banco
        sexo = fake.random_element(['Masculino', 'Feminino'])

        # endereço
        cep = fake.postcode()
        rua = fake.street_name()
        numero = fake.building_number()
        bairro = fake.city()
        cidade = fake.state()
        estado_id = random.randint(1, 27)

        # Perfil
        foto_masculino='https://super.abril.com.br/wp-content/uploads/2019/01/house.jpg?crop=1&resize=1212,909'
        foto_feminino='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcsUSTTErzLgA0uLHqfAZIQZvk5AzzGnd4Bw&s'
        if sexo == 'Masculino':
            foto_perfil = foto_masculino
        else:
            foto_perfil = foto_feminino
        especialidade_id = random.randint(1,9)

        role = 'medico'
        valor_consulta = fake.random_element(['100', '200', '300', '400', '500'])

        tipo_conselho_id = random.randint(1,4)
        uf_conselho_id = random.randint(1,27)
        numero_conselho = random.randint(100000, 999999)
        rqe = random.randint(100000, 999999)
        
        # metadados
        created_at = fake.date_time()
        updated_at = fake.date_time()

        medico = (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, foto_perfil, especialidade_id, role, valor_consulta, tipo_conselho_id, uf_conselho_id, numero_conselho, rqe, created_at, updated_at)
        
        cursor.execute("INSERT INTO painel_medico (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, foto_perfil, especialidade_id, role, valor_consulta, tipo_conselho_id, uf_conselho_id, numero_conselho, rqe, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", medico)
        print(f"Adicionado medico {i+1}: {nome}")
    
    conn.commit()
    print(f"\nTotal de {10} medicos adicionados com sucesso!")
if __name__ == "__main__":
    # estados()
    # especialidades()
    # tipo_conselho()
    # clinicas()
    # salas()
    vagas()
    # pacientes()
    # medico()
    conn.close()


