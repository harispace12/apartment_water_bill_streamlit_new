import re

VALID_FLAT_REGEX = r'^(G[1-9]|[1-5]0[1-9])$'

def normalize_flat(flat):
    return flat.strip().upper()

def is_valid_flat(flat, master_flats):
    flat = normalize_flat(flat)
    if not re.match(VALID_FLAT_REGEX, flat):
        return False, "Invalid flat format"
    if flat not in master_flats:
        return False, "Flat not in society master list"
    return True, ""

def validate_reading(prev, curr):
    if curr < prev:
        return False, "Current reading cannot be less than previous"
    if curr - prev > 10000:
        return True, "Unusually high usage – please verify"
    return True, ""
