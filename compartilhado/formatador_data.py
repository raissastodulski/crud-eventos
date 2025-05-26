from datetime import datetime, date, time

class FormatadorData:
    """
    Classe utilitária para formatação padronizada de datas no sistema CRUD Eventos.
    
    Padronização:
    - Interface do usuário: SEMPRE dd/mm/yyyy 
    - Banco de dados: SEMPRE datetime/date/time (formato ISO)
    - Validações: Centralizadas e automáticas
    """
    
    # Constantes de formato
    FORMATO_DATA_BRASILEIRA = "%d/%m/%Y"
    FORMATO_HORA = "%H:%M"
    FORMATO_DATA_HORA_BRASILEIRA = "%d/%m/%Y %H:%M"
    FORMATO_ISO_DATA = "%Y-%m-%d"
    
    @staticmethod
    def str_para_data(data_str):
        """
        Converte string dd/mm/yyyy para objeto date.
        
        Args:
            data_str (str): Data no formato dd/mm/yyyy
            
        Returns:
            date: Objeto date ou None se inválido
        """
        if not data_str or not data_str.strip():
            return None
            
        try:
            return datetime.strptime(data_str.strip(), FormatadorData.FORMATO_DATA_BRASILEIRA).date()
        except ValueError:
            return None
    
    @staticmethod
    def str_para_hora(hora_str):
        """
        Converte string hh:mm para objeto time.
        
        Args:
            hora_str (str): Hora no formato hh:mm
            
        Returns:
            time: Objeto time ou None se inválido
        """
        if not hora_str or not hora_str.strip():
            return None
            
        try:
            return datetime.strptime(hora_str.strip(), FormatadorData.FORMATO_HORA).time()
        except ValueError:
            return None
    
    @staticmethod
    def data_para_str(data_obj):
        """
        Converte objeto date para string dd/mm/yyyy.
        
        Args:
            data_obj (date): Objeto date
            
        Returns:
            str: Data no formato dd/mm/yyyy ou string vazia se None
        """
        if data_obj is None:
            return ""
            
        if isinstance(data_obj, str):
            # Se já é string, verificar se precisa converter
            temp_data = FormatadorData.str_para_data(data_obj)
            if temp_data:
                return temp_data.strftime(FormatadorData.FORMATO_DATA_BRASILEIRA)
            return data_obj
            
        return data_obj.strftime(FormatadorData.FORMATO_DATA_BRASILEIRA)
    
    @staticmethod
    def hora_para_str(hora_obj):
        """
        Converte objeto time para string hh:mm.
        
        Args:
            hora_obj (time): Objeto time
            
        Returns:
            str: Hora no formato hh:mm ou string vazia se None
        """
        if hora_obj is None:
            return ""
            
        if isinstance(hora_obj, str):
            return hora_obj
            
        return hora_obj.strftime(FormatadorData.FORMATO_HORA)
    
    @staticmethod
    def data_hora_para_str(data_hora_obj):
        """
        Converte objeto datetime para string dd/mm/yyyy hh:mm.
        
        Args:
            data_hora_obj (datetime): Objeto datetime
            
        Returns:
            str: Data e hora no formato dd/mm/yyyy hh:mm
        """
        if data_hora_obj is None:
            return ""
            
        return data_hora_obj.strftime(FormatadorData.FORMATO_DATA_HORA_BRASILEIRA)
    
    @staticmethod
    def iso_para_data(iso_str):
        """
        Converte string ISO (yyyy-mm-dd) para objeto date.
        
        Args:
            iso_str (str): Data no formato ISO yyyy-mm-dd
            
        Returns:
            date: Objeto date ou None se inválido
        """
        if not iso_str or not iso_str.strip():
            return None
            
        try:
            return datetime.fromisoformat(iso_str.strip()).date()
        except (ValueError, TypeError):
            try:
                return datetime.strptime(iso_str.strip(), FormatadorData.FORMATO_ISO_DATA).date()
            except (ValueError, TypeError):
                return None
    
    @staticmethod
    def data_para_iso(data_obj):
        """
        Converte objeto date para string ISO (yyyy-mm-dd).
        
        Args:
            data_obj (date): Objeto date
            
        Returns:
            str: Data no formato ISO yyyy-mm-dd ou None
        """
        if data_obj is None:
            return None
            
        return data_obj.isoformat()
    
    @staticmethod
    def validar_data_futura(data_obj):
        """
        Valida se a data é futura (não permite datas no passado).
        
        Args:
            data_obj (date): Objeto date para validar
            
        Returns:
            bool: True se data é futura ou hoje, False caso contrário
        """
        if data_obj is None:
            return False
            
        return data_obj >= date.today()
    
    @staticmethod
    def validar_data_fim_posterior(data_inicio, data_fim):
        """
        Valida se data fim é posterior ou igual à data início.
        
        Args:
            data_inicio (date): Data de início
            data_fim (date): Data de fim
            
        Returns:
            bool: True se data fim >= data início
        """
        if data_inicio is None or data_fim is None:
            return True
            
        return data_fim >= data_inicio
    
    @staticmethod
    def solicitar_data_usuario(prompt, permitir_vazio=False, validar_futura=False):
        """
        Solicita data do usuário com validação automática.
        
        Args:
            prompt (str): Texto a exibir para o usuário
            permitir_vazio (bool): Se permite entrada vazia
            validar_futura (bool): Se deve validar data futura
            
        Returns:
            date: Objeto date válido ou None se vazio permitido
        """
        while True:
            data_str = input(f"{prompt} (dd/mm/yyyy): ").strip()
            
            if not data_str and permitir_vazio:
                return None
            
            if not data_str:
                print("⚠️  Data obrigatória. Digite uma data válida.")
                continue
                
            data_obj = FormatadorData.str_para_data(data_str)
            
            if data_obj is None:
                print("⚠️  Data inválida. Use o formato dd/mm/yyyy.")
                continue
                
            if validar_futura and not FormatadorData.validar_data_futura(data_obj):
                print("⚠️  A data não pode estar no passado.")
                continue
                
            return data_obj
    
    @staticmethod
    def solicitar_hora_usuario(prompt, permitir_vazio=False):
        """
        Solicita hora do usuário com validação automática.
        
        Args:
            prompt (str): Texto a exibir para o usuário
            permitir_vazio (bool): Se permite entrada vazia
            
        Returns:
            time: Objeto time válido ou None se vazio permitido
        """
        while True:
            hora_str = input(f"{prompt} (hh:mm): ").strip()
            
            if not hora_str and permitir_vazio:
                return None
                
            if not hora_str:
                print("⚠️  Hora obrigatória. Digite uma hora válida.")
                continue
                
            hora_obj = FormatadorData.str_para_hora(hora_str)
            
            if hora_obj is None:
                print("⚠️  Hora inválida. Use o formato hh:mm.")
                continue
                
            return hora_obj
    
    @staticmethod
    def data_cadastro_hoje():
        """
        Retorna a data atual formatada para cadastros.
        
        Returns:
            str: Data atual no formato dd/mm/yyyy
        """
        return date.today().strftime(FormatadorData.FORMATO_DATA_BRASILEIRA)
    
    @staticmethod
    def data_hora_inscricao_agora():
        """
        Retorna a data/hora atual formatada para inscrições.
        
        Returns:
            str: Data/hora atual no formato dd/mm/yyyy hh:mm
        """
        return datetime.now().strftime(FormatadorData.FORMATO_DATA_HORA_BRASILEIRA)
