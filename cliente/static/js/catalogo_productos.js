const toggleModal = () => document.body.classList.toggle("open"); /*Abrir modal*/



//contador
document.addEventListener("DOMContentLoaded", function() {
    const botonAumentar = document.querySelector('.botonAumentar');
    const botonRestar = document.querySelector('.botonRestar');
    const contadorNumero = document.querySelector('.contadorNumero');
    
    const enlace = document.getElementById('enlace').addEventListener('click',function(event){
        event.preventDefault();
    })
  
    botonAumentar.addEventListener('click', function() {
      let valor = parseInt(contadorNumero.textContent);
      contadorNumero.textContent = valor + 1;
    });
  
    botonRestar.addEventListener('click', function() {
      let valor = parseInt(contadorNumero.textContent);
      if (valor > 1) {
        contadorNumero.textContent = valor - 1;
      }
    });
  });

  let cantidad = 1;

  function aumentarCantidad() {
    cantidad++;
    document.getElementById('contador').textContent = cantidad;
  }

  function disminuirCantidad() {
    if (cantidad > 1) {
      cantidad--;
      document.getElementById('contador').textContent = cantidad;
    }
  }

  
 // Variable para almacenar la cantidad de productos en el carrito
let cantidadProductosCarrito = 0;

// Función para mostrar u ocultar el modal
const toggleModal2 = () => {
    document.body.classList.toggle("open");

    // Actualizar el contador del carrito al abrir el modal
    updateCarritoCounter();
};



// Función para actualizar el contador del carrito en la interfaz
const updateCarritoCounter = () => {
    const contadorCarrito = document.querySelector(".contador-carrito");

    // Actualizar el contenido del contador con la cantidad de productos en el carrito
    contadorCarrito.textContent = cantidadProductosCarrito.toString();
};
function mostrarAlerta() {
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = Swal.stopTimer;
          toast.onmouseleave = Swal.resumeTimer;
        }
      });
      Toast.fire({
        icon: "success",
        color: "",
        background: "#fff url(/images/trees.png)",
        title: "Producto agregado al carrito"
      });
  }

  function cerrarAlerta() {
    Swal.close(); 
  }

function agregarAlCarrito() {
    cantidadProductosCarrito++;
    updateCarritoCounter();
    mostrarAlerta();
  }
  
  
