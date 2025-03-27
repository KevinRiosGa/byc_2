$(document).ready(function () {
    $('#marcasTable').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/2.2.2/i18n/es-CL.json"
        }
    });
    // Manejar el envío del formulario de creación con AJAX
    $("#form-add").submit(function (e) {
        e.preventDefault();
        let formData = $(this).serialize();

        $.ajax({
            url: "",
            type: "POST",
            data: formData,
            success: function (response) {
                if (response.success) {
                    $("#crearModal").modal("hide");
                    location.reload();
                }
            },
            error: function (xhr) {
                let errors = xhr.responseJSON.errors;
                let errorMessage = errors.prefixeq ? errors.prefixeq[0] : "Error al crear la marca.";
                $("#crearModal .modal-body").prepend(`
                    <div class="alert alert-danger" id="error-message">${errorMessage}</div>
                `);
            }
        });
    });

    // Limpiar el mensaje de error cuando se abre el modal
    $("#crearModal").on("show.bs.modal", function () {
        $("#form-add")[0].reset();
        $("#error-message").remove();
    });
    //    // Cuando se haga clic en "Editar", llenar el modal con los datos
    //     $(".edit-btn").click(function () {
    //         $("#edit-id").val($(this).data("id"));
    //         $("#edit-prefixeq").val($(this).data("prefix"));
    //         $("#edit-tipoeq").val($(this).data("tipo"));
    //     });
    
    //     // Deshabilitar edición del prefijo
    //     $("#edit-prefixeq").prop("disabled", true);
    
    //     // Enviar formulario de edición con AJAX
    //     $("#form-edit").submit(function (e) {
    //         e.preventDefault();
    //         let id = $("#edit-id").val();
    //         let tipoeq = $("#edit-tipoeq").val();
    //         let csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        
    //         $.ajax({
    //             url: `${id}/editar/`,
    //             type: "POST",
    //             data: {
    //                 csrfmiddlewaretoken: csrf_token,
    //                 tipoeq: tipoeq
    //             },
    //             success: function (response) {
    //                 $("#edit-message").text("¡Registro actualizado correctamente!").css({
    //                     "display": "block",
    //                     "background-color": "green",
    //                     "color": "white",
    //                     "text-align": "center"
    //                 });
                
    //                 setTimeout(function() {
    //                     location.reload();
    //                 }, 850);
    //             },
    //             error: function () {
    //                 $("#edit-message").text("Error al actualizar.").css({
    //                     "display": "block",
    //                     "background-color": "red",
    //                     "color": "white",
    //                     "text-align": "center"
    //                 });
    //             }
    //         });
    //     });
    
    //     // Mostrar ID del registro a eliminar en el modal
    //     $(".delete-btn").click(function () {
    //         $("#delete-id").val($(this).data("id"));
    //     });
    
    //     // Confirmar eliminación con AJAX
    //     $("#confirm-delete").click(function () {
    //         let id = $("#delete-id").val();
    //         let csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        
    //         $.ajax({
    //             url: `${id}/eliminar/`,
    //             type: "POST",
    //             data: { csrfmiddlewaretoken: csrf_token },
    //             success: function (response) {
    //                 $("#deleteModal").modal("hide");
    //                 location.reload();
    //             },
    //             error: function () {
    //                 alert("Error al eliminar el registro.");
    //             }
    //         });
    //     });
    });     