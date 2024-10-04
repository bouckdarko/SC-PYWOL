from wakeonlan import send_magic_packet

def wake_device(mac_address):
    """Envoie un paquet Wake On Lan pour réveiller un périphérique."""
    send_magic_packet(mac_address)
    print(f"Magic packet sent to {mac_address}")
