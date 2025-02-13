import sys, os
import mimetypes
import logging
import datetime

# MIME type ayarları
mimetypes.add_type('text/html', '.py')
mimetypes.add_type('text/html', '.wsgi')

# Log dizinini kontrol et ve oluştur
log_dir = '/home/dig317xiocom/logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging ayarları
logging.basicConfig(
    filename='/home/dig317xiocom/logs/passenger.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Uygulama başlatılıyor...")

try:
    # Uygulama dizinini logla
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info(f"Uygulama dizini: {current_dir}")
    
    sys.path.insert(0, current_dir)
    
    # Virtual environment yolu - Python 3.6 için
    INTERP = os.path.join(current_dir, 'venv', 'bin', 'python')
    if sys.executable != INTERP:
        os.execl(INTERP, INTERP, *sys.argv)

    from app import application
    
except Exception as e:
    logging.error(f"Başlatma hatası: {str(e)}", exc_info=True)
    raise 