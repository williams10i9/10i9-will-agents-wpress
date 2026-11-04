const form = document.querySelector('#mission-form');
const input = document.querySelector('#message');
const button = document.querySelector('#send');
const messages = document.querySelector('#messages');
const agents = document.querySelector('#agents');
const events = document.querySelector('#events');
const status = document.querySelector('#status');
const ollamaHost = document.querySelector('#ollama-host');
const ollamaUrl = document.querySelector('#ollama-url');
let shownResults = new Set();

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, character => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[character]));
}

function inline(text) {
  return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

function renderMessage(text, type) {
  if (type === 'user') return inline(text);
  const lines = text.trim().split('\n');
  let html = '';
  let listOpen = false;
  for (const rawLine of lines) {
    const line = rawLine.trimEnd();
    if (line.startsWith('- ')) {
      if (!listOpen) { html += '<ul class="result-list">'; listOpen = true; }
      else html += '</li>';
      html += `<li>${inline(line.slice(2))}`;
      continue;
    }
    if (line.startsWith('  ') && listOpen) {
      html += `<span class="issue-meta">${inline(line.trim())}</span></li>`;
      continue;
    }
    if (listOpen) { html += '</li></ul>'; listOpen = false; }
    if (!line.trim()) continue;
    if (/^\*\*.+\*\*$/.test(line.trim())) html += `<h3>${inline(line.trim().slice(2, -2))}</h3>`;
    else html += `<p>${inline(line)}</p>`;
  }
  if (listOpen) html += '</li></ul>';
  return html;
}

function appendMessage(text, type) {
  const node = document.createElement('article');
  node.className = `message ${type}`;
  node.innerHTML = renderMessage(text, type);
  messages.appendChild(node);
  messages.scrollTop = messages.scrollHeight;
}

function render(state) {
  const working = state.status === 'working';
  status.textContent = working ? 'Em missão' : state.status === 'failed' ? 'Interrompido' : 'Disponível';
  button.disabled = working;
  input.disabled = working;
  button.textContent = working ? 'Agentes trabalhando…' : 'Iniciar missão';
  agents.innerHTML = state.agents.length ? state.agents.map(agent => `<article class="agent"><strong>${agent.name}</strong><span>${agent.role}</span><em>${agent.status}</em></article>`).join('') : '<p class="empty">Nenhum agente ativo.</p>';
  events.innerHTML = (state.events.length ? state.events : ['Aguardando uma orientação.']).map(item => `<li>${item}</li>`).join('');
  if (state.result && !shownResults.has(state.id)) {
    appendMessage(state.result, 'assistant');
    shownResults.add(state.id);
  }
}

async function refresh() {
  const response = await fetch('/api/state');
  render(await response.json());
}

async function loadConfig() {
  const response = await fetch('/api/config');
  const config = await response.json();
  ollamaHost.textContent = config.ollama_host;
  ollamaUrl.textContent = config.ollama_url;
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  input.value = '';
  const response = await fetch('/api/missions', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message})});
  if (!response.ok) appendMessage('Não foi possível iniciar a missão.', 'assistant');
  refresh();
});

refresh();
loadConfig();
setInterval(refresh, 1200);
