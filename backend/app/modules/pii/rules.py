import re

COLUMN_PATTERNS = {
    'PII_RFC': r'(?i).*(rfc|tax_id).*',
    'PII_CURP': r'(?i).*(curp|id_nacional).*',
    'PII_EMAIL': r'(?i).*(email|correo).*',
    'PCI_TARJETA': r'(?i).*(tarjeta|card_number|pan|ccn).*',
    'PCI_CVV': r'(?i).*(cvv|cvc|codigo_seguridad).*',
    'PII_TELEFONO': r'(?i).*(telefono|phone|celular).*',
    'SEC_PASSWORD': r'(?i).*(password|contrase[ñn]a|pwd).*',
    'PII_NOMBRE': r'(?i).*(nombre|name|full_name).*',
    'PII_APELLIDO': r'(?i).*(apellido|lastname|surname).*',
    'PII_DIRECCION': r'(?i).*(direccion|address|domicilio).*',
    'PII_FECHA_NACIMIENTO': r'(?i).*(fecha_nacimiento|birth_date|dob).*',
    'PII_CP': r'(?i).*(codigo_postal|cp|zip).*'
}

CONTENT_PATTERNS = {
    'PII_RFC_DATA': re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-V1-9][A-Z1-9][0-9A]$', re.IGNORECASE),
    'PII_EMAIL_DATA': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
    'PCI_TARJETA_DATA': re.compile(r'^\d{13,19}$'),
    'PII_TELEFONO_DATA': re.compile(r'^\+?\d{10,15}$'),
    'PII_CP_DATA': re.compile(r'^\d{5}$')
}
