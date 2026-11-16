"""Citizen Assist AI: assistente de orientação ao cidadão (público: pequenos comércios, tema: energia).

Execute com:  python main.py
"""
import os
import sys

from assistente import Assistente
from base_conhecimento import BaseConhecimento
from orientacao import AVISO

PASTA = os.path.dirname(os.path.abspath(__file__))


def main():
    base = BaseConhecimento(os.path.join(PASTA, "data", "base_conhecimento.json"))
    ok, msg = base.carregar()
    if not ok:
        print(f"Não foi possível iniciar: {msg}")
        return 1

    assistente = Assistente("Citizen Assist AI", base,
                            os.path.join(PASTA, "data", "historico.json"),
                            os.path.join(PASTA, "data", "atendimentos.csv"))
    pendentes = [o.id for o in base.orientacoes if o.pendente]
    print(f"=== {assistente.nome}: energia para pequenos comércios ===")
    print(msg)
    print(AVISO)
    print("Não digite CPF, telefone ou e-mail.")
    if pendentes:
        print(f"(Aviso da equipe: fonte ainda não conferida nas orientações {pendentes}.)")

    inicio_sessao = len(assistente.historico)
    while True:
        print("\n=== Menu ===")
        print("1. Fazer uma pergunta")
        print("2. Navegar por categorias")
        print("3. Ver indicadores")
        print("4. Exportar atendimentos (CSV)")
        print("0. Sair")
        try:
            op = assistente.ler_opcao("Escolha: ", 4)
            if op == 1:
                assistente.perguntar()
            elif op == 2:
                assistente.navegar()
            elif op == 3:
                assistente.exibir_indicadores()
            elif op == 4:
                assistente.exportar_csv()
            else:
                assistente.pedir_nota_facilidade(inicio_sessao)
                print("Até logo!")
                return 0
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            return 0


if __name__ == "__main__":
    sys.exit(main())
