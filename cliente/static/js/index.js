function showLoadingAnimation() {
  var loadingOverlay = document.querySelector('.loading-overlay');
  var content = document.querySelector('.content');
  var body = document.body;

  loadingOverlay.style.display = 'flex';
  content.style.display = 'none';
  body.style.overflow = 'hidden';
  body.style.backgroundColor = 'white'; // Establecer el color de fondo
}

function hideLoadingAnimation() {
  var loadingOverlay = document.querySelector('.loading-overlay');
  var content = document.querySelector('.content');
  var body = document.body;

  loadingOverlay.style.display = 'none';
  content.style.display = 'block';
  body.style.overflow = 'auto';
  body.style.backgroundColor = ''; // Restablecer el color de fondo a su valor predeterminado
}

window.addEventListener('load', function() {
  showLoadingAnimation();

  setTimeout(function() {
      hideLoadingAnimation();
  }, 1000); // Ocultar la animación después de 3000 milisegundos (3 segundos)
});
