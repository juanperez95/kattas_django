const btnSiguientePersonal = document.querySelector('#personal-section button');
const btnAnteriorContacto = document.querySelector('#contacto-section button:first-of-type');
const btnSiguienteContacto = document.querySelector('#contacto-section button:last-of-type');
const btnAnteriorContrasena = document.querySelector('#contrasena-section button:first-of-type');

const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

btnSiguientePersonal.addEventListener('click', function() {
    mostrarSiguiente('personal-section', 'contacto-section');
});

btnAnteriorContacto.addEventListener('click', function() {
    mostrarAnterior('contacto-section', 'personal-section');
});

btnSiguienteContacto.addEventListener('click', function() {
    mostrarSiguiente('contacto-section', 'contrasena-section');
});

btnAnteriorContrasena.addEventListener('click', function() {
    mostrarAnterior('contrasena-section', 'contacto-section');
});

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

function mostrarSiguiente(actual, siguiente) {
    document.getElementById(actual).hidden = true;
    document.getElementById(siguiente).hidden = false;
}

function mostrarAnterior(actual, anterior) {
    document.getElementById(actual).hidden = true;
    document.getElementById(anterior).hidden = false;
}
