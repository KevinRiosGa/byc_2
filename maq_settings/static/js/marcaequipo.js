$(document).ready(function () {
    // Inicializa DataTables
    $('#marcasTable').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/2.2.2/i18n/es-CL.json"
        }
    });

    // Manejo del envío del formulario de creación de marcas
    $('#form-add').on('submit', function (e) {
        e.preventDefault(); // Evitar recarga de página
        var formData = $(this).serialize();

        $.ajax({
            url: "", // Usa la URL actual
            method: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    $('#crearModal').modal('hide'); // Cerrar modal si la marca se crea correctamente
                    location.reload(); // Recargar la página para actualizar la tabla
                }
            },
            error: function (xhr) {
                let errors = xhr.responseJSON.errors;
                let errorMessage = errors.marcaeq ? errors.marcaeq[0] : "Error al crear la marca, ya existe."

                $("#crearModal .modal-body").prepend(`
                    <div class="alert alert-danger" id="error-message">${errorMessage}</div>
                `);
            }
        });
    });

    // Cuando se haga clic en el botón de editar
    $(document).on('click', '.edit-btn', function () {
        var marcaId = $(this).data('id');  
        console.log("Marca ID:", marcaId);

        if (!marcaId) {
            console.error("No se ha encontrado el ID de la marca.");
            return;
        }

        var url = '/maq_settings/obtener_datos_marca/' + marcaId + '/';

        $.ajax({
            url: url,
            method: 'GET',
            success: function (data) {
                console.log('Datos recibidos:', data);

                // Rellenar el campo de la marca
                $('#editModal input[name="marcaeq"]').val(data.marca);

                // Limpiar errores previos
                $('#editModal .error-message').remove();

                // Limpiar las opciones del select de checkboxes antes de agregar las nuevas
                $('#editModal input[name="tipoeq"]').prop('checked', false);

                // Marcar las casillas correspondientes
                $.each(data.tipos_equipos_ids, function (index, tipoId) {
                    $('#editModal input[name="tipoeq"][value="' + tipoId + '"]').prop('checked', true);
                });

                // Establecer el ID de la marca en el formulario para la actualización
                $('#form-edit').data('id', marcaId);

                // Mostrar el modal
                $('#editModal').modal('show');
            },
            error: function (error) {
                console.log("Error:", error);
            }
        });
    });

    // Manejo del envío del formulario de edición
    $('#form-edit').on('submit', function (e) {
        e.preventDefault();

        var marcaId = $(this).data('id'); 
        console.log("Marca ID en submit:", marcaId);

        if (!marcaId) {
            console.error("El ID de la marca no está disponible.");
            return;
        }

        var formData = $(this).serialize();

        $.ajax({
            url: '/maq_settings/editar_marca/' + marcaId + '/',
            method: 'POST',
            data: formData,
            success: function (data) {
                console.log('Marca actualizada:', data);
                $('#editModal').modal('hide'); 
                location.reload();
            },
            error: function (xhr) {
                var errors = xhr.responseJSON.errors;
                var errorMessage = '';

                if (errors.marcaeq) {
                    errorMessage = errors.marcaeq[0]; // Captura el mensaje de error
                }

                // Mostrar el mensaje de error en rojo dentro del modal
                $('#form-edit .error-message').remove(); // Elimina mensajes previos
                $('#form-edit input[name="marcaeq"]').after(
                    '<div class="text-danger error-message">' + errorMessage + '</div>'
                );
            }
        });
    });
});
