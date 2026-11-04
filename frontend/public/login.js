// Se já estiver logado, pula direto para o sistema
if (getToken()) {
  window.location.href = "pacientes.html";
}

document.getElementById("form-login").addEventListener("submit", async (evento) => {
  evento.preventDefault(); // impede o formulário de recarregar a página

  const login = document.getElementById("login").value;
  const senha = document.getElementById("senha").value;

  try {
    await fazerLogin(login, senha); // guarda o token no localStorage
    window.location.href = "pacientes.html";
  } catch (erro) {
    mostrarMensagem(erro.message, true);
  }
});