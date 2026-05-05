import re

COLUMN_PATTERNS = {
    'PII_RFC': r'(?i).*(rfc|tax_id).*',
    'PII_CURP': r'(?i).*(curp|id_nacional).*',
    'PII_EMAIL': r'(?i).*(email|correo).*',
    'PCI_TARJETA': r'(?i).*(tarjeta|card_number|pan|ccn).*',
    'PCI_CVV': r'(?i).*(cvv|cvc|codigo_seguridad).*',
    'PII_TELEFONO': r'(?i).*(telefono|phone|celular).*',
    'SEC_PASSWORD': r'(?i).*(password|contrase[ñn]a|pwd).*'
}

CONTENT_PATTERNS = {
    'PII_RFC_DATA': re.compile(r'^[A-ZÑ&]{3,4}\d{6}[A-V1-9][A-Z1-9][0-9A]$', re.IGNORECASE),
    'PII_EMAIL_DATA': re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$'),
    'PCI_TARJETA_DATA': re.compile(r'^\d{13,19}$')
}