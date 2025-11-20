import requests
import time
import random
import pandas as pd
import config

def update_headers(api_key):
    """
    Atualiza os headers com a nova chave de API.
    
    Args:
        api_key (str): Nova chave de API
    """
    global HEADERS
    HEADERS = {
        "X-Riot-Token": api_key
    }

# Carrega a chave de API do arquivo de configuração
API_KEY = config.load_api_key()
if not API_KEY:
    print("⚠️ Nenhuma chave de API encontrada. Por favor, atualize a chave através do menu principal.")
    API_KEY = "RGAPI-00000000-0000-0000-0000-000000000000"  # Chave temporária

# Inicializa os headers com a chave carregada
HEADERS = {
    "X-Riot-Token": API_KEY
}

# Defina as regiões para a League/Summoner e para a Match API
REGION = "br1"             # Exemplo: "br1", "na1", "euw1", etc.
MATCH_REGION = "americas"  # Para a Match API (americas, europe, asia)

# Dicionário de mapeamento de campeões para suas classes
CHAMPION_CLASSES = {
    # Magos
    "Ahri": "Mago",
    "Lux": "Mago",
    "Annie": "Mago",
    "Morgana": "Mago",
    "Veigar": "Mago",
    "Syndra": "Mago",
    "Zyra": "Mago",
    "Orianna": "Mago",
    "Twisted Fate": "Mago",
    "TwistedFate": "Mago",  # Nome como a API retorna
    "Brand": "Mago",
    "Zoe": "Mago",
    "Seraphine": "Mago",
    "Swain": "Mago",
    "Vladimir": "Mago",
    "Kennen": "Mago",
    "Sylas": "Mago",
    "Taliyah": "Mago",
    "Viktor": "Mago",
    "Ryze": "Mago",
    "Mel": "Mago",
    "AurelionSol": "Mago",
    "Azir": "Mago",
    "Cassiopeia": "Mago",
    "Elise": "Mago",
    "Fiddlesticks": "Mago",
    "Heimerdinger": "Mago",
    "Lillia": "Mago",
    "Lissandra": "Mago",
    "Malzahar": "Mago",
    "Neeko": "Mago",
    "Velkoz": "Mago",
    "Vex": "Mago",
    "Xerath": "Mago",
    "Ziggs": "Mago",
    
    # Assassinos
    "Zed": "Assassino",
    "Katarina": "Assassino",
    "Master Yi": "Assassino",
    "MasterYi": "Assassino",  # Nome como a API retorna
    "Talon": "Assassino",
    "Akali": "Assassino",
    "LeBlanc": "Assassino",
    "Ekko": "Assassino",
    "Diana": "Assassino",
    "Kassadin": "Assassino",
    "Kha'Zix": "Assassino",
    "KhaZix": "Assassino",  # Nome como a API retorna
    "Khazix": "Assassino",
    "Rengar": "Assassino",
    "Evelynn": "Assassino",
    "Fizz": "Assassino",
    "Qiyana": "Assassino",
    "Yone": "Assassino",
    "Nidalee": "Assassino",
    "Kayn": "Assassino",
    "Nocturne": "Assassino",
    "Shaco": "Assassino",
    
    # Lutadores
    "Garen": "Lutador",
    "Lee Sin": "Lutador",
    "LeeSin": "Lutador",  # Nome como a API retorna
    "Darius": "Lutador",
    "Yasuo": "Lutador",
    "Riven": "Lutador",
    "Olaf": "Lutador",
    "Jax": "Lutador",
    "Irelia": "Lutador",
    "Renekton": "Lutador",
    "Sett": "Lutador",
    "Gwen": "Lutador",
    "Volibear": "Lutador",
    "Warwick": "Lutador",
    "Xin Zhao": "Lutador",
    "XinZhao": "Lutador",  # Nome como a API retorna
    "Gangplank": "Lutador",
    "Gragas": "Lutador",
    "Ambessa": "Lutador",
    "Jayce": "Lutador",
    "Pantheon": "Lutador",
    "JarvanIV": "Lutador",
    "Aatrox": "Lutador",
    "Briar": "Lutador",
    "Camille": "Lutador",
    "Fiora": "Lutador",
    "Hecarim": "Lutador",
    "Illaoi": "Lutador",
    "Kled": "Lutador",
    "Mordekaiser": "Lutador",
    "Nasus": "Lutador",
    "RekSai": "Lutador",
    "Rumble": "Lutador",
    "Shyvana": "Lutador",
    "Skarner": "Lutador",
    "Trundle": "Lutador",
    "Tryndamere": "Lutador",
    "Udyr": "Lutador",
    "Urgot": "Lutador",
    "Vi": "Lutador",
    "Viego": "Lutador",
    "Yorick": "Lutador",
    
    # Atiradores
    "Ezreal": "Atirador",
    "Jinx": "Atirador",
    "Teemo": "Atirador",
    "Ashe": "Atirador",
    "Caitlyn": "Atirador",
    "Vayne": "Atirador",
    "Tristana": "Atirador",
    "Jhin": "Atirador",
    "Lucian": "Atirador",
    "Varus": "Atirador",
    "Corki": "Atirador",
    "Kaisa": "Atirador",
    "Aphelios": "Atirador",
    "Kalista": "Atirador",
    "Kindred": "Atirador",
    "Akshan": "Atirador",
    "Draven": "Atirador",
    "Graves": "Atirador",
    "KogMaw": "Atirador",
    "MissFortune": "Atirador",
    "Quinn": "Atirador",
    "Samira": "Atirador",
    "Twitch": "Atirador",
    "Xayah": "Atirador",
    "Zeri": "Atirador",
    
    # Suportes
    "Soraka": "Suporte",
    "Thresh": "Suporte",
    "Sona": "Suporte",
    "Zilean": "Suporte",
    "Bard": "Suporte",
    "Janna": "Suporte",
    "Nami": "Suporte",
    "Lulu": "Suporte",
    "Braum": "Suporte",
    "Blitzcrank": "Suporte",
    "Yuumi": "Suporte",
    "Pyke": "Suporte",
    "Senna": "Suporte",
    "Karma": "Suporte",
    "Taric": "Suporte",
    "Rakan": "Suporte",
    "Ivern": "Suporte",
    "Renata": "Suporte",
    
    # Tanques
    "Leona": "Tanque",
    "Malphite": "Tanque",
    "Alistar": "Tanque",
    "Sion": "Tanque",
    "Ornn": "Tanque",
    "Cho'Gath": "Tanque",
    "ChoGath": "Tanque",  # Nome como a API retorna
    "Sejuani": "Tanque",
    "Nautilus": "Tanque",
    "Rell": "Tanque",
    "Galio": "Tanque",
    "Amumu": "Tanque",
    "KSante": "Tanque",
    "Maokai": "Tanque",
    "Nunu": "Tanque",
    "NunuWillump": "Tanque",
    "Poppy": "Tanque",
    "Rammus": "Tanque",
    "Shen": "Tanque",
    "Singed": "Tanque",
    "Tahm Kench": "Tanque",
    "TahmKench": "Tanque",  # Nome como a API retorna
    "Zac": "Tanque",
    
    # Healers específicos
    "Soraka": "Healer",
    "Sona": "Healer"
}

def get_league_entries(league_tier):
    """
    Coleta os dados da Liga (Challenger, GrandMaster ou Master).
    
    Args:
        league_tier (str): Tier da liga (Challenger, Grandmaster ou Master)
        
    Returns:
        list: Lista de jogadores na liga especificada
    """
    # Formatação correta do tier para a URL - verificando e ajustando para minúsculo
    tier_lower = league_tier.lower()
    
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/{tier_lower}leagues/by-queue/RANKED_SOLO_5x5"
    print(f"Acessando URL: {url}")
    
    response = requests.get(url, headers=HEADERS)
    
    # Se receber código 429 (rate limit), aguarda e tenta novamente
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        print(f"Rate limit atingido. Aguardando {retry_after} segundos...")
        time.sleep(retry_after + 1)
        return get_league_entries(league_tier)  # Tenta novamente após esperar
    
    if response.status_code != 200:
        print(f"Erro ao coletar dados da {league_tier} League: {response.status_code}")
        # Mostrar detalhes do erro para ajudar no diagnóstico
        try:
            error_details = response.json()
            print(f"Detalhes do erro: {error_details}")
        except:
            print("Não foi possível obter detalhes adicionais do erro")
        
        return []
    
    data = response.json()
    entries = data.get('entries', [])
    print(f"Jogadores encontrados na liga {league_tier}: {len(entries)}")
    return entries

def get_summoner_data(summoner_id):
    """
    Coleta os dados do summoner para obter informações como o puuid.
    
    Args:
        summoner_id (str): ID do invocador
        
    Returns:
        dict: Dados do invocador ou None em caso de erro
    """
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    response = requests.get(url, headers=HEADERS)
    
    # Se receber código 429 (rate limit), aguarda e tenta novamente
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        print(f"Rate limit atingido. Aguardando {retry_after} segundos...")
        time.sleep(retry_after + 1)
        return get_summoner_data(summoner_id)  # Tenta novamente após esperar
    
    if response.status_code != 200:
        print(f"Erro ao coletar dados do summoner {summoner_id}: {response.status_code}")
        return None
    
    return response.json()

def get_match_ids(puuid, count=1, region=None):
    """
    Coleta uma lista de IDs de partidas para um dado puuid, limitado a 'count' partidas.
    
    Args:
        puuid (str): PUUID do jogador
        count (int): Número de partidas a serem coletadas
        region (str): Região para buscar as partidas (americas, europe, asia)
        
    Returns:
        list: Lista de IDs de partidas
    """
    # Use a região fornecida ou a padrão
    match_region = region if region else MATCH_REGION
    
    # Busca mais partidas do que o necessário para garantir que teremos partidas suficientes após a filtragem
    url = f"https://{match_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=20"
    response = requests.get(url, headers=HEADERS)
    
    # Se receber código 429 (rate limit), aguarda e tenta novamente
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        print(f"Rate limit atingido. Aguardando {retry_after} segundos...")
        time.sleep(retry_after + 1)
        return get_match_ids(puuid, count, region)  # Tenta novamente após esperar
    
    if response.status_code != 200:
        print(f"Erro ao coletar matches para o puuid {puuid}: {response.status_code}")
        return []
    
    # Retorna apenas o número solicitado de partidas
    match_ids = response.json()
    return match_ids[:count] if match_ids else []

def get_match_detail(match_id, region=None):
    """
    Coleta os detalhes de uma partida específica.
    
    Args:
        match_id (str): ID da partida
        region (str): Região para buscar os detalhes (americas, europe, asia)
        
    Returns:
        dict: Detalhes da partida ou None em caso de erro
    """
    # Use a região fornecida ou a padrão
    match_region = region if region else MATCH_REGION
    
    url = f"https://{match_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    
    # Se receber código 429 (rate limit), aguarda e tenta novamente
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 5))
        print(f"Rate limit atingido. Aguardando {retry_after} segundos...")
        time.sleep(retry_after + 1)
        return get_match_detail(match_id, region)  # Tenta novamente após esperar
    
    if response.status_code != 200:
        print(f"Erro ao coletar detalhes do match {match_id}: {response.status_code}")
        return None
    
    return response.json()

def extract_participant_data(match_detail, puuid):
    """
    Extrai os dados de um participante específico de uma partida.
    
    Args:
        match_detail (dict): Detalhes da partida
        puuid (str): PUUID do jogador a ser encontrado
        
    Returns:
        dict: Dados formatados do participante ou None se não encontrado
    """
    if not match_detail:
        return None
        
    # Encontra os dados do participante correspondente ao puuid
    participant_data = None
    for participant in match_detail.get('info', {}).get('participants', []):
        if participant.get('puuid', '').lower() == puuid.lower():
            participant_data = participant
            break
            
    if not participant_data:
        print(f"Dados do participante não encontrados para o puuid {puuid}.")
        return None
        
    # Coleta os dados necessários da partida
    kills = participant_data.get('kills', 0)
    assists = participant_data.get('assists', 0)
    deaths = participant_data.get('deaths', 0)
    total_minions = participant_data.get('totalMinionsKilled', 0)
    neutral_minions = participant_data.get('neutralMinionsKilled', 0)
    cs = total_minions + neutral_minions
    vision_score = participant_data.get('visionScore', 0)
    gold_earned = participant_data.get('goldEarned', 0)
    
    # A API da Riot usa 'totalDamageDealtToChampions' para o dano causado a campeões
    damage_dealt_to_champions = participant_data.get('totalDamageDealtToChampions', 0)

    # Cálculo da Participação em Objetivos: (kills + assists) / total kills do time
    team_id = participant_data.get('teamId')
    team_kills = sum(p.get('kills', 0) for p in match_detail.get('info', {}).get('participants', []) 
                     if p.get('teamId') == team_id)
    objective_participation = (kills + assists) / team_kills if team_kills > 0 else 0

    # Extração da rota e da classe do campeão
    # Para a rota, usa-se o campo "teamPosition" ou "individualPosition" ou "lane" se disponível
    lane = (participant_data.get("teamPosition", "") or 
            participant_data.get("individualPosition", "") or 
            participant_data.get("lane", ""))
            
    # Para a classe do campeão, usa-se o championName e mapeia com o dicionário
    champion_name = participant_data.get("championName", "")
    champion_class = CHAMPION_CLASSES.get(champion_name, "Desconhecido")
    
    # Normaliza a lane para comparação case-insensitive
    lane_normalized = lane.strip().lower() if lane else ""
    
    # Verifica se os dados são válidos:
    # 1. champion_class não é "Desconhecido"
    # 2. lane não está vazia
    # 3. lane não contém "invalid" em qualquer formato
    invalid_lane = not lane_normalized or "invalid" in lane_normalized
    
    if champion_class == "Desconhecido" or invalid_lane:
        if champion_class == "Desconhecido":
            print(f"Partida ignorada: Champion {champion_name} não tem classe definida")
        elif not lane_normalized:
            print(f"Partida ignorada: Lane não definida para o champion {champion_name}")
        elif "invalid" in lane_normalized:
            print(f"Partida ignorada: Lane inválida ({lane}) para o champion {champion_name}")
        return None
    
    # Retorna os dados formatados
    return {
        "match_id": match_detail.get('metadata', {}).get('matchId', ''),
        "kills": kills,
        "assists": assists,
        "deaths": deaths,
        "cs": cs,
        "objective_participation": objective_participation,
        "visionScore": vision_score,
        "goldEarned": gold_earned,
        "damageDealtToChampions": damage_dealt_to_champions,
        "lane": lane,
        "champion_class": champion_class,
        "champion_name": champion_name
    }

def update_api_key(new_key):
    """
    Atualiza a chave de API da Riot.
    
    Args:
        new_key (str): Nova chave de API
        
    Returns:
        bool: True se a chave foi atualizada com sucesso, False caso contrário
    """
    global API_KEY, HEADERS
    
    # Remove espaços em branco do início e fim
    new_key = new_key.strip()
    
    # Validações básicas
    if not new_key:
        print("\n❌ ERRO: A chave de API não pode estar vazia!")
        return False
    
    if not new_key.startswith("RGAPI-"):
        print("\n❌ ERRO: A chave de API está em formato incorreto!")
        print("A chave deve começar com 'RGAPI-'")
        return False
    
    if len(new_key) < 20:  # Chaves da Riot geralmente têm mais de 20 caracteres
        print("\n❌ ERRO: A chave de API parece ser muito curta!")
        print("Verifique se a chave foi copiada corretamente.")
        return False
    
    # Atualiza as variáveis globais
    API_KEY = new_key
    update_headers(new_key)
    
    # Testa a nova chave
    try:
        print("\nTestando a nova chave de API...")
        test_url = f"https://{REGION}.api.riotgames.com/lol/platform/v3/champion-rotations"
        print(f"URL de teste: {test_url}")
        print(f"Headers: {HEADERS}")
        
        response = requests.get(test_url, headers=HEADERS)
        
        if response.status_code == 200:
            print("\n✓ Chave de API atualizada com sucesso!")
            print("✓ Chave verificada e funcionando corretamente.")
            # Salva a chave no arquivo de configuração
            if config.save_api_key(new_key):
                print("✓ Chave salva no arquivo de configuração.")
            return True
        elif response.status_code == 401:
            print("\n❌ ERRO: A chave de API está inválida!")
            print("Verifique se a chave foi copiada corretamente.")
            return False
        elif response.status_code == 403:
            print("\n❌ ERRO: Acesso negado com a chave fornecida!")
            print("A chave pode estar expirada ou não ter as permissões necessárias.")
            return False
        else:
            print(f"\n⚠️ AVISO: A chave foi atualizada, mas retornou código {response.status_code} no teste.")
            print("A chave pode estar funcionando parcialmente ou ter restrições.")
            return True
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API da Riot!")
        print("Verifique sua conexão com a internet.")
        return False
    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro ao testar a chave: {e}")
        return False

def coletar_dados_challenger(target_partidas=100, max_jogadores=200):
    """
    Coleta dados de jogadores apenas da liga Challenger e suas partidas recentes.
    
    Args:
        target_partidas (int): Número desejado de partidas a serem coletadas
        max_jogadores (int): Número máximo de jogadores a serem analisados
        
    Returns:
        list: Lista de dicionários com os dados das partidas
    """
    # Lista para armazenar dados de todas as partidas
    rows = []
    partidas_processadas = 0
    
    # Apenas liga Challenger
    liga = "Challenger"
    
    print(f"Coletando dados da {liga} League...")
    league_entries = get_league_entries(liga)
    print(f"Total de jogadores na {liga}: {len(league_entries)}")
    
    # Embaralha a lista para pegar jogadores aleatórios
    random.shuffle(league_entries)
    
    # Limita a quantidade de jogadores
    league_entries = league_entries[:max_jogadores]
    
    for entry in league_entries:
        if len(rows) >= target_partidas:
            break
            
        summoner_id = entry.get('summonerId')
        print(f"Coletando dados para summoner (ID: {summoner_id})...")
        
        # Obter dados do summoner para acessar o puuid
        summoner_data = get_summoner_data(summoner_id)
        if not summoner_data:
            continue
        
        puuid = summoner_data.get('puuid')
        if not puuid:
            print("PUUID não encontrado, pulando jogador.")
            continue

        # Tenta coletar até 3 partidas para cada jogador para aumentar a chance de encontrar partidas válidas
        match_ids = get_match_ids(puuid, count=3)
        if not match_ids:
            print(f"Nenhuma partida encontrada para o puuid {puuid}.")
            continue

        for match_id in match_ids:
            partidas_processadas += 1
            match_detail = get_match_detail(match_id)
            if not match_detail:
                continue

            # Extrai os dados do participante correspondente ao puuid
            participant_data = extract_participant_data(match_detail, puuid)
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

def salvar_dados_challenger_csv(dados, nome_arquivo="dados_challenger.csv"):
    """
    Salva os dados coletados da liga Challenger em um arquivo CSV.
    
    Args:
        dados (list): Lista de dicionários com os dados das partidas
        nome_arquivo (str): Nome do arquivo CSV a ser criado
        
    Returns:
        DataFrame: DataFrame pandas com os dados salvos
    """
    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    return df

def coletar_dados_jogador(username, tag, region):
    """
    Coleta dados das últimas 5 partidas rankeadas de um jogador específico.
    
    Args:
        username (str): Nome do invocador
        tag (str): Tag do invocador (ex: BR1, NA1, etc)
        region (str): Região do jogador (ex: BR1, NA1, EUW1, etc)
        
    Returns:
        list: Lista de dicionários com os dados das partidas
    """
    # Lista para armazenar dados das partidas
    rows = []
    partidas_necessarias = 5
    
    # Limpa e formata o nome e tag do jogador
    username = username.strip()
    tag = tag.strip().replace("#", "")  # Remove o # se presente
    
    # Define a região para a API de contas (americas para BR1, NA1, LA1, LA2)
    account_region = "americas"
    if region.upper() in ["EUW1", "EUN1", "TR1", "RU"]:
        account_region = "europe"
    elif region.upper() in ["KR", "JP1"]:
        account_region = "asia"
    
    # URL para obter o puuid do jogador usando a região correta para contas
    url = f"https://{account_region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tag}"
    print(f"\nBuscando jogador em: {url}")
    print(f"Nome: {username}")
    print(f"Tag: {tag}")
    print(f"Região: {region}")
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 403:
        print(f"\nErro 403: Acesso negado ao buscar dados do jogador {username}#{tag}")
        print("Possíveis causas:")
        print("1. A chave de API está inválida ou expirada")
        print("2. A chave de API não tem permissão para acessar a API de contas")
        print("3. A chave de API não está configurada corretamente")
        print("\nPor favor, atualize sua chave de API e tente novamente.")
        return []
    elif response.status_code == 404:
        print(f"\nErro 404: Jogador '{username}#{tag}' não encontrado")
        print("Verifique se:")
        print("1. O nome do jogador está correto")
        print("2. A tag está correta (sem o #)")
        print("3. O jogador existe")
        return []
    elif response.status_code != 200:
        print(f"\nErro ao buscar dados do jogador {username}#{tag}: {response.status_code}")
        print(f"Resposta da API: {response.text}")
        return []
    
    account_data = response.json()
    puuid = account_data.get('puuid')
    
    if not puuid:
        print("\nPUUID não encontrado para o jogador.")
        print("Verifique se o nome e tag do jogador estão corretos.")
        return []
    
    # Define a região para buscar o histórico de partidas
    match_region = "americas"
    if region.upper() in ["EUW1", "EUN1", "TR1", "RU"]:
        match_region = "europe"
    elif region.upper() in ["KR", "JP1"]:
        match_region = "asia"
    
    print(f"\nBuscando histórico de partidas na região: {match_region}")
    
    # Tenta coletar partidas até ter 5 válidas ou esgotar as tentativas
    tentativas = 0
    max_tentativas = 4  # Número máximo de tentativas para encontrar 5 partidas válidas
    
    while len(rows) < partidas_necessarias and tentativas < max_tentativas:
        # Busca mais partidas a cada tentativa
        partidas_por_tentativa = 10
        match_ids = get_match_ids(puuid, count=partidas_por_tentativa, region=match_region)
        if not match_ids:
            break
        
        print(f"\nTentativa {tentativas + 1}: Analisando {len(match_ids)} partidas...")
        
        for match_id in match_ids:
            if len(rows) >= partidas_necessarias:
                break
                
            match_detail = get_match_detail(match_id, region=match_region)
            if not match_detail:
                continue

            # Extrai os dados do participante
            participant_data = extract_participant_data(match_detail, puuid)
            if participant_data:
                rows.append(participant_data)
                champion_name = participant_data["champion_name"]
                lane = participant_data["lane"]
                champion_class = participant_data["champion_class"]
                print(f"Partida {len(rows)}/5 adicionada: {champion_name} na lane {lane} (Classe: {champion_class})")
            
            # Adiciona uma pequena pausa para não atingir os limites da API
            time.sleep(0.5)
        
        tentativas += 1
        if len(rows) < partidas_necessarias:
            print(f"\nAinda precisamos de {partidas_necessarias - len(rows)} partidas válidas...")
    
    print(f"\nResumo da coleta:")
    print(f"Total de partidas válidas incluídas: {len(rows)}")
    
    if len(rows) < partidas_necessarias:
        print(f"\n⚠️ Aviso: Não foi possível encontrar {partidas_necessarias} partidas válidas.")
        print(f"Foram encontradas apenas {len(rows)} partidas válidas.")
    
    return rows

def salvar_dados_jogador_csv(dados, nome_arquivo="dados_jogador.csv"):
    """
    Salva os dados coletados do jogador em um arquivo CSV.
    
    Args:
        dados (list): Lista de dicionários com os dados das partidas
        nome_arquivo (str): Nome do arquivo CSV a ser criado
        
    Returns:
        DataFrame: DataFrame pandas com os dados salvos
    """
    df = pd.DataFrame(dados)
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    return df
