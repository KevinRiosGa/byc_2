$(document).ready(function () {
    $('#seccionesTable').DataTable({
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

    // Manejar el envío del formulario de creación con AJAX
    $("#form-add").submit(function (e) {
        e.preventDefault();
        handleFormSubmit($(this), "/maq_settings/seccionespecificacion/", '#crearModal');
    });

    // Limpiar el mensaje de error cuando se abre el modal
    $("#crearModal").on("show.bs.modal", function () {
        $("#form-add")[0].reset();
        $("#error-message").remove();
    });

    // Cuando se haga clic en "Editar", llenar el modal con los datos
    $(".edit-btn").click(function () {
        const seccionId = $(this).data("id");
        const seccion = $(this).closest("tr").find("td:eq(1)").text();
        
        $("#form-edit input[name='seccion']").val(seccion);
        $("#form-edit").data("id", seccionId);
    });

    // Enviar formulario de edición con AJAX
    $("#form-edit").submit(function (e) {
        e.preventDefault();
        const seccionId = $(this).data("id");
        handleFormSubmit($(this), `/maq_settings/seccionespecificacion/${seccionId}/editar/`, '#editModal');
    });

    // Mostrar ID del registro a eliminar en el modal
    $(".delete-btn").click(function () {
        $("#delete-id").val($(this).data("id"));
    });

    // Confirmar eliminación con AJAX
    $("#confirm-delete").click(function () {
        const seccionId = $("#delete-id").val();
        
        $.ajax({
            url: `/maq_settings/seccionespecificacion/${seccionId}/eliminar/`,
            method: 'POST',
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (response) {
                if (response.success) {
                    $("#deleteModal").modal("hide");
                    location.reload();
                } else {
                    showError('#deleteModal', "Error al eliminar el registro.");
                }
            },
            error: function () {
                showError('#deleteModal', "Error al eliminar el registro.");
            }
        });
    });
});     