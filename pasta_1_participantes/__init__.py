# Este arquivo permite que Python reconheça o diretório como um pacote

# Primeiro importamos as classes básicas
from .participante import Participante
from .crud_bd_participantes import CrudBDParticipantes

# Depois importamos as classes que dependem das anteriores
from .crud_participantes import CrudParticipantes
from .menu_participantes import MenuParticipantes