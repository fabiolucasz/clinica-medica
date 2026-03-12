import faker
import sqlite3
import os
import random

# Caminho correto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

fake = faker.Faker('pt_BR')

def populate_db():
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


def cadastrar_medico():
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
        especialidade = fake.random_element(['Clínico Geral', 'Pediatra', 'Cardiologia', 'Dermatologia', 'Oftalmologia'])

        role = 'medico'
        valor_consulta = fake.random_element(['100', '200', '300', '400', '500'])

        tipo_conselho = fake.random_element(['CRM', 'CRP','CREFITO', 'CRN'])
        uf_conselho = fake.random_element(['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'])
        numero_conselho = fake.random_element(['123456', '123457', '123458', '123459', '123460'])
        
        # metadados
        created_at = fake.date_time()
        updated_at = fake.date_time()

        medico = (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, foto_perfil, especialidade, role, valor_consulta, tipo_conselho,uf_conselho,numero_conselho, created_at, updated_at)
        
        cursor.execute("INSERT INTO painel_medico (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado_id, foto_perfil, especialidade, role, valor_consulta, tipo_conselho,uf_conselho,numero_conselho, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", medico)
        print(f"Adicionado medico {i+1}: {nome}")
    
    conn.commit()
    print(f"\nTotal de {10} medicos adicionados com sucesso!")
if __name__ == "__main__":
    #populate_db()
    cadastrar_tipo_conselho()
    conn.close()


