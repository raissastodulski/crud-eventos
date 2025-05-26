from datetime import datetime, date, time

class FormatadorData:
    
    FORMATO_DATA_BRASILEIRA = "%d/%m/%Y"
    FORMATO_HORA = "%H:%M"
    FORMATO_DATA_HORA_BRASILEIRA = "%d/%m/%Y %H:%M"
    FORMATO_ISO_DATA = "%Y-%m-%d"
    
    @staticmethod
    def str_para_data(data_str):
        if not data_str or not data_str.strip():
            return None
            
        try:
            return datetime.strptime(data_str.strip(), FormatadorData.FORMATO_DATA_BRASILEIRA).date()
        except ValueError:
            return None
    
    @staticmethod
    def str_para_hora(hora_str):
        if not hora_str or not hora_str.strip():
            return None
            
        try:
            return datetime.strptime(hora_str.strip(), FormatadorData.FORMATO_HORA).time()
        except ValueError:
            return None
    
    @staticmethod
    def data_para_str(data_obj):
        if data_obj is None:
            return ""
            
        if isinstance(data_obj, str):
            temp_data = FormatadorData.str_para_data(data_obj)
            if temp_data:
                return temp_data.strftime(FormatadorData.FORMATO_DATA_BRASILEIRA)
            return data_obj
            
        return data_obj.strftime(FormatadorData.FORMATO_DATA_BRASILEIRA)
    
    @staticmethod
    def hora_para_str(hora_obj):
        if hora_obj is None:
            return ""
            
        if isinstance(hora_obj, str):
            return hora_obj
            
        return hora_obj.strftime(FormatadorData.FORMATO_HORA)
    
    @staticmethod
    def data_hora_para_str(data_hora_obj):
        if data_hora_obj is None:
            return ""
            
        return data_hora_obj.strftime(FormatadorData.FORMATO_DATA_HORA_BRASILEIRA)
    
    @staticmethod
    def iso_para_data(iso_str):
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
        if data_obj is None:
            return None
            
        return data_obj.isoformat()
    
    @staticmethod
    def validar_data_futura(data_obj):
        if data_obj is None:
            return False
            
        return data_obj >= date.today()
    
    @staticmethod
    def validar_data_fim_posterior(data_inicio, data_fim):
        if data_inicio is None or data_fim is None:
            return True
            
        return data_fim >= data_inicio
    
    @staticmethod
    def solicitar_data_usuario(prompt, permitir_vazio=False, validar_futura=False):
        while True:
            data_str = input(f"{prompt} (DD/MM/AAAA): ").strip()
            
            if not data_str and permitir_vazio:
                return None
            
            if not data_str:
                print("⚠️  Data obrigatória. Digite uma data válida.")
                continue
                
            data_obj = FormatadorData.str_para_data(data_str)
            
            if data_obj is None:
                print("⚠️  Data inválida. Use o formato DD/MM/AAAA.")
                continue
                
            if validar_futura and not FormatadorData.validar_data_futura(data_obj):
                print("⚠️  A data não pode estar no passado.")
                continue
                
            return data_obj
    
    @staticmethod
    def solicitar_hora_usuario(prompt, permitir_vazio=False):
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
    def data_hora_inscricao_agora():
        return datetime.now().strftime(FormatadorData.FORMATO_DATA_HORA_BRASILEIRA)
