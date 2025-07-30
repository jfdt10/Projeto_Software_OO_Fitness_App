from fitness_app.core.utils import gerar_csv_wearable_aleatorio
from fitness_app.services.wearable import ServicoWearable
import os

os.makedirs("fitness_app/data", exist_ok=True)
servico = ServicoWearable()
usuario_email = "usuario@exemplo.com"
caminho_csv = "fitness_app/data/wearable.csv"
tipos = ["passos", "batimentos", "sono"]

gerar_csv_wearable_aleatorio(servico, usuario_email, caminho_csv, tipos, dias=30)