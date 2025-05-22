# Este arquivo permite que Python reconheça o diretório como um pacote

# Primeiro importamos as classes básicas
from .evento import Evento
from .crud_bd_eventos import CrudBDEventos

# Depois importamos as classes que dependem das anteriores
from .crud_eventos import CrudEventos
from .menu_eventos import MenuEventos