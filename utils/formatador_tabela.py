class FormatadorTabela:
    @staticmethod
    def criar_tabela(dados, cabecalhos, larguras=None):
        if not dados:
            return "Nenhum dado para exibir."
        
        if larguras is None:
            larguras = [max(len(str(cabecalho)), max(len(str(linha[i]) if i < len(linha) else '') for linha in dados)) 
                       for i, cabecalho in enumerate(cabecalhos)]
        
        larguras = [max(largura, 8) for largura in larguras]
        
        separador = "+" + "+".join("-" * (largura + 2) for largura in larguras) + "+"
        
        cabecalho_formatado = "|" + "|".join(f" {cabecalho:<{larguras[i]}} " 
                                           for i, cabecalho in enumerate(cabecalhos)) + "|"
        
        linhas_formatadas = []
        for linha in dados:
            linha_formatada = "|" + "|".join(f" {str(linha[i]) if i < len(linha) else '':<{larguras[i]}} " 
                                           for i in range(len(cabecalhos))) + "|"
            linhas_formatadas.append(linha_formatada)
        
        tabela = [separador, cabecalho_formatado, separador] + linhas_formatadas + [separador]
        
        return "\n".join(tabela)
    
    @staticmethod
    def criar_tabela_detalhes(titulo, dados_dict):
        if not dados_dict:
            return "Nenhum detalhe para exibir."
        
        largura_chave = max(len(str(chave)) for chave in dados_dict.keys())
        largura_valor = max(len(str(valor)) for valor in dados_dict.values())
        largura_chave = max(largura_chave, 15)
        largura_valor = max(largura_valor, 20)
        
        separador = "+" + "-" * (largura_chave + 2) + "+" + "-" * (largura_valor + 2) + "+"
        titulo_completo = f"| {titulo:^{largura_chave + largura_valor + 3}} |"
        separador_titulo = "+" + "-" * (largura_chave + largura_valor + 5) + "+"
        
        linhas = []
        for chave, valor in dados_dict.items():
            linha = f"| {str(chave):<{largura_chave}} | {str(valor):<{largura_valor}} |"
            linhas.append(linha)
        
        tabela = [
            separador_titulo,
            titulo_completo,
            separador,
        ] + linhas + [separador]
        
        return "\n".join(tabela)
    
    @staticmethod
    def truncar_texto(texto, max_length):
        if len(str(texto)) > max_length:
            return str(texto)[:max_length-3] + "..."
        return str(texto)
