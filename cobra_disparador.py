# COBRA - DISPARADOR AUTOMÁTICO v3.2 (SESSÃO ÚNICA)
from telethon import TelegramClient, errors
from datetime import datetime, time
import asyncio
import pytz
import os

# CONFIGURAÇÕES ESPECÍFICAS PARA O NÚMERO +5511977645726
API_ID = 23219166
API_HASH = '63f5fc1d1eab6902c0550cbf1098c3b6'
HORARIO_DISPARO = time(20, 0, 0)  # 13:20 (1:20 PM)
MENSAGEM = "Jana x Braga r2"
NOME_SESSAO = 'COBRA_5511977645726'  # Sessão única para este número
TZ = pytz.timezone('America/Sao_Paulo')

async def selecionar_grupo(client):
    """Seleção de grupos da conta correta"""
    try:
        # Forçar atualização dos diálogos
        await client.get_dialogs()
        
        grupos = [d for d in await client.get_dialogs() if d.is_group]
        
        print("\n" + "="*40)
        print(f"{' GRUPOS DA CONTA +5511977645726 ':=^40}")
        for idx, grupo in enumerate(grupos, 1):
            print(f"[{idx}] {grupo.title}")
        print("="*40)

        while True:
            escolha = input("\nDigite o número do grupo: ")
            if escolha.isdigit() and 0 < int(escolha) <= len(grupos):
                grupo = grupos[int(escolha)-1]
                print(f"\n✔ Grupo selecionado: {grupo.title}")
                return grupo.id
            print("⚠ Erro: Digite um número válido da lista")
            
    except Exception as e:
        print(f"\n❌ Falha ao carregar grupos: {str(e)}")
        raise

async def disparar_mensagem(client, grupo_id):
    """Disparo exclusivo para a conta configurada"""
    try:
        print("\n" + "="*40)
        print(f"{' DISPARADOR ATIVADO ':=^40}")
        print(f"Conta: +5511977645726")
        print(f"Alvo: {HORARIO_DISPARO.strftime('%H:%M:%S')}")
        print(f"Mensagem: '{MENSAGEM}'")
        print("="*40)

        while True:
            agora = datetime.now(TZ)
            alvo = TZ.localize(datetime.combine(agora.date(), HORARIO_DISPARO))
            
            if agora >= alvo:
                try:
                    await client.send_message(grupo_id, MENSAGEM)
                    print("\n" + "="*40)
                    print(f"{'✅ MENSAGEM ENVIADA! ':=^40}")
                    print(f"Horário: {agora.strftime('%H:%M:%S')}")
                    print("="*40)
                    return
                    
                except errors.ChatWriteForbiddenError:
                    print("⏳ Grupo fechado. Tentando...", end='\r')
                    await asyncio.sleep(0.2)
                    
                except Exception as e:
                    print(f"\n❌ Erro: {str(e)}")
                    return
            else:
                faltam = alvo - agora
                print(f"🕒 Contagem: {faltam.seconds//3600:02d}:{(faltam.seconds//60)%60:02d}:{faltam.seconds%60:02d}", end='\r')
                await asyncio.sleep(0.1)

    except Exception as e:
        print(f"\n❌ Falha crítica: {str(e)}")
        raise

async def main():
    # Remover sessões conflitantes
    if os.path.exists(f'{NOME_SESSAO}.session'):
        os.remove(f'{NOME_SESSAO}.session')
    
    client = TelegramClient(NOME_SESSAO, API_ID, API_HASH)
    
    try:
        # Autenticação forçada para a conta específica
        await client.start(phone='+5511977645726')
        
        # Seleção de grupo
        grupo_id = await selecionar_grupo(client)
        
        # Ativar sistema
        await disparar_mensagem(client, grupo_id)

    except KeyboardInterrupt:
        print("\n⚠ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ ERRO GLOBAL: {str(e)}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    print("\n" + "="*40)
    print(f"{' DISPARADOR OFICIAL - +5511977645726 ':=^40}")
    asyncio.run(main())