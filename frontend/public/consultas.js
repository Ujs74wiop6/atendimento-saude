exigirLogin(); // sem token, volta para o login

const form = document.getElementById("form-consulta");
const lista = document.getElementById("lista");
const selectPaciente = document.getElementById("paciente_id");

// ---------- Preenche o <select> com os pacientes (reaproveita getAllPacientes) ----------
async function carregarPacientes() {
  try {
    const pacientes = await getAllPacientes();
    selectPaciente.innerHTML = '<option value="">Selecione...</option>' +
      pacientes.map((p) => `<option value="${p.id}">${escapar(p.nome)}</option>`).join("");
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

// ---------- Listar (GetAll) ----------
async function carregarLista() {
  try {
    const consultas = await getAllConsultas();

    if (consultas.length === 0) {
      lista.innerHTML = '<tr><td colspan="6">Nenhuma consulta cadastrada.</td></tr>';
      return;
    }

    lista.innerHTML = consultas.map((c) => `
      <tr>
        <td>${c.id}</td>
        <td>${escapar(c.paciente_nome)}</td>
        <td>${formatarData(c.data_consulta)}</td>
        <td>${escapar(c.descricao)}</td>
        <td>${formatarMoeda(c.valor)}</td>
        <td class="acoes">
          <button onclick="editar(${c.id})">Editar</button>
          <button class="perigo" onclick="remover(${c.id})">Remover</button>
        </td>
      </tr>`).join("");
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

// ---------- Salvar: Insert (sem id) ou Update (com id) ----------
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const id = document.getElementById("id").value;
  const dados = {
    paciente_id: Number(selectPaciente.value),
    data_consulta: document.getElementById("data_consulta").value,
    descricao: document.getElementById("descricao").value,
    valor: document.getElementById("valor").value,
  };

  try {
    if (id) {
      await updateConsulta(id, dados);
      mostrarMensagem("Consulta atualizada com sucesso.");
    } else {
      await insertConsulta(dados);
      mostrarMensagem("Consulta cadastrada com sucesso.");
    }
    limparFormulario();
    carregarLista();
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
});

// ---------- Editar: busca a consulta (GetByID) e preenche o formulário ----------
async function editar(id) {
  try {
    const c = await getConsultaByID(id);
    document.getElementById("id").value = c.id;
    selectPaciente.value = c.paciente_id;
    document.getElementById("data_consulta").value = c.data_consulta;
    document.getElementById("descricao").value = c.descricao;
    document.getElementById("valor").value = c.valor;
    document.getElementById("titulo-form").textContent = "Editando consulta #" + c.id;
    window.scrollTo(0, 0);
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

// ---------- Remover (Delete) ----------
async function remover(id) {
  if (!confirm("Deseja realmente remover esta consulta?")) return;

  try {
    await deleteConsulta(id);
    mostrarMensagem("Consulta removida com sucesso.");
    carregarLista();
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

function limparFormulario() {
  form.reset();
  document.getElementById("id").value = "";
  document.getElementById("titulo-form").textContent = "Nova consulta";
}

document.getElementById("cancelar").addEventListener("click", limparFormulario);

// Ao abrir a tela: carrega os pacientes do select e a lista de consultas
carregarPacientes();
carregarLista();
