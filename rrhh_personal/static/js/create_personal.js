
// Función para calcular el dígito verificador
function calcularDV(rut) {
    let suma = 0;
    let multiplicador = 2;
    for (let i = rut.length - 1; i >= 0; i--) {
        suma += parseInt(rut.charAt(i)) * multiplicador;
        multiplicador = multiplicador + 1 <= 7 ? multiplicador + 1 : 2;
    }
    const dv = 11 - (suma % 11);
    if (dv === 11) return '0';
    if (dv === 10) return 'K';
    return dv.toString();
}
// Captura el evento de cambio en el campo 'rut' y actualiza 'dvrut'
document.addEventListener('DOMContentLoaded', function() {
    const rutField = document.getElementById('id_rut');  // ID del campo RUT
    const dvField = document.getElementById('id_dvrut');  // ID del campo DV
    rutField.addEventListener('input', function() {
        const rut = rutField.value.replace(/\D/g, '');  // Elimina cualquier caracter no numérico
        if (rut.length >= 7) {  // Asegura que el RUT tenga al menos 7 dígitos
            dvField.value = calcularDV(rut);  // Asigna el dígito verificador
        } else {
            dvField.value = '';  // Borra el valor de 'dvrut' si el RUT es inválido
        }
    });
});

