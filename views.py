from automovel import Caminhao, Carro, Automovel
from users import User, Admin, UserRole 
from reserva import Reserva

def tela_login():
    print("\n" + "="*40)
    print("      RECEPÇÃO - GESTÃO DE FROTA      ")
    print("="*40)
    cnh_digitada = input("Digite a sua CNH para entrar: ")

    usuario_db = User.buscar_por_cnh(cnh_digitada)

    if usuario_db is None:
        print("\nUsuário não encontrado.")
        escolha = input("Deseja criar um cadastro agora? (S/N): ").strip().upper()
        
        if escolha == 'S':
            nome = input("Digite o seu nome: ")
            telefone = input("Digite o seu telefone (com DDD, apenas números): ")
            tipo = input("Cadastrar como Cliente comum (1) ou Administrador (2)? ")
            
            try:
                if tipo == '2':
                    novo_usuario = Admin(cnh_digitada, nome, telefone)
                else:
                    novo_usuario = UserRole(cnh_digitada, nome, telefone)
                
                if novo_usuario.salvar():
                    return User.buscar_por_cnh(cnh_digitada)
                    
            except ValueError as e:
                print(f"\nERRO de validação: {e}")
                return None
        
        return None

    return usuario_db


def menu_admin(usuario_logado):
    # Formatando a CNH e o Telefone que vêm brutos do banco de dados para exibição
    cnh_bruta = str(usuario_logado[2])
    cnh_formatada = f"{cnh_bruta[:3]}.{cnh_bruta[3:6]}.{cnh_bruta[6:9]}-{cnh_bruta[9:]}"
    
    while True:
        print(f"\n--- PAINEL ADMINISTRATIVO | Olá, {usuario_logado[3]} ---")
        print(f"--- CNH: {cnh_formatada} ---")
        print("1. Cadastrar novo Veículo")
        print("2. Listar Veículos Disponíveis")
        print("3. Buscar Veículo por Placa")
        print("4. Fazer Logout (Sair)")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            tipo_veiculo = input("\nÉ um Carro (1) ou Caminhão (2)? ")
            modelo = input("Digite o modelo: ")
            try:
                ano = int(input("Digite o ano: "))
                placa = input("Digite a placa (ex: ABC-1234): ")
                
                if tipo_veiculo == '1':
                    novo_veiculo = Carro(ano, modelo, placa)
                else:
                    novo_veiculo = Caminhao(ano, modelo, placa)
                
                novo_veiculo.salvar()
            except Exception as e:
                print(f"\nERRO: {e}")

        elif opcao == '2':
            carros = Automovel.listar_disponiveis()
            if not carros:
                print("\nNão há veículos disponíveis.")
            else:
                for c in carros:
                    placa_bruta = c[2]
                    # Injeta o hífen na placa crua (ex: ABC1234 -> ABC-1234)
                    placa_formatada = f"{placa_bruta[:3]}-{placa_bruta[3:]}"
                    print(f"ID: {c[0]} | {c[1]} | Placa: {placa_formatada} | {c[3]} | Ano: {c[4]}")

        elif opcao == '3':
            placa_busca = input("\nDigite a placa: ")
            carro = Automovel.buscar_por_placa(placa_busca)
            if carro:
                placa_bruta = carro[2]
                placa_formatada = f"{placa_bruta[:3]}-{placa_bruta[3:]}"
                print(f"Encontrado: {carro[1]} {carro[3]} ({placa_formatada}) - Status: {carro[5]}")
            else:
                print("Veículo não encontrado.")

        elif opcao == '4':
            print("Saindo da conta...")
            break


def menu_cliente(usuario_logado):
    # Formatando a CNH e o Telefone que vêm brutos do banco de dados para exibição
    cnh_bruta = str(usuario_logado[2])
    cnh_formatada = f"{cnh_bruta[:3]}.{cnh_bruta[3:6]}.{cnh_bruta[6:9]}-{cnh_bruta[9:]}"
    
    tel_bruto = str(usuario_logado[4])
    # Suportando telefones com 10 ou 11 dígitos
    if len(tel_bruto) == 11:
        tel_formatado = f"({tel_bruto[:2]}) {tel_bruto[2:7]}-{tel_bruto[7:]}"
    else:
        tel_formatado = f"({tel_bruto[:2]}) {tel_bruto[2:6]}-{tel_bruto[6:]}"

    while True:
        print(f"\n--- ÁREA DO CLIENTE | Olá, {usuario_logado[3]} ---")
        print(f"--- CNH: {cnh_formatada} | Contato: {tel_formatado} ---")
        print("1. Ver Veículos Disponíveis")
        print("2. Fazer Logout (Sair)")
        print("3. Alugar Veículo")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            carros = Automovel.listar_disponiveis()
            if not carros:
                print("\nNão há veículos disponíveis.")
            else:
                for c in carros:
                    placa_bruta = c[2]
                    placa_formatada = f"{placa_bruta[:3]}-{placa_bruta[3:]}"
                    print(f"ID: {c[0]} | {c[1]} | Placa: {placa_formatada} | {c[3]} | Ano: {c[4]}")
                    
        elif opcao == '2':
            print("Saindo da conta...")
            break
            
        elif opcao == '3':
            print("\n--- ALUGAR VEÍCULO ---")
            placa = input("Digite a placa do veículo que deseja alugar: ")
            
            carro = Automovel.buscar_por_placa(placa)
            
            if not carro:
                print("❌ Veículo não encontrado. Verifique a placa e tente novamente.")
                continue
            
            id_carro = carro[0]
            placa_bruta = carro[2]
            placa_formatada = f"{placa_bruta[:3]}-{placa_bruta[3:]}"
            
            print("\nFormato aceito: DD/MM/AAAA")
            data_inicio = input("Data de retirada: ")
            data_final = input("Data de devolução: ")
            
            try:
                if Reserva.verificar_disp(id_carro, data_inicio, data_final):
                    
                    nova_reserva = Reserva(usuario_logado[0], id_carro, data_inicio, data_final)
                    
                    if nova_reserva.salvar_datas():
                        print(f"🎉 Reserva do veículo {carro[3]} (Placa: {placa_formatada}) confirmada com sucesso!")
                else:
                    print("⚠️ Desculpe, este veículo já se encontra alugado para as datas selecionadas.")
                    
            except ValueError:
                print("❌ Erro: Formato de data inválido. Certifique-se de usar o formato DD/MM/AAAA.")
            except Exception as e:
                print(f"❌ Ocorreu um erro no sistema: {e}")


def main():
    while True:
        usuario = tela_login()
        
        if usuario:
            role = usuario[1] # O índice 1 contém a string 'Admin' ou 'User'
            
            if role == "Admin":
                menu_admin(usuario)
            else:
                menu_cliente(usuario)
        else:
            print("\nRetornando ao início...")


if __name__ == "__main__":
    main()
    