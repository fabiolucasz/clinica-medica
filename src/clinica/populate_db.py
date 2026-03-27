#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinica.settings')
django.setup()

from painel.models import Especialidades, Estados, Tipo_conselho

def populate_database():
    """Função principal para popular o banco de dados"""
    print("🚀 Iniciando população do banco de dados...")
    
    # Criar dados básicos
    create_estados()
    create_tipos_conselho()
    create_especialidades()
    
    print("✅ Banco de dados populado com sucesso!")

def create_estados():
    """Cria estados brasileiros"""
    print("📍 Criando estados...")
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
        estado, created = Estados.objects.get_or_create(nome=nome, sigla=uf)
        if created:
            print(f"  ✅ Estado criado: {nome}")

def create_tipos_conselho():
    """Cria tipos de conselho"""
    print("🏥 Criando tipos de conselho...")
    tipos = ['CRM', 'CRP', 'CRN', 'CREFITO']
    
    for tipo in tipos:
        conselho, created = Tipo_conselho.objects.get_or_create(nome=tipo)
        if created:
            print(f"  ✅ Tipo de conselho criado: {tipo}")

def create_especialidades():
    """Cria especialidades médicas"""
    print("⚕️ Criando especialidades...")
    especialidades_data = [
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
    
    for esp in especialidades_data:
        especialidade, created = Especialidades.objects.get_or_create(nome=esp)
        if created:
            print(f"  ✅ Especialidade criada: {esp}")


if __name__ == '__main__':
    populate_database()