$(document).ready(function () {
    $('#especificacionesTable').DataTable({
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json"
        }       
    });

    const showError = (modal, message) => {
        $(modal + ' .alert-danger').remove();
        let errorMessage = '';
        
        if (typeof message === 'object') {
            if (message.errors) {
                // Si es un objeto de errores de Django
                const errorList = [];
                for (const [key, value] of Object.entries(message.errors)) {
                    if (Array.isArray(value)) {
                        errorList.push(`${key}: ${value.join(', ')}`);
                    } else {
                        errorList.push(`${key}: ${value}`);
                    }
                }
                errorMessage = errorList.join('<br>');
            } else {
                // Si es un objeto de errores directo
                const errorList = [];
                for (const [key, value] of Object.entries(message)) {
                    if (Array.isArray(value)) {
                        errorList.push(`${key}: ${value.join(', ')}`);
                    } else {
                        errorList.push(`${key}: ${value}`);
                    }
                }
                errorMessage = errorList.join('<br>');
            }
        } else {
            errorMessage = message;
        }
        
        $(modal + ' .modal-body').prepend(`
            <div class="alert alert-danger" id="error-message">${errorMessage}</div>
        `);
    };

    // Función para actualizar el total de formularios y reiniciar los IDs
    function updateFormCount() {
        const totalForms = $('.formset-form').length;
        $('#id_form-TOTAL_FORMS').val(totalForms);
        $('#id_form-INITIAL_FORMS').val(totalForms);
        
        // Reiniciar los IDs de los formularios
        $('.formset-form').each(function(index) {
            $(this).find('input, select').each(function() {
                const name = $(this).attr('name');
                if (name) {
                    $(this).attr('name', name.replace(/-\d+-/, `-${index}-`));
                    $(this).attr('id', `id_${name.replace(/-\d+-/, `-${index}-`)}`);
                }
            });
        });
    }

    // Función para aplicar formateo a un campo
    function aplicarFormateoACampo(campo) {
        $(campo).on('input', function() {
            const posicionCursor = this.selectionStart;
            const textoFormateado = formatearTexto(this.value);
            
            if (this.value !== textoFormateado) {
                this.value = textoFormateado;
                this.setSelectionRange(posicionCursor, posicionCursor);
            }
        });
        
        $(campo).on('blur', function() {
            this.value = formatearTexto(this.value);
        });
        
        // Aplicar formateo al valor inicial
        campo.value = formatearTexto(campo.value);
    }

    // Aplicar formateo a todos los campos existentes cuando se carga la página
    $(document).ready(function() {
        $('input[type="text"]').each(function() {
            aplicarFormateoACampo(this);
        });
    });

    // Función para agregar un nuevo formulario
    function 
    addForm() {
        const formCount = $('.formset-form').length;
        const template = $('.formset-form:first').clone();
        
        // Limpiar los valores del formulario clonado
        template.find('input, select').val('');
        
        // Actualizar los nombres y IDs de los campos
        template.find('input, select').each(function() {
            const name = $(this).attr('name');
            if (name) {
                const newName = name.replace(/-\d+-/, `-${formCount}-`);
                $(this).attr('name', newName);
                $(this).attr('id', `id_${newName}`);
            }
        });
        
        // Agregar el nuevo formulario al contenedor
        $('#formset-container').append(template);
        
        // Aplicar formateo al nuevo campo de texto
        const nuevoCampo = template.find('input[type="text"]')[0];
        if (nuevoCampo) {
            // Aplicar formateo inmediatamente
            $(nuevoCampo).on('input', function() {
                const posicionCursor = this.selectionStart;
                const textoFormateado = formatearTexto(this.value);
                
                if (this.value !== textoFormateado) {
                    this.value = textoFormateado;
                    this.setSelectionRange(posicionCursor, posicionCursor);
                }
            });
            
            $(nuevoCampo).on('blur', function() {
                this.value = formatearTexto(this.value);
            });
            
            // Aplicar formateo al valor inicial
            nuevoCampo.value = formatearTexto(nuevoCampo.value);
        }
        
        updateFormCount();
    }

    // Manejar el envío del formulario de creación con AJAX
    $("#form-add").submit(function (e) {
        e.preventDefault();
        const seccionId = $('#seccion-select').val();
        if (!seccionId) {
            showError('#crearModal', 'Por favor seleccione una sección');
            return;
        }

        const formData = new FormData(this);
        // Asegurarse de que la sección se envíe en cada formulario del formset
        $('.formset-form').each(function(index) {
            formData.set(`form-${index}-seccion`, seccionId);
        });
        
        $.ajax({
            url: "/maq_settings/especificacion/",
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.success) {
                    $("#crearModal").modal('hide');
                    location.reload();
                } else {
                    showError('#crearModal', response);
                }
            },
            error: function (xhr) {
                showError('#crearModal', xhr.responseJSON || "Error al procesar la solicitud.");
            }
        });
    });

    // Limpiar el mensaje de error cuando se abre el modal
    $("#crearModal").on("show.bs.modal", function () {
        $("#form-add")[0].reset();
        $("#error-message").remove();
        // Mantener solo el primer formulario
        $('.formset-form:not(:first)').remove();
        updateFormCount();
    });

    // Agregar nuevo formulario
    $("#add-form").click(function() {
        addForm();
    });

    // Eliminar formulario
    $(document).on('click', '.delete-form', function() {
        if ($('.formset-form').length > 1) {
            $(this).closest('.formset-form').remove();
            updateFormCount();
        }
    });

    // Cuando se haga clic en "Editar", llenar el modal con los datos
    $(".edit-btn").click(function () {
        const seccionId = $(this).data("id");
        
        $.ajax({
            url: `/maq_settings/especificacion/${seccionId}/editar/`,
            method: 'GET',
            success: function(response) {
                const container = $('#edit-formset-container');
                container.empty();
                
                // Agregar el select de sección
                const seccionHtml = `
                    <div class="mb-3">
                        <label class="form-label">Sección</label>
                        <select class="form-control" disabled>
                            <option value="${response.seccion.id}" selected>${response.seccion.nombre}</option>
                        </select>
                    </div>
                `;
                container.append(seccionHtml);
                
                // Agregar el formset management form
                container.append(`
                    <input type="hidden" name="form-TOTAL_FORMS" value="${response.forms.length}" id="id_form-TOTAL_FORMS">
                    <input type="hidden" name="form-INITIAL_FORMS" value="${response.forms.length}" id="id_form-INITIAL_FORMS">
                    <input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS">
                    <input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">
                `);
                
                // Agregar cada formulario
                response.forms.forEach((formData, index) => {
                    const formHtml = `
                        <div class="formset-form mb-3">
                            <div class="row">
                                <div class="col-md-10">
                                    <label class="form-label">Especificación</label>
                                    <input type="hidden" name="form-${index}-id" value="${formData.id}">
                                    <input type="text" name="form-${index}-especificacion" class="form-control" value="${formData.especificacion}">
                                    <input type="hidden" name="form-${index}-seccion" value="${response.seccion.id}">
                                    <input type="hidden" name="form-${index}-DELETE" value="">
                                </div>
                                <div class="col-md-2 d-flex align-items-end">
                                    <button type="button" class="btn btn-outline-danger delete-form">
                                        <i class="fas fa-times"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    container.append(formHtml);
                    
                    // Aplicar formateo al campo de texto recién creado
                    const nuevoCampo = container.find(`input[name="form-${index}-especificacion"]`)[0];
                    if (nuevoCampo) {
                        aplicarFormateoACampo(nuevoCampo);
                    }
                });
            },
            error: function() {
                showError('#editModal', "Error al cargar los datos");
            }
        });
    });

    // Eliminar formulario en el modal de edición
    $(document).on('click', '#editModal .delete-form', function() {
        const form = $(this).closest('.formset-form');
        const especificacionId = form.find('input[name$="-id"]').val();
        
        if (especificacionId) {
            $.ajax({
                url: `/maq_settings/especificacion/${especificacionId}/eliminar/`,
                method: 'POST',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(response) {
                    if (response.success) {
                        form.remove();
                        updateFormCount();
                    } else {
                        showError('#editModal', response.error || 'Error al eliminar la especificación');
                    }
                },
                error: function(xhr) {
                    showError('#editModal', 'Error al eliminar la especificación');
                }
            });
        } else {
            form.remove();
            updateFormCount();
        }
    });

    // Enviar formulario de edición con AJAX
    $("#form-edit").submit(function (e) {
        e.preventDefault();
        const formData = new FormData();
        const seccionId = $('#editModal select[disabled]').val();
        
        // Agregar el token CSRF
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
        
        // Asegurarse de que todos los campos requeridos estén presentes
        let formIndex = 0;
        $('#editModal .formset-form').each(function() {
            const id = $(this).find('input[name$="-id"]').val();
            const especificacion = $(this).find('input[name$="-especificacion"]').val();
            const isDeleted = $(this).is(':hidden');
            
            if (!isDeleted) {
                formData.append(`form-${formIndex}-id`, id);
                formData.append(`form-${formIndex}-especificacion`, especificacion);
                formData.append(`form-${formIndex}-seccion`, seccionId);
                formData.append(`form-${formIndex}-DELETE`, '');
            } else {
                formData.append(`form-${formIndex}-id`, id);
                formData.append(`form-${formIndex}-DELETE`, 'on');
            }
            formIndex++;
        });
        
        // Actualizar el total de formularios y otros campos de gestión
        formData.append('form-TOTAL_FORMS', formIndex);
        formData.append('form-INITIAL_FORMS', formIndex);
        formData.append('form-MIN_NUM_FORMS', '0');
        formData.append('form-MAX_NUM_FORMS', '1000');

        // Imprimir los datos que se enviarán
        console.log('Datos a enviar:');
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }
        
        $.ajax({
            url: `/maq_settings/especificacion/${$('.edit-btn').data('id')}/editar/`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log('Respuesta del servidor:', response);
                if (response.success) {
                    $("#editModal").modal('hide');
                    location.reload();
                } else {
                    showError('#editModal', response);
                }
            },
            error: function (xhr) {
                console.log('Error en la petición:', xhr.responseJSON);
                showError('#editModal', xhr.responseJSON || "Error al procesar la solicitud.");
            }
        });
    });

    // Mostrar ID del registro a eliminar en el modal
    $(".delete-btn").click(function () {
        $("#delete-id").val($(this).data("id"));
    });

    // Confirmar eliminación con AJAX
    $("#confirm-delete").click(function () {
        const especificacionId = $("#delete-id").val();
        
        $.ajax({
            url: `/maq_settings/especificacion/${especificacionId}/eliminar/`,
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