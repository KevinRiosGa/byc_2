$(document).ready(function () {
    const table = $('#marcasTable').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/2.2.2/i18n/es-CL.json"
        }
    });

    const showError = (modal, message) => {
        $(modal + ' .alert-danger').remove();
        $(modal + ' .modal-body').prepend(`
            <div class="alert alert-danger" id="error-message">${message}</div>
        `);
    };

    const handleFormSubmit = (form, url, modal) => {
        const formData = new FormData(form[0]);
        
        $.ajax({
            url: url,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $(modal).modal('hide');
                    location.reload();
                } else {
                    showError(modal, response.errors ? Object.values(response.errors).join(', ') : "Error al procesar la solicitud.");
                }
            },
            error: function (xhr) {
                const errorMessage = xhr.responseJSON?.errors ? Object.values(xhr.responseJSON.errors).join(', ') : "Error al procesar la solicitud.";
                showError(modal, errorMessage);
            }
        });
    };

    $('#form-add').on('submit', function (e) {
        e.preventDefault();
        handleFormSubmit($(this), "", '#crearModal');
    });

    $(document).on('click', '.edit-btn', function () {
        const marcaId = $(this).data('id');
        if (!marcaId) {
            console.error("No se ha encontrado el ID de la marca.");
            return;
        }

        $.ajax({
            url: '/maq_settings/obtener_datos_marca/' + marcaId + '/',
            method: 'GET',
            success: function (data) {
                $('#editModal input[name="marcaeq"]').val(data.marca);
                $('#editModal .alert-danger').remove();
                $('#editModal input[name="tipoeq"]').prop('checked', false);
                
                data.tipos_equipos_ids.forEach(tipoId => {
                    $('#editModal input[name="tipoeq"][value="' + tipoId + '"]').prop('checked', true);
                });

                $('#form-edit').data('id', marcaId);
                $('#editModal').modal('show');
            },
            error: function (error) {
                console.error("Error:", error);
            }
        });
    });

    $('#form-edit').on('submit', function (e) {
        e.preventDefault();
        const marcaId = $(this).data('id');
        if (!marcaId) {
            console.error("El ID de la marca no está disponible.");
        }
        handleFormSubmit($(this), '/maq_settings/editar_marca/' + marcaId + '/', '#editModal');
    });

    // Mostrar ID del registro a eliminar en el modal
    $(".delete-btn").click(function () {
        $("#delete-id").val($(this).data("id"));
    });

    // Confirmar eliminación con AJAX
    $("#confirm-delete").click(function () {
        let id = $("#delete-id").val();
        let csrf_token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/maq_settings/eliminar_marca/' + id + '/',
            type: "POST",
            data: { csrfmiddlewaretoken: csrf_token },
            success: function (response) {
                $("#deleteModal").modal("hide");
                location.reload();
            },
            error: function () {
                alert("Error al eliminar la marca.");
            }
        });
    });
});
