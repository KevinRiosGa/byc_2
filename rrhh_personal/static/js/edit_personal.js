document.addEventListener("DOMContentLoaded", function () {
    const btnEditar = document.getElementById("btn_editar");
    const btnGuardar = document.getElementById("btn_guardar");
    const campos = document.querySelectorAll("#personal-form input, #personal-form select");
    const form = document.getElementById("personal-form");

    // Hacer que los campos sean editables al hacer clic en "Editar"
    btnEditar.addEventListener("click", function () {
        campos.forEach(function (campo) {
            campo.removeAttribute("disabled"); // Eliminar "disabled"
        });

        btnGuardar.style.display = "inline-block"; // Mostrar botón "Guardar"
        btnEditar.style.display = "none"; // Ocultar botón "Editar"
    });

    // Deshabilitar los campos si el formulario es válido
    if (form.dataset.isValid === "true") {
        campos.forEach(function (campo) {
            campo.setAttribute("disabled", "disabled"); // Deshabilitar campos
        });

        btnGuardar.style.display = "none"; // Ocultar botón "Guardar"
        btnEditar.style.display = "inline-block"; // Mostrar botón "Editar"
    }
});