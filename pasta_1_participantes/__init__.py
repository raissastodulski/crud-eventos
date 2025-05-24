# Este arquivo permite que Python reconheça o diretório como um pacote

# Primeiro importamos as classes básicas
from .participantes import Participante
from .crud_bd_participantes import CrudBDParticipantes

# Depois importamos as classes que dependem das anteriores
from .participantes import CrudParticipantes
from .menu_participantes import MenuParticipantes