
# Valida RUT
def validar_rut(rut):
    rut = str(rut)
  
    # Verifica si el RUT contiene solo dígitos
    if not rut.isdigit():
        return False
    
    suma = 0
    multiplicador = 2
    
    # Calcula la suma ponderada para los dígitos del RUT
    for digito in reversed(rut):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2  # Se corrige la actualización de multiplicador

    # Calcula el dígito verificador
    dv_calculado = 11 - (suma % 11)
    
    if dv_calculado == 11:
        return "0"
    elif dv_calculado == 10:
        return "K"
    else:
        return str(dv_calculado)
    