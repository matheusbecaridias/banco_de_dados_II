// ═══════════════════════════════════════════════════════════
//  Help Desk — Frontend JS
//  Simula dados vindos do MySQL (substituir por fetch() / API)
// ═══════════════════════════════════════════════════════════

// ─── DADOS SIMULADOS (substituir por chamadas ao backend) ──
let DB = {
  chamados: [
    { id:1,  equipamento:"Notebook Dell XPS",   problema:"Tela piscando ao usar bateria",        prioridade:1, tecnico:"Carlos Lima",   status:"Aberto",    data_abertura:"2025-05-18 08:14", data_fechamento:null },
    { id:2,  equipamento:"Impressora HP LaserJet",problema:"Não imprime — fila travada",          prioridade:2, tecnico:"Ana Souza",     status:"Finalizado",data_abertura:"2025-05-18 09:02", data_fechamento:"2025-05-18 10:30" },
    { id:3,  equipamento:"Desktop i5 — Setor RH",problema:"Lentidão extrema ao abrir sistema",   prioridade:1, tecnico:"Carlos Lima",   status:"Aberto",    data_abertura:"2025-05-19 07:50", data_fechamento:null },
    { id:4,  equipamento:"Switch Cisco SG300",   problema:"Porta #6 sem link",                   prioridade:1, tecnico:"Bruno Melo",    status:"Aberto",    data_abertura:"2025-05-19 08:30", data_fechamento:null },
    { id:5,  equipamento:"Monitor LG 27\"",      problema:"Sem sinal após atualização",           prioridade:3, tecnico:"Débora Neves",  status:"Finalizado",data_abertura:"2025-05-19 09:00", data_fechamento:"2025-05-19 11:00" },
    { id:6,  equipamento:"Teclado sem fio",      problema:"Teclas F1-F4 não respondem",           prioridade:3, tecnico:"Ana Souza",     status:"Finalizado",data_abertura:"2025-05-19 10:10", data_fechamento:"2025-05-19 10:45" },
    { id:7,  equipamento:"Servidor NAS",         problema:"Volume RAID degradado",                prioridade:1, tecnico:"Carlos Lima",   status:"Aberto",    data_abertura:"2025-05-20 07:00", data_fechamento:null },
    { id:8,  equipamento:"Projetor Epson",       problema:"Lâmpada com vida útil baixa",         prioridade:2, tecnico:"Débora Neves",  status:"Aberto",    data_abertura:"2025-05-20 08:20", data_fechamento:null },
    { id:9,  equipamento:"Notebook Lenovo T14",  problema:"Bateria não carrega acima de 80%",    prioridade:2, tecnico:"Ana Souza",     status:"Finalizado",data_abertura:"2025-05-20 09:00", data_fechamento:"2025-05-20 11:30" },
    { id:10, equipamento:"Access Point WiFi",    problema:"Queda frequente na sala de reunião",  prioridade:1, tecnico:"Bruno Melo",    status:"Aberto",    data_abertura:"2025-05-20 09:45", data_fechamento:null },
  ],
  nextId: 11,
};

function getRanking() {
  const map = {};
  DB.chamados.forEach(c => {
    if (!map[c.tecnico]) map[c.tecnico] = 0;
    map[c.tecnico]++;
  });
  return Object.entries(map)
    .map(([nome, count]) => ({ nome, count }))
    .sort((a,b) => b.count - a.count);
}

// ─── NAVIGATION ───────────────────────────────────────────
const PAGE_LABELS = {
  dashboard: "DASHBOARD",
  abrir:     "ABRIR CHAMADO",
  chamados:  "CHAMADOS",
  ranking:   "RANKING DE TÉCNICOS",
};

function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  document.querySelector(`[data-page="${id}"]`).classList.add('active');
  document.getElementById('page-label').textContent = PAGE_LABELS[id];

  if (id === 'dashboard') renderDashboard();
  if (id === 'chamados')  renderChamados();
  if (id === 'ranking')   renderRanking();
}

// ─── CLOCK ────────────────────────────────────────────────
function tick() {
  const t = new Date().toLocaleTimeString('pt-BR', { hour:'2-digit', minute:'2-digit', second:'2-digit' });
  const d = new Date().toLocaleDateString('pt-BR', { weekday:'short', day:'2-digit', month:'short' });
  document.getElementById('clock-side').textContent = t;
  document.getElementById('clock-top').textContent  = `${d} — ${t}`;
}
tick(); setInterval(tick, 1000);

// ─── HELPERS ──────────────────────────────────────────────
const PRIO_LABEL = { 1:'Alto', 2:'Médio', 3:'Baixo' };
const PRIO_CLASS = { 1:'high', 2:'med', 3:'low' };
const MEDALS     = ['🥇','🥈','🥉'];

function badge(text, cls) {
  return `<span class="badge badge-${cls}">${text}</span>`;
}
function priBadge(p) {
  return badge(PRIO_LABEL[p], PRIO_CLASS[p]);
}
function statusBadge(s) {
  return badge(s, s === 'Aberto' ? 'open' : 'done');
}
function initials(name) {
  return name.split(' ').slice(0,2).map(w=>w[0]).join('').toUpperCase();
}

// ─── DASHBOARD ────────────────────────────────────────────
function renderDashboard() {
  const total     = DB.chamados.length;
  const abertos   = DB.chamados.filter(c => c.status === 'Aberto').length;
  const finalizados = total - abertos;
  const altos     = DB.chamados.filter(c => c.prioridade === 1).length;
  const medios    = DB.chamados.filter(c => c.prioridade === 2).length;
  const baixos    = DB.chamados.filter(c => c.prioridade === 3).length;

  document.getElementById('m-total').textContent = total;
  document.getElementById('m-open').textContent  = abertos;
  document.getElementById('m-done').textContent  = finalizados;
  document.getElementById('m-high').textContent  = altos;

  document.getElementById('bar-open').style.width = total ? Math.round(abertos/total*100)+'%' : '0%';
  document.getElementById('bar-done').style.width = total ? Math.round(finalizados/total*100)+'%' : '0%';
  document.getElementById('bar-high').style.width = total ? Math.round(altos/total*100)+'%' : '0%';

  // Recent
  const recent = [...DB.chamados].reverse().slice(0, 6);
  document.getElementById('tbl-recent').innerHTML = recent.map(c => `
    <tr>
      <td class="mono">#${c.id}</td>
      <td>${c.equipamento}</td>
      <td>${c.tecnico}</td>
      <td>${priBadge(c.prioridade)}</td>
      <td>${statusBadge(c.status)}</td>
      <td class="mono" style="color:var(--dim);font-size:11px">${c.data_abertura.split(' ')[0]}</td>
    </tr>
  `).join('');

  // Prio chart
  const maxP = Math.max(altos, medios, baixos, 1);
  document.getElementById('prio-chart').innerHTML = `
    <div class="prio-row">
      <span class="prio-name">🔴 Alto</span>
      <div class="prio-track"><div class="prio-fill fill-high" style="width:${Math.round(altos/maxP*100)}%"></div></div>
      <span class="prio-count">${altos}</span>
    </div>
    <div class="prio-row">
      <span class="prio-name">🟡 Médio</span>
      <div class="prio-track"><div class="prio-fill fill-med" style="width:${Math.round(medios/maxP*100)}%"></div></div>
      <span class="prio-count">${medios}</span>
    </div>
    <div class="prio-row">
      <span class="prio-name">🟢 Baixo</span>
      <div class="prio-track"><div class="prio-fill fill-low" style="width:${Math.round(baixos/maxP*100)}%"></div></div>
      <span class="prio-count">${baixos}</span>
    </div>
  `;

  // Rank mini
  const ranking = getRanking().slice(0, 5);
  const maxR = ranking[0]?.count || 1;
  document.getElementById('rank-mini').innerHTML = ranking.map((r,i) => `
    <div class="rank-row-mini">
      <span class="rank-medal">${MEDALS[i] || (i+1)}</span>
      <span class="rank-name-mini">${r.nome}</span>
      <div class="rank-bar-mini"><div class="rank-fill-mini" style="width:${Math.round(r.count/maxR*100)}%"></div></div>
      <span class="rank-count-mini">${r.count} ch.</span>
    </div>
  `).join('');
}

// ─── CHAMADOS ─────────────────────────────────────────────
function renderChamados() {
  const fStatus = document.getElementById('flt-status').value;
  const fPrio   = document.getElementById('flt-prio').value;
  const fSearch = document.getElementById('flt-search').value.toLowerCase();

  let list = [...DB.chamados].reverse();
  if (fStatus) list = list.filter(c => c.status === fStatus);
  if (fPrio)   list = list.filter(c => c.prioridade == fPrio);
  if (fSearch) list = list.filter(c =>
    c.equipamento.toLowerCase().includes(fSearch) ||
    c.tecnico.toLowerCase().includes(fSearch) ||
    c.problema.toLowerCase().includes(fSearch)
  );

  const tb = document.getElementById('tbl-chamados');
  if (!list.length) {
    tb.innerHTML = `<tr><td colspan="9" class="empty">NENHUM CHAMADO ENCONTRADO</td></tr>`;
    return;
  }

  tb.innerHTML = list.map(c => `
    <tr>
      <td class="mono">#${c.id}</td>
      <td>${c.equipamento}</td>
      <td style="color:var(--dim);max-width:200px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">${c.problema}</td>
      <td>${c.tecnico}</td>
      <td>${priBadge(c.prioridade)}</td>
      <td>${statusBadge(c.status)}</td>
      <td class="mono" style="color:var(--dim);font-size:11px">${c.data_abertura}</td>
      <td class="mono" style="color:var(--dim);font-size:11px">${c.data_fechamento || '—'}</td>
      <td>${c.status === 'Aberto' ? `<button class="btn-fin" onclick="openModal(${c.id})">FINALIZAR</button>` : ''}</td>
    </tr>
  `).join('');
}

// ─── RANKING ──────────────────────────────────────────────
function renderRanking() {
  const ranking = getRanking();
  const maxR = ranking[0]?.count || 1;

  const posClass = ['gold','silver','bronze'];
  document.getElementById('rank-full').innerHTML = ranking.map((r, i) => `
    <div class="rank-full-row">
      <div class="rank-full-pos ${posClass[i] || ''}">${String(i+1).padStart(2,'0')}</div>
      <div class="rank-full-avatar">${initials(r.nome)}</div>
      <div class="rank-full-name">${r.nome}</div>
      <div class="rank-full-bar"><div class="rank-full-fill" style="width:${Math.round(r.count/maxR*100)}%"></div></div>
      <div class="rank-full-count">${r.count}</div>
    </div>
  `).join('');
}

// ─── ABRIR CHAMADO ────────────────────────────────────────
function abrirChamado(e) {
  e.preventDefault();
  const equip   = document.getElementById('f-equip').value.trim();
  const problema= document.getElementById('f-problema').value.trim();
  const prio    = parseInt(document.getElementById('f-prio').value);
  const tec     = document.getElementById('f-tec').value.trim();

  const id = DB.nextId++;
  const now = new Date().toLocaleString('sv').replace('T',' ').slice(0,16);

  DB.chamados.push({ id, equipamento:equip, problema, prioridade:prio,
    tecnico:tec, status:'Aberto', data_abertura:now, data_fechamento:null });

  // Exibir confirmação
  const box = document.getElementById('confirm-box');
  box.style.display = '';
  document.getElementById('confirm-content').innerHTML = `
    <div class="confirm-id">CHAMADO #${id} ABERTO</div>
    <div class="confirm-line"><span class="confirm-key">EQUIPAMENTO</span><span class="confirm-val">${equip}</span></div>
    <div class="confirm-line"><span class="confirm-key">PROBLEMA</span><span class="confirm-val">${problema}</span></div>
    <div class="confirm-line"><span class="confirm-key">PRIORIDADE</span><span class="confirm-val">${priBadge(prio)}</span></div>
    <div class="confirm-line"><span class="confirm-key">TÉCNICO</span><span class="confirm-val">${tec}</span></div>
    <div class="confirm-line"><span class="confirm-key">ABERTURA</span><span class="confirm-val" style="font-family:var(--font-mono);font-size:12px">${now}</span></div>
  `;

  e.target.reset();
}

// ─── MODAL FINALIZAR ──────────────────────────────────────
let modalChamadoId = null;

function openModal(id) {
  const c = DB.chamados.find(x => x.id === id);
  if (!c) return;
  modalChamadoId = id;

  document.getElementById('modal-body').innerHTML = `
    <div class="confirm-line"><span class="confirm-key">CHAMADO</span><span class="confirm-val" style="font-family:var(--font-mono)">#${c.id}</span></div>
    <div class="confirm-line"><span class="confirm-key">EQUIPAMENTO</span><span class="confirm-val">${c.equipamento}</span></div>
    <div class="confirm-line"><span class="confirm-key">TÉCNICO</span><span class="confirm-val">${c.tecnico}</span></div>
    <div class="confirm-line"><span class="confirm-key">PRIORIDADE</span><span class="confirm-val">${priBadge(c.prioridade)}</span></div>
    <p style="margin-top:16px;font-size:12px;color:var(--dim)">Esta ação irá registrar a data/hora de fechamento e alterar o status para <span style="color:var(--green)">Finalizado</span>.</p>
  `;

  document.getElementById('btn-confirm-fin').onclick = finalizarChamado;
  document.getElementById('modal').classList.add('open');
}

function closeModal() {
  document.getElementById('modal').classList.remove('open');
  modalChamadoId = null;
}

function finalizarChamado() {
  if (!modalChamadoId) return;
  const c = DB.chamados.find(x => x.id === modalChamadoId);
  if (c) {
    c.status = 'Finalizado';
    c.data_fechamento = new Date().toLocaleString('sv').replace('T',' ').slice(0,16);
  }
  closeModal();
  renderChamados();
}

// ─── INIT ─────────────────────────────────────────────────
renderDashboard();
