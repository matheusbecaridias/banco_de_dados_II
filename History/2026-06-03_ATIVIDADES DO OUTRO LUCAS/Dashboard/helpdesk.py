import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "helpdesk.db")

# ─────────────────────────────────────────
# BANCO DE DADOS
# ─────────────────────────────────────────

def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_bd():
    conn = conectar()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS tecnicos (
            id                 INTEGER PRIMARY KEY AUTOINCREMENT,
            nome               TEXT    NOT NULL UNIQUE,
            quantidade_chamados INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chamados (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            equipamento       TEXT    NOT NULL,
            problema          TEXT    NOT NULL,
            prioridade        INTEGER NOT NULL CHECK(prioridade IN (1,2,3)),
            tecnico_responsavel TEXT  NOT NULL,
            status            TEXT    NOT NULL DEFAULT 'Aberto'
                                      CHECK(status IN ('Aberto','Finalizado')),
            data_abertura     TEXT    NOT NULL,
            data_fechamento   TEXT
        );
    """)

    conn.commit()
    conn.close()

# ─────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────

PRIORIDADE_LABEL = {1: "Alto", 2: "Médio", 3: "Baixo"}
PRIORIDADE_EMOJI = {1: "🔴", 2: "🟡", 3: "🟢"}

def linha(char="─", n=50):
    print(char * n)

def cabecalho(titulo):
    print()
    linha("═")
    print(f"  {titulo}")
    linha("═")

def pausar():
    input("\n  Pressione Enter para continuar...")

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def escolher_prioridade():
    while True:
        print("  Prioridade:")
        print("    1 - 🔴 Alto")
        print("    2 - 🟡 Médio")
        print("    3 - 🟢 Baixo")
        op = input("  Escolha (1/2/3): ").strip()
        if op in ("1", "2", "3"):
            return int(op)
        print("  ⚠  Opção inválida. Tente novamente.")

def listar_tecnicos_disponiveis(cur):
    cur.execute("SELECT nome FROM tecnicos ORDER BY nome")
    rows = cur.fetchall()
    if rows:
        print("  Técnicos cadastrados:")
        for i, (nome,) in enumerate(rows, 1):
            print(f"    {i}. {nome}")
    return rows

# ─────────────────────────────────────────
# 1. ABRIR CHAMADO
# ─────────────────────────────────────────

def abrir_chamado():
    cabecalho("📋  ABRIR CHAMADO")

    conn = conectar()
    cur = conn.cursor()

    listar_tecnicos_disponiveis(cur)
    print()

    equipamento = input("  Equipamento: ").strip()
    if not equipamento:
        print("  ⚠  Campo obrigatório."); conn.close(); return

    problema = input("  Problema identificado: ").strip()
    if not problema:
        print("  ⚠  Campo obrigatório."); conn.close(); return

    prioridade = escolher_prioridade()

    tecnico = input("  Técnico responsável (nome completo): ").strip()
    if not tecnico:
        print("  ⚠  Campo obrigatório."); conn.close(); return

    data_abertura = now_str()

    cur.execute("""
        INSERT INTO chamados (equipamento, problema, prioridade,
                              tecnico_responsavel, data_abertura)
        VALUES (?, ?, ?, ?, ?)
    """, (equipamento, problema, prioridade, tecnico, data_abertura))
    chamado_id = cur.lastrowid

    # Atualiza (ou cria) técnico no ranking
    cur.execute("SELECT id FROM tecnicos WHERE nome = ?", (tecnico,))
    if cur.fetchone():
        cur.execute("""
            UPDATE tecnicos SET quantidade_chamados = quantidade_chamados + 1
            WHERE nome = ?
        """, (tecnico,))
    else:
        cur.execute("""
            INSERT INTO tecnicos (nome, quantidade_chamados) VALUES (?, 1)
        """, (tecnico,))

    conn.commit()
    conn.close()

    print(f"\n  ✅  Chamado #{chamado_id} aberto com sucesso!")
    print(f"  📅  Data/hora: {data_abertura}")
    print(f"  {PRIORIDADE_EMOJI[prioridade]} Prioridade: {PRIORIDADE_LABEL[prioridade]}")
    pausar()

# ─────────────────────────────────────────
# 2. FINALIZAR CHAMADO
# ─────────────────────────────────────────

def finalizar_chamado():
    cabecalho("✅  FINALIZAR CHAMADO")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, equipamento, problema, prioridade, tecnico_responsavel, data_abertura
        FROM chamados
        WHERE status = 'Aberto'
        ORDER BY prioridade, data_abertura
    """)
    abertos = cur.fetchall()

    if not abertos:
        print("  Nenhum chamado aberto no momento.")
        conn.close(); pausar(); return

    print(f"  {'ID':<6} {'Equip.':<20} {'Técnico':<20} {'Prior.':<8} {'Aberto em'}")
    linha()
    for row in abertos:
        cid, eq, _, prio, tec, dt = row
        print(f"  #{cid:<5} {eq:<20} {tec:<20} {PRIORIDADE_EMOJI[prio]}{PRIORIDADE_LABEL[prio]:<7} {dt}")

    print()
    try:
        cid = int(input("  ID do chamado a finalizar (0 para cancelar): "))
    except ValueError:
        conn.close(); return

    if cid == 0:
        conn.close(); return

    cur.execute("SELECT id FROM chamados WHERE id = ? AND status = 'Aberto'", (cid,))
    if not cur.fetchone():
        print("  ⚠  Chamado não encontrado ou já finalizado.")
        conn.close(); pausar(); return

    data_fechamento = now_str()
    cur.execute("""
        UPDATE chamados
        SET status = 'Finalizado', data_fechamento = ?
        WHERE id = ?
    """, (data_fechamento, cid))

    conn.commit()
    conn.close()

    print(f"\n  ✅  Chamado #{cid} finalizado em {data_fechamento}.")
    pausar()

# ─────────────────────────────────────────
# 3. RANKING DE TÉCNICOS
# ─────────────────────────────────────────

def ranking_tecnicos():
    cabecalho("🏆  RANKING DE TÉCNICOS")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT nome, quantidade_chamados
        FROM tecnicos
        ORDER BY quantidade_chamados DESC, nome
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("  Nenhum técnico registrado ainda.")
        pausar(); return

    medalhas = ["🥇", "🥈", "🥉"]
    print(f"  {'Pos.':<6} {'Técnico':<30} {'Chamados'}")
    linha()
    for i, (nome, qtd) in enumerate(rows):
        pos = medalhas[i] if i < 3 else f"  {i+1}."
        bar = "█" * min(qtd, 30)
        print(f"  {pos:<6} {nome:<30} {qtd:>3}  {bar}")

    pausar()

# ─────────────────────────────────────────
# 4. DASHBOARD
# ─────────────────────────────────────────

def dashboard():
    cabecalho("📊  DASHBOARD — HELP DESK")

    conn = conectar()
    cur = conn.cursor()

    # Totais
    cur.execute("SELECT COUNT(*) FROM chamados")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM chamados WHERE status = 'Aberto'")
    abertos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM chamados WHERE status = 'Finalizado'")
    finalizados = cur.fetchone()[0]

    # Por prioridade
    cur.execute("""
        SELECT prioridade, COUNT(*) FROM chamados
        GROUP BY prioridade ORDER BY prioridade
    """)
    por_prio = {row[0]: row[1] for row in cur.fetchall()}

    # Ranking top 5
    cur.execute("""
        SELECT nome, quantidade_chamados FROM tecnicos
        ORDER BY quantidade_chamados DESC LIMIT 5
    """)
    top_tecs = cur.fetchall()

    conn.close()

    print(f"\n  📁  Total de chamados   : {total}")
    print(f"  🟦  Chamados abertos    : {abertos}")
    print(f"  ✅  Chamados finalizados: {finalizados}")

    linha()
    print("  Por prioridade:")
    for p in (1, 2, 3):
        qtd = por_prio.get(p, 0)
        bar = "▮" * qtd
        print(f"    {PRIORIDADE_EMOJI[p]} {PRIORIDADE_LABEL[p]:<6}: {qtd:>3}  {bar}")

    if top_tecs:
        linha()
        print("  🏆  Top técnicos:")
        for i, (nome, qtd) in enumerate(top_tecs, 1):
            print(f"    {i}. {nome:<28} — {qtd} chamado(s)")

    pausar()

# ─────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────

def menu():
    inicializar_bd()
    while True:
        cabecalho("🖥️   SISTEMA HELP DESK")
        print("  1. 📋  Abrir chamado")
        print("  2. ✅  Finalizar chamado")
        print("  3. 🏆  Ranking de técnicos")
        print("  4. 📊  Dashboard")
        print("  5. 🚪  Sair do sistema")
        linha()
        op = input("  Escolha uma opção: ").strip()

        if op == "1":
            abrir_chamado()
        elif op == "2":
            finalizar_chamado()
        elif op == "3":
            ranking_tecnicos()
        elif op == "4":
            dashboard()
        elif op == "5":
            print("\n  👋  Encerrando o sistema. Até logo!\n")
            break
        else:
            print("  ⚠  Opção inválida! Tente novamente.")
            pausar()

if __name__ == "__main__":
    menu()
