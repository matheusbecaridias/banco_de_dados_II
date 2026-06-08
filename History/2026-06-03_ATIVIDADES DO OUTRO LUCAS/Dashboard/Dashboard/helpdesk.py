import mysql.connector
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO — ajuste host/user/password conforme seu ambiente
# ─────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "sua_senha",   # ← altere aqui
    "database": "helpDesk",
    "charset":  "utf8mb4",
}

# ─────────────────────────────────────────────────────────────
# BANCO DE DADOS
# ─────────────────────────────────────────────────────────────

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def inicializar_bd():
    cfg = {**DB_CONFIG}
    cfg.pop("database")                       # conecta sem banco primeiro
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()

    cur.execute("CREATE SCHEMA IF NOT EXISTS helpDesk")
    cur.execute("USE helpDesk")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tecnicos (
            id                  INT          PRIMARY KEY AUTO_INCREMENT,
            nome                VARCHAR(100) NOT NULL UNIQUE,
            quantidade_chamados INT          NOT NULL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id                  INT          PRIMARY KEY AUTO_INCREMENT,
            equipamento         VARCHAR(100) NOT NULL  COMMENT 'Nome do equipamento',
            problema            TEXT         NOT NULL  COMMENT 'Descrição do problema',
            prioridade          INT          NOT NULL  COMMENT '1-Alto 2-Médio 3-Baixo',
            tecnico_responsavel VARCHAR(100) NOT NULL,
            status              ENUM('Aberto','Finalizado') NOT NULL DEFAULT 'Aberto',
            data_abertura       DATETIME     NOT NULL,
            data_fechamento     DATETIME     DEFAULT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

# ─────────────────────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────────────────────

PRIORIDADE_LABEL = {1: "Alto", 2: "Médio", 3: "Baixo"}
PRIORIDADE_EMOJI = {1: "🔴", 2: "🟡", 3: "🟢"}

def linha(char="─", n=52):
    print(char * n)

def cabecalho(titulo):
    print()
    linha("═")
    print(f"  {titulo}")
    linha("═")

def pausar():
    input("\n  Pressione Enter para continuar...")

def now():
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
        print("  ⚠  Opção inválida.")

# ─────────────────────────────────────────────────────────────
# 1. ABRIR CHAMADO
# ─────────────────────────────────────────────────────────────

def abrir_chamado():
    cabecalho("📋  ABRIR CHAMADO")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT nome FROM tecnicos ORDER BY nome")
    tecnicos_bd = cur.fetchall()
    if tecnicos_bd:
        print("  Técnicos cadastrados:")
        for (nome,) in tecnicos_bd:
            print(f"    • {nome}")
    print()

    equipamento = input("  Equipamento: ").strip()
    if not equipamento:
        print("  ⚠  Campo obrigatório."); cur.close(); conn.close(); return

    problema = input("  Problema identificado: ").strip()
    if not problema:
        print("  ⚠  Campo obrigatório."); cur.close(); conn.close(); return

    prioridade = escolher_prioridade()

    tecnico = input("  Técnico responsável: ").strip()
    if not tecnico:
        print("  ⚠  Campo obrigatório."); cur.close(); conn.close(); return

    data_abertura = now()

    cur.execute(
        "INSERT INTO chamados (equipamento,problema,prioridade,tecnico_responsavel,data_abertura) "
        "VALUES (%s,%s,%s,%s,%s)",
        (equipamento, problema, prioridade, tecnico, data_abertura)
    )
    chamado_id = cur.lastrowid

    cur.execute("SELECT id FROM tecnicos WHERE nome=%s", (tecnico,))
    if cur.fetchone():
        cur.execute("UPDATE tecnicos SET quantidade_chamados=quantidade_chamados+1 WHERE nome=%s", (tecnico,))
    else:
        cur.execute("INSERT INTO tecnicos (nome,quantidade_chamados) VALUES (%s,1)", (tecnico,))

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n  ✅  Chamado #{chamado_id} aberto em {data_abertura}")
    print(f"  {PRIORIDADE_EMOJI[prioridade]} Prioridade: {PRIORIDADE_LABEL[prioridade]}")
    pausar()

# ─────────────────────────────────────────────────────────────
# 2. FINALIZAR CHAMADO
# ─────────────────────────────────────────────────────────────

def finalizar_chamado():
    cabecalho("✅  FINALIZAR CHAMADO")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, equipamento, prioridade, tecnico_responsavel, data_abertura
        FROM chamados WHERE status='Aberto'
        ORDER BY prioridade, data_abertura
    """)
    abertos = cur.fetchall()

    if not abertos:
        print("  Nenhum chamado aberto no momento.")
        cur.close(); conn.close(); pausar(); return

    print(f"  {'ID':<6} {'Equipamento':<22} {'Técnico':<20} {'Prio':<8} Aberto em")
    linha()
    for cid, eq, prio, tec, dt in abertos:
        print(f"  #{cid:<5} {eq:<22} {tec:<20} {PRIORIDADE_EMOJI[prio]}{PRIORIDADE_LABEL[prio]:<7} {dt}")

    print()
    try:
        cid = int(input("  ID do chamado a finalizar (0 = cancelar): "))
    except ValueError:
        cur.close(); conn.close(); return

    if cid == 0:
        cur.close(); conn.close(); return

    cur.execute("SELECT id FROM chamados WHERE id=%s AND status='Aberto'", (cid,))
    if not cur.fetchone():
        print("  ⚠  Chamado não encontrado ou já finalizado.")
        cur.close(); conn.close(); pausar(); return

    data_fechamento = now()
    cur.execute(
        "UPDATE chamados SET status='Finalizado', data_fechamento=%s WHERE id=%s",
        (data_fechamento, cid)
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"\n  ✅  Chamado #{cid} finalizado em {data_fechamento}.")
    pausar()

# ─────────────────────────────────────────────────────────────
# 3. RANKING DE TÉCNICOS
# ─────────────────────────────────────────────────────────────

def ranking_tecnicos():
    cabecalho("🏆  RANKING DE TÉCNICOS")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, quantidade_chamados FROM tecnicos ORDER BY quantidade_chamados DESC, nome")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("  Nenhum técnico registrado ainda.")
        pausar(); return

    medalhas = ["🥇", "🥈", "🥉"]
    print(f"  {'Pos.':<6} {'Técnico':<30} {'Qtd':>4}  Barra")
    linha()
    for i, (nome, qtd) in enumerate(rows):
        pos = medalhas[i] if i < 3 else f"  {i+1}."
        bar = "█" * min(qtd, 30)
        print(f"  {pos:<6} {nome:<30} {qtd:>4}  {bar}")

    pausar()

# ─────────────────────────────────────────────────────────────
# 4. DASHBOARD
# ─────────────────────────────────────────────────────────────

def dashboard():
    cabecalho("📊  DASHBOARD — HELP DESK")

    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM chamados")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM chamados WHERE status='Aberto'")
    abertos = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM chamados WHERE status='Finalizado'")
    finalizados = cur.fetchone()[0]

    cur.execute("SELECT prioridade, COUNT(*) FROM chamados GROUP BY prioridade ORDER BY prioridade")
    por_prio = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute("SELECT nome, quantidade_chamados FROM tecnicos ORDER BY quantidade_chamados DESC LIMIT 5")
    top = cur.fetchall()

    cur.close()
    conn.close()

    print(f"\n  📁  Total de chamados   : {total}")
    print(f"  🟦  Abertos             : {abertos}")
    print(f"  ✅  Finalizados         : {finalizados}")

    linha()
    print("  Por prioridade:")
    for p in (1, 2, 3):
        qtd = por_prio.get(p, 0)
        bar = "▮" * qtd
        print(f"    {PRIORIDADE_EMOJI[p]} {PRIORIDADE_LABEL[p]:<6}: {qtd:>3}  {bar}")

    if top:
        linha()
        print("  🏆  Top 5 técnicos:")
        medals = ["🥇","🥈","🥉"]
        for i, (nome, qtd) in enumerate(top):
            m = medals[i] if i < 3 else f"  {i+1}."
            print(f"    {m} {nome:<28} — {qtd} chamado(s)")

    pausar()

# ─────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────────────────────

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
            print("\n  👋  Encerrando. Até logo!\n")
            break
        else:
            print("  ⚠  Opção inválida!")
            pausar()

if __name__ == "__main__":
    menu()
