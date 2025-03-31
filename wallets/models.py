from django.db import models
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
import base64

class Wallet(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed password
    blockchain_network = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        """ Hash password before saving """
        self.password = make_password(self.password)  # Hash the password
        super(Wallet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlockchainWallet(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    encrypted_private_key = models.TextField()

    # Define the encryption key directly (unsafe in production)
    ENCRYPTION_KEY = b'your-secret-encryption-key-here'  # Replace this with your key

    def set_private_key(self, private_key: str):
        """Encrypt the private key before saving it"""
        fernet = Fernet(self.ENCRYPTION_KEY)
        encrypted_key = fernet.encrypt(private_key.encode())
        self.encrypted_private_key = base64.urlsafe_b64encode(encrypted_key).decode('utf-8')
        self.save()

    def get_private_key(self) -> str:
        """Decrypt the private key"""
        fernet = Fernet(self.ENCRYPTION_KEY)
        encrypted_key = base64.urlsafe_b64decode(self.encrypted_private_key.encode('utf-8'))
        decrypted_key = fernet.decrypt(encrypted_key).decode('utf-8')
        return decrypted_key
