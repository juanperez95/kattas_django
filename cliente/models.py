from django.db import models
from django.utils import timezone

class Perfil(models.Model):
    class Meta:
        db_table = "perfil"
        
    nombre_perfil = models.CharField(max_length=20,null=False)
    
class Habilitado(models.Model):
    class Meta:
        db_table = "habilitado"
        
    nombre_habilitado = models.CharField(max_length=20,null=False)
    
class Cargo(models.Model):
    class Meta:
        db_table = "cargo"
        
    nombre_cargo = models.CharField(max_length=20,null=False)

# Create your models here.
class Usuario(models.Model):
    class Meta:
        db_table = "usuarios"
        
    documento = models.BigIntegerField(null=False,primary_key=True)
    habilitado = models.ForeignKey(Habilitado,on_delete=models.CASCADE, blank=True, null=True)
    perfil = models.ForeignKey(Perfil,on_delete=models.CASCADE, blank=True, null=True)
    cargo = models.ForeignKey(Cargo,on_delete=models.CASCADE, blank=True, null=True)
    password = models.TextField(null=False)
    nombre = models.CharField(max_length=30,null=False)
    apellidos = models.CharField(max_length=30,null=False)
    email = models.EmailField(null=False)
    fecha_registro = models.DateField(null=False,default=timezone.now)
    fecha_nacimiento = models.DateField(null=False)
    genero = models.CharField(max_length=30,null=False)
    telefono = models.CharField(max_length=10,null=False)
    direccion = models.CharField(max_length=50,null=False)
    foto_perfil = models.ImageField(upload_to="perfiles", null=True, default="perfiles/imagen_usuario.jpg")

# Insumos ------------------------------------------------------------

class Categoria(models.Model):
    class Meta:
        db_table = "categoria"
        
    nombre_categoria = models.CharField(max_length=20,null=True)
    
class Estado(models.Model):
    class Meta:
        db_table = "estados"
    tipo_estado = models.CharField(max_length=20)

class Insumo(models.Model):
    class Meta:
        db_table = "insumos"
        
    fk_categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    fk_estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    nombre_insumo = models.CharField(max_length=30)    
    cantidad_existente = models.BigIntegerField(null=False)
    cantidad_minimo = models.IntegerField(null=False)
    
class Producto(models.Model):
    class Meta:
        db_table = "producto"
        
    fk_estado = models.ForeignKey(Estado,on_delete=models.CASCADE)
    
    nombre_producto = models.CharField(max_length=40, null=False)
    descripcion = models.TextField()
    tamaño = models.CharField(max_length=40, null=False) 
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    foto_p = models.ImageField(upload_to="imagenes_productos",null=True)
    
class Producto_Insumo(models.Model):
    class Meta:
        db_table = "productos_insumos"

    insumos = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    productos = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    
    
class Entrada_Insumo(models.Model):
    class Meta:
        db_table= "entradaInsumo"
        
    fk_insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad_entrada= models.BigIntegerField(null = False)
    fecha_entrada= models.DateTimeField(null=False,default=timezone.now )
    fecha_vencimiento=models.DateTimeField(null=False)
    estado_vencido=models.CharField(max_length=30 , null=False)
    cantidad_inicial=models.BigIntegerField(null = True)

    

#--------------------------Pedido y Ventas----------------------------------------
    
class Estado_Pedido(models.Model):
    class Meta:
        db_table = "estados_pedido"
    tipo_estado = models.CharField(max_length=20)



class Pedido(models.Model):
    class Meta:
            db_table= "pedido"
            ordering = ['-id'] 

    fk_documento=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=10, decimal_places=2, null= False)
    fecha_pedido=models.DateTimeField(auto_now=True)
    
    fk_estado=models.ForeignKey(Estado_Pedido, on_delete=models.CASCADE)
    
    
class Pedido_Producto(models.Model):
    class Meta:
            db_table= "pedido_producto"

    fk_pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fk_producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto=models.IntegerField()
    precio_producto=models.DecimalField(max_digits=15, decimal_places=2)


class Venta(models.Model):
    class Meta:
            db_table= "venta"

    fk_pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    
    