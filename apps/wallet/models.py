import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Wallet(models.Model):
    wallet_id = models.CharField(max_length=32, primary_key=True, editable=False)
    user = models.OneToOneField(User, blank=False, null=False, on_delete=models.RESTRICT)
    balance = models.BigIntegerField(default=0)
    available_balance = models.BigIntegerField(default=0, editable=False)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('onhold', 'On Hold'), ('inactive', 'In Active')), default='active')

    def __str__(self):
        return self.wallet_id

    def save(self, *args, **kwargs):
        if not self.wallet_id:
            self.wallet_id = self.user.phone_number
        super().save(*args, **kwargs)


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4().hex, editable=False, unique=True)
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet_sender')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='wallet_receiver')
    # from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sender')
    # to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_receiver')
    transaction_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_by')
    amount = models.BigIntegerField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        bunus_amount = 0
        from_wallet = self.from_wallet
        to_wallet = self.to_wallet
        if from_wallet.user.is_player and to_wallet.user.is_agent:
            bunus_amount = self.amount * 0.2
        from_wallet.balance -= self.amount
        to_wallet.balance += self.amount + bunus_amount
        from_wallet.save()
        to_wallet.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.transaction_id)
    
