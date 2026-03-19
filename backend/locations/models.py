from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        
    def __str__(self):
        return f"{self.code} - {self.name}"

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        
    def __str__(self):
        return f"{self.code} - {self.name}"


class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="wards")
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['code']  # or ['code']
        
    def __str__(self):
        return f"{self.code} - {self.name}"
    

class Street(models.Model):
    ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name="streets"
    )
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("ward", "name")

    class Meta:
        # verbose_name = "Marital Status"
        # verbose_name_plural = "Marital Statuses"
        ordering = ['id']  # or ['code']
        
    def __str__(self):
        return f"{self.id} - {self.name}"