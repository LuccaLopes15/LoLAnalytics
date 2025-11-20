import analytics
import pandas as pd
import random
import time
import os
import requests

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def coletar_dados_jogadores(ligas=None, target_partidas=100, max_jogadores_por_liga=200):
    """
    Coleta dados de jogadores de determinadas ligas e suas partidas recentes.
    
    Args:
        ligas (list): Lista de ligas a serem coletadas (padrão: Challenger, Grandmaster, Master)
        target_partidas (int): Número desejado de partidas a serem coletadas
        max_jogadores_por_liga (int): Número máximo de jogadores a serem analisados por liga
        
    Returns:
        list: Lista de dicionários com os dados das partidas
    """
    if ligas is None:
        ligas = ["Challenger", "Grandmaster", "Master"]
    
    # Lista para armazenar dados de todas as partidas
    rows = []
    partidas_processadas = 0
    
    for liga in ligas:
        if len(rows) >= target_partidas:
            break
            
        print(f"Coletando dados da {liga} League...")
        league_entries = analytics.get_league_entries(liga)
        print(f"Total de jogadores na {liga}: {len(league_entries)}")
        
        # Embaralha a lista para pegar jogadores aleatórios de cada liga
        random.shuffle(league_entries)
        
        # Limita a quantidade de jogadores por liga para não exceder muito o total desejado
        league_entries = league_entries[:max_jogadores_por_liga]
        
        for entry in league_entries:
            if len(rows) >= target_partidas:
                break
                
            summoner_id = entry.get('summonerId')
            print(f"Coletando dados para summoner (ID: {summoner_id})...")
            
            # Obter dados do summoner para acessar o puuid
            summoner_data = analytics.get_summoner_data(summoner_id)
            if not summoner_data:
                continue
            
            puuid = summoner_data.get('puuid')
            if not puuid:
                print("PUUID não encontrado, pulando jogador.")
                continue

            # Tenta coletar até 3 partidas para cada jogador para aumentar a chance de encontrar partidas válidas
            match_ids = analytics.get_match_ids(puuid, count=3)
            if not match_ids:
                print(f"Nenhuma partida encontrada para o puuid {puuid}.")
                continue

            for match_id in match_ids:
                partidas_processadas += 1
                match_detail = analytics.get_match_detail(match_id)
                if not match_detail:
                    continue

                # Extrai os dados do participante correspondente ao puuid
                participant_data = analytics.extract_participant_data(match_detail, puuid)
                if participant_data:
                    rows.append(participant_data)
                    champion_name = participant_data["champion_name"]
                    lane = participant_data["lane"] 
                    champion_class = participant_data["champion_class"]
                    print(f"Partida adicionada ({len(rows)}/{target_partidas}): {champion_name} na lane {lane} (Classe: {champion_class})")
                    
                    if len(rows) >= target_partidas:
                        break
                
                # Adiciona uma pequena pausa para não atingir rapidamente os limites da API
                time.sleep(0.5)
            
            # Adiciona uma pausa entre jogadores para não atingir os limites da API
            time.sleep(1)
    
    # Resumo da coleta
    print(f"\nResumo da coleta:")
    print(f"Total de partidas processadas: {partidas_processadas}")
    print(f"Total de partidas válidas incluídas: {len(rows)}")
    
    return rows

def coletar_dados_somente_challenger():
    """
    Função para coletar dados apenas da liga Challenger.
    """
    # Verificar se a chave de API atual é válida
    test_url = f"https://{analytics.REGION}.api.riotgames.com/lol/platform/v3/champion-rotations"
    try:
        response = requests.get(test_url, headers=analytics.HEADERS)
        if response.status_code != 200:
            print(f"⚠️ A chave de API atual parece ser inválida (status code: {response.status_code})")
            if input("Deseja atualizar a chave de API antes de continuar? (s/n): ").lower() == 's':
                atualizar_chave_api()
    except Exception as e:
        print(f"⚠️ Erro ao verificar a chave de API: {e}")
        if input("Deseja atualizar a chave de API antes de continuar? (s/n): ").lower() == 's':
            atualizar_chave_api()
    
    # Define o número de partidas a coletar
    try:
        target = int(input("Quantas partidas deseja coletar? (padrão: 100): ") or "100")
    except ValueError:
        print("Valor inválido, usando o padrão de 100 partidas.")
        target = 100
    
    # Define o nome do arquivo para salvar
    arquivo = input("Nome do arquivo para salvar os dados (padrão: dados_challenger.csv): ") or "dados_challenger.csv"
    
    # Coleta os dados
    try:
        print("\nIniciando coleta de dados da liga Challenger...\n")
        dados = analytics.coletar_dados_challenger(target_partidas=target)
        if dados and len(dados) > 0:
            df = analytics.salvar_dados_challenger_csv(dados, arquivo)
            print(f"\nColeta concluída! {len(dados)} partidas salvas em '{arquivo}'")
        else:
            print("\nNenhum dado foi coletado ou a lista de dados está vazia.")
            print("Possíveis causas:")
            print("1. A chave de API pode estar expirada ou ser inválida")
            print("2. Pode haver problemas de conectividade com a API da Riot")
            print("3. As ligas podem estar indisponíveis no momento")
            
            if input("Deseja atualizar a chave de API e tentar novamente? (s/n): ").lower() == 's':
                atualizar_chave_api()
                coletar_dados_somente_challenger()  # Recursão para tentar novamente
    except Exception as e:
        print(f"Erro durante a coleta de dados: {e}")
        if input("Deseja atualizar a chave de API e tentar novamente? (s/n): ").lower() == 's':
            atualizar_chave_api()
            coletar_dados_somente_challenger()  # Recursão para tentar novamente

def salvar_dados_csv(dados, nome_arquivo="dados_partidas.csv"):
    """
    Salva os dados coletados em um arquivo CSV.
    
    Args:
        dados (list): Lista de dicionários com os dados das partidas
        nome_arquivo (str): Nome do arquivo CSV a ser criado
    """
    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    return df

def atualizar_chave_api():
    """
    Solicita ao usuário que insira uma nova chave de API da Riot.
    """
    limpar_tela()
    print("=== Atualizar Chave de API ===")
    print("\nPara obter uma nova chave de API:")
    print("1. Acesse https://developer.riotgames.com/")
    print("2. Faça login na sua conta")
    print("3. Vá para o painel de desenvolvedor")
    print("4. Gere uma nova chave de API")
    print("\nA chave deve começar com 'RGAPI-'")
    
    while True:
        nova_chave = input("\nDigite a nova chave de API: ").strip()
        
        if not nova_chave:
            print("\n❌ ERRO: A chave não pode estar vazia!")
            continue
            
        if not nova_chave.startswith("RGAPI-"):
            print("\n❌ ERRO: A chave deve começar com 'RGAPI-'")
            continue
            
        if len(nova_chave) < 20:
            print("\n❌ ERRO: A chave parece ser muito curta!")
            print("Verifique se a chave foi copiada corretamente.")
            continue
            
        # Tenta atualizar a chave
        if analytics.update_api_key(nova_chave):
            print("\nPressione ENTER para continuar...")
            input()
            return
        else:
            if input("\nDeseja tentar novamente? (s/n): ").lower() != 's':
                return

def coletar_dados_jogador():
    """
    Coleta dados das últimas 5 partidas rankeadas de um jogador específico.
    """
    print("\n=== Coletar Dados de Jogador ===")
    print("Digite o nome do jogador, tag e região.")
    print("\nExemplo de formato:")
    print("Nome: LKA")
    print("Tag: 0515 (apenas os números, sem #)")
    print("Região: BR1")
    
    print("\nRegiões disponíveis:")
    print("BR1 - Brasil")
    print("NA1 - América do Norte")
    print("EUW1 - Europa Oeste")
    print("EUN1 - Europa Norte")
    print("KR - Coreia")
    print("JP1 - Japão")
    print("OC1 - Oceania")
    print("RU - Rússia")
    print("TR1 - Turquia")
    print("LA1 - América Latina Norte")
    print("LA2 - América Latina Sul")
    print("SG2 - Singapura")
    print("TH2 - Tailândia")
    print("TW2 - Taiwan")
    print("VN2 - Vietnã")
    print("PH2 - Filipinas")
    
    username = input("\nDigite o nome do jogador: ").strip()
    tag = input("Digite a tag do jogador (apenas números, sem #): ").strip()
    region = input("Digite a região (ex: BR1): ").strip().upper()
    
    if not username or not tag or not region:
        print("\n❌ ERRO: Nome do jogador, tag e região são obrigatórios!")
        return
    
    try:
        print("\nColetando dados...")
        dados = analytics.coletar_dados_jogador(username, tag, region)
        
        if dados:
            print("\n✓ Dados coletados com sucesso!")
            print(f"Total de partidas encontradas: {len(dados)}")
            
            # Salva os dados em CSV
            analytics.salvar_dados_jogador_csv(dados)
            print("\nDados salvos em 'dados_jogador.csv'")
        else:
            print("\n❌ Nenhum dado foi coletado.")
            print("Verifique se o nome do jogador, tag e região estão corretos.")
            
    except Exception as e:
        print(f"\n❌ ERRO ao coletar dados: {e}")
        print("Verifique se a chave de API está configurada corretamente.")
    
    input("\nPressione ENTER para continuar...")

def main():
    """
    Função principal que executa o menu do programa.
    """
    while True:
        print("\n=== Menu Principal ===")
        print("1. Coletar dados da liga Challenger")
        print("2. Coletar dados de um jogador específico")
        print("3. Sair")
        print("4. Atualizar chave da API")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            try:
                print("\nColetando dados da liga Challenger...")
                dados = analytics.coletar_dados_challenger()
                if dados:
                    analytics.salvar_dados_challenger_csv(dados)
                    print("\nDados salvos em 'dados_challenger.csv'")
            except Exception as e:
                print(f"\nErro ao coletar dados: {e}")
            input("\nPressione ENTER para continuar...")
            
        elif opcao == "2":
            coletar_dados_jogador()
            
        elif opcao == "3":
            print("\nEncerrando o programa...")
            break
            
        elif opcao == "4":
            atualizar_chave_api()
            
        else:
            print("\nOpção inválida! Por favor, escolha uma opção válida.")
            input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main() 