import faker
import sqlite3
import os

# Caminho correto para o banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

fake = faker.Faker('pt_BR')

def populate_db():
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
        estado = fake.state()

        role = 'paciente'
        created_at = fake.date_time()
        updated_at = fake.date_time()

        paciente = (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado, role, created_at, updated_at)
        
        cursor.execute("INSERT INTO painel_paciente (nome, cpf, celular, email, data_nascimento, sexo, cep, rua, numero, bairro, cidade, estado, role, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", paciente)
        print(f"Adicionado paciente {i+1}: {nome}")
    
    conn.commit()
    print(f"\nTotal de {100} pacientes adicionados com sucesso!")

if __name__ == "__main__":
    populate_db()
    conn.close()


