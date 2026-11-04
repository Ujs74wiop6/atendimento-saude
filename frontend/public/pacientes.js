exigirLogin(); // sem token, volta para o login

const form = document.getElementById("form-paciente");
const lista = document.getElementById("lista");

// Listar (GetAll)
async function carregarLista() {
  try {
    const pacientes = await getAllPacientes();

    if (pacientes.length === 0) {
      lista.innerHTML = '<tr><td colspan="6">Nenhum paciente cadastrado.</td></tr>';
      return;
    }

    lista.innerHTML = pacientes.map((p) => `
      <tr>
        <td>${p.id}</td>
        <td>${escapar(p.nome)}</td>
        <td>${escapar(p.cpf)}</td>
        <td>${formatarData(p.data_nascimento)}</td>
        <td>${escapar(p.telefone || "")}</td>
        <td class="acoes">
          <button onclick="editar(${p.id})">Editar</button>
          <button class="perigo" onclick="remover(${p.id})">Remover</button>
        </td>
      </tr>`).join("");
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

// Salvar: Insert (sem id) ou Update (com id)
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const id = document.getElementById("id").value;
  const dados = {
    nome: document.getElementById("nome").value,
    cpf: document.getElementById("cpf").value,
    data_nascimento: document.getElementById("data_nascimento").value,
    telefone: document.getElementById("telefone").value || null,
  };

  try {
    if (id) {
      await updatePaciente(id, dados);
      mostrarMensagem("Paciente atualizado com sucesso.");
    } else {
      await insertPaciente(dados);
      mostrarMensagem("Paciente cadastrado com sucesso.");
    }
    limparFormulario();
    carregarLista();
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
});

// Editar: busca o paciente (GetByID) e preenche o formulário
async function editar(id) {
  try {
    const p = await getPacienteByID(id);
    document.getElementById("id").value = p.id;
    document.getElementById("nome").value = p.nome;
    document.getElementById("cpf").value = p.cpf;
    document.getElementById("data_nascimento").value = p.data_nascimento;
    document.getElementById("telefone").value = p.telefone || "";
    document.getElementById("titulo-form").textContent = "Editando paciente #" + p.id;
    window.scrollTo(0, 0);
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

// Remover (Delete)
async function remover(id) {
  if (!confirm("Deseja realmente remover este paciente?")) return;

  try {
    await deletePaciente(id);
    mostrarMensagem("Paciente removido com sucesso.");
    carregarLista();
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
}

function limparFormulario() {
  form.reset();
  document.getElementById("id").value = "";
  document.getElementById("titulo-form").textContent = "Novo paciente";
}

document.getElementById("cancelar").addEventListener("click", limparFormulario);

carregarLista(); // ao abrir a tela
