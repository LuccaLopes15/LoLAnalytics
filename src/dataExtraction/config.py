import json
import os

def load_api_key():
    """
    Carrega a chave da API do arquivo de configuração.
    
    Returns:
        str: Chave da API ou None se não existir
    """
    try:
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                config = json.load(f)
                api_key = config.get('api_key')
                if api_key and api_key.startswith('RGAPI-'):
                    return api_key
                else:
                    print("⚠️ Chave de API inválida no arquivo de configuração.")
                    return None
    except Exception as e:
        print(f"Erro ao carregar a chave de API: {e}")
    return None

def save_api_key(api_key):
    """
    Salva a chave da API no arquivo de configuração.
    
    Args:
        api_key (str): Chave da API a ser salva
        
    Returns:
        bool: True se a chave foi salva com sucesso, False caso contrário
    """
    try:
        # Validação básica da chave
        if not api_key or not api_key.startswith('RGAPI-'):
            print("❌ ERRO: Chave de API inválida!")
            return False
            
        config = {'api_key': api_key}
        with open('config.json', 'w') as f:
            json.dump(config, f)
        print("✓ Chave de API salva com sucesso!")
        return True
    except Exception as e:
        print(f"❌ ERRO ao salvar a chave de API: {e}")
        return False 