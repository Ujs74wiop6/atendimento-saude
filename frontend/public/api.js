// ============================================================
// api.js: tudo que conversa com a API (back-end) e utilitários
// compartilhados pelas telas.
// ============================================================

// Endereço da API. O navegador chama direto o back-end (porta 5000).
const API_URL = "http://localhost:5000";

// ---------- Token (JWT) no localStorage ----------

function getToken() {
  return localStorage.getItem("token");
}

// Se não houver token, manda para a tela de login
function exigirLogin() {
  if (!getToken()) {
    window.location.href = "index.html";
  }
}

// Apaga o token e volta para o login
function sair() {
  localStorage.removeItem("token");
  localStorage.removeItem("usuario");
  window.location.href = "index.html";
}

// ---------- Função base: todas as chamadas passam por aqui ----------

async function requisicao(metodo, caminho, corpo) {
  const opcoes = {
    method: metodo,
    headers: { "Content-Type": "application/json" },
  };

  // Se existe token, envia no cabeçalho Authorization
  const token = getToken();
  if (token) {
    opcoes.headers["Authorization"] = "Bearer " + token;
  }
  if (corpo) {
    opcoes.body = JSON.stringify(corpo);
  }

  let resposta;
  try {
    resposta = await fetch(API_URL + caminho, opcoes);
  } catch (e) {
    throw new Error("Não foi possível conectar à API. Verifique se o servidor está no ar.");
  }

  const dados = await resposta.json();

  // Token vencido ou inválido: volta para o login
  if (resposta.status === 401 && caminho !== "/login") {
    sair();
    throw new Error("Sessão expirada. Faça login novamente.");
  }
  // Qualquer outro erro: repassa a mensagem que a API mandou
  if (!resposta.ok) {
    throw new Error(dados.erro || "Erro inesperado");
  }
  return dados;
}

// ---------- Login ----------

async function fazerLogin(login, senha) {
  const dados = await requisicao("POST", "/login", { login, senha });
  localStorage.setItem("token", dados.token);
  localStorage.setItem("usuario", JSON.stringify(dados.usuario));
  return dados;
}

// ---------- Pacientes (5 funções) ----------

function getAllPacientes() {
  return requisicao("GET", "/pacientes");
}
function getPacienteByID(id) {
  return requisicao("GET", "/pacientes/" + id);
}
function insertPaciente(dados) {
  return requisicao("POST", "/pacientes", dados);
}
function updatePaciente(id, dados) {
  return requisicao("PUT", "/pacientes/" + id, dados);
}
function deletePaciente(id) {
  return requisicao("DELETE", "/pacientes/" + id);
}

// ---------- Consultas (5 funções) ----------

function getAllConsultas() {
  return requisicao("GET", "/consultas");
}
function getConsultaByID(id) {
  return requisicao("GET", "/consultas/" + id);
}
function insertConsulta(dados) {
  return requisicao("POST", "/consultas", dados);
}
function updateConsulta(id, dados) {
  return requisicao("PUT", "/consultas/" + id, dados);
}
function deleteConsulta(id) {
  return requisicao("DELETE", "/consultas/" + id);
}

// ---------- Utilitários das telas ----------

// Mostra uma mensagem de sucesso (verde) ou erro (vermelha) no <p id="mensagem">
function mostrarMensagem(texto, ehErro = false) {
  const el = document.getElementById("mensagem");
  el.textContent = texto;
  el.className = "mensagem " + (ehErro ? "erro" : "sucesso");
}

// Evita que um texto digitado vire HTML (proteção contra XSS)
function escapar(texto) {
  const div = document.createElement("div");
  div.textContent = texto;
  return div.innerHTML;
}

// "2026-11-10" -> "10/11/2026" (sem usar Date, para não mudar o dia por fuso horário)
function formatarData(iso) {
  const [ano, mes, dia] = iso.split("-");
  return `${dia}/${mes}/${ano}`;
}

// 150 -> "R$ 150,00"
function formatarMoeda(valor) {
  return Number(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}
