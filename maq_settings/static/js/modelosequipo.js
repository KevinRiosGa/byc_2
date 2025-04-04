$(document).ready(function() {
    // Inicializar DataTable
    const table = $('#modelosTable').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/2.2.2/i18n/es-CL.json"
        }
    });

    // Función para mostrar errores en el modal
    function showErrors(errors) {
        const errorDiv = $('#errorMessages');
        const errorList = errorDiv.find('ul');
        errorList.empty();
        
        // Convertir el objeto de errores en un array de mensajes
        const errorMessages = [];
        for (const field in errors) {
            if (Array.isArray(errors[field])) {
                errors[field].forEach(error => errorMessages.push(error));
            } else {
                errorMessages.push(errors[field]);
            }
        }

        // Agregar cada mensaje de error a la lista
        errorMessages.forEach(error => {
            errorList.append(`<li>${error}</li>`);
        });

        // Mostrar el div de errores
        errorDiv.removeClass('d-none');
    }

    // Función para limpiar errores
    function clearErrors() {
        $('#errorMessages').addClass('d-none').find('ul').empty();
    }

    // Función para cargar las marcas según el tipo seleccionado
    function loadMarcas(tipoId, marcaId = null) {
        var marcaSelect = $('#marca_equipo_select');
        marcaSelect.empty().append('<option value="">Seleccione una marca</option>');
        
        if (tipoId) {
            $.get(`/maq_settings/obtener_marcas_por_tipo/${tipoId}/`, function(data) {
                data.marcas.forEach(function(marca) {
                    marcaSelect.append(`<option value="${marca.id}">${marca.nombre}</option>`);
                });
                if (marcaId) {
                    marcaSelect.val(marcaId);
                }
            });
        }
    }

    // Evento change para el select de tipo de equipo
    $('#tipo_equipo_select').change(function() {
        loadMarcas($(this).val());
    });

    // Guardar modelo
    $('#guardarModelo').click(function() {
        clearErrors();
        var formData = new FormData($('#modeloForm')[0]);
        var modeloId = $('#modelo_id').val();
        var url = modeloId ? `/maq_settings/modeloequipo/${modeloId}/editar/` : '/maq_settings/modeloequipo/';

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    location.reload();
                }
            },
            error: function(xhr) {
                if (xhr.status === 400) {
                    showErrors(xhr.responseJSON.errors);
                }
            }
        });
    });

    // Manejar el evento show.bs.modal
    $('#modeloModal').on('show.bs.modal', function(e) {
        clearErrors();
        var button = $(e.relatedTarget);
        
        if (button.hasClass('edit-btn')) {
            // Modo edición
            var id = button.data('id');
            var tipo = button.data('tipo');
            var marca = button.data('marca');
            var modelo = button.data('modelo');

            console.log("Datos para edición:", {id, tipo, marca, modelo});

            // Establecer los valores en el formulario
            $('#modelo_id').val(id);
            $('#modeloeq').val(modelo);
            $('#tipo_equipo_select').val(tipo);
            
            // Cargar las marcas y establecer la marca seleccionada
            loadMarcas(tipo, marca);
            
            // Cambiar el título del modal
            $('#modeloModalLabel').text('Editar Modelo');
        } else {
            // Modo creación
            $('#modeloForm')[0].reset();
            $('#modelo_id').val('');
            $('#modeloModalLabel').text('Crear Modelo');
            $('#marca_equipo_select').empty().append('<option value="">Seleccione una marca</option>');
        }
    });

    // Variable para almacenar el ID del modelo a eliminar
    let modeloIdToDelete = null;

    // Abrir modal de confirmación de eliminación
    $(document).on('click', '.eliminar-modelo', function() {
        modeloIdToDelete = $(this).data('id');
        var confirmarModal = new bootstrap.Modal(document.getElementById('confirmarEliminarModal'));
        confirmarModal.show();
    });

    // Confirmar eliminación
    $('#confirmarEliminar').click(function() {
        if (modeloIdToDelete) {
            $.ajax({
                url: `/maq_settings/modeloequipo/${modeloIdToDelete}/eliminar/`,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    if (response.success) {
                        // Cerrar el modal de confirmación
                        var confirmarModal = bootstrap.Modal.getInstance(document.getElementById('confirmarEliminarModal'));
                        confirmarModal.hide();
                        // Recargar la página
                        location.reload();
                    }
                }
            });
        }
    });
});