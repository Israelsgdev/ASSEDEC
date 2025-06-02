document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

    // Simulação de usuários (em um sistema real, isso viria de um banco de dados)
    const users = [
        { email: 'membro@adcacule.com', password: 'senha123', name: 'João Silva' },
        { email: 'lider@adcacule.com', password: 'senha456', name: 'Maria Souza' }
    ];

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;
        
        // Verificar credenciais
        const user = users.find(u => u.email === email && u.password === password);
        
        if (user) {
            // Salvar sessão (simplificado - em produção usar métodos seguros)
            sessionStorage.setItem('loggedIn', 'true');
            sessionStorage.setItem('userName', user.name);
            
            if (remember) {
                localStorage.setItem('rememberEmail', email);
            } else {
                localStorage.removeItem('rememberEmail');
            }
            
            // Redirecionar para área de membros
            window.location.href = 'membros/dashboard.html';
        } else {
            loginError.classList.remove('d-none');
        }
    });
    
    // Preencher e-mail se "lembrar" estava ativado
    const rememberedEmail = localStorage.getItem('rememberEmail');
    if (rememberedEmail) {
        document.getElementById('email').value = rememberedEmail;
        document.getElementById('remember').checked = true;
    }
});