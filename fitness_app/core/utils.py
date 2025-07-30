"""
Funções Utilitárias que auxiliam na manutenção de funções secundárias do sistema para testes
"""

def gerar_csv_wearable_aleatorio(servico, usuario_email, caminho_csv, tipos, dias=30):
    from datetime import datetime, timedelta
    import random
    hoje = datetime.now()
    for i in range(dias):
        for tipo in tipos:
            hora = random.randint(0, 23)
            minuto = random.randint(0, 59)
            segundo = random.randint(0, 59)
            data_base = hoje - timedelta(days=i)
            data_aleatoria = data_base.replace(hour=hora, minute=minuto, second=segundo, microsecond=0)
            data_str = data_aleatoria.strftime('%d/%m/%Y %H:%M:%S')
            servico.gerar_dado_aleatorio(usuario_email, tipo, data_str)
    servico.exportar_dados_csv(usuario_email, caminho_csv)