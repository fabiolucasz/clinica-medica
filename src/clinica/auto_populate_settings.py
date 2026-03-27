# clinica/settings.py

# ... outras configurações ...

# Importar função de auto-população
try:
    import os
    import sys
    
    # Adicionar path do projeto
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_root)
    
    # Importar e executar auto-população
    from populate_db import auto_populate_if_empty
    
    # Executar apenas em desenvolvimento
    if DEBUG:
        auto_populate_if_empty()
        
except ImportError:
    print("⚠️ Não foi possível importar o script de população")
except Exception as e:
    print(f"⚠️ Erro na auto-população: {e}")
