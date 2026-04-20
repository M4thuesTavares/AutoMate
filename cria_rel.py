from weasyprint import HTML

def criar_pdf_rel_manutecao(dados, nome_arquivo="relatorio_automate.pdf"):
    linha_html = ""
    for linha in dados:

        linha_html += f"""
                    <tr>
                        <td>{linha['Codigo']}</td>
                        <td>{linha['Descricao']}</td>
                        <td>{linha['DataUltimaManutecao']}</td>
                        <td>{linha['DataProxManutecao']}</td>
                    </tr>
                        """
    html_template = f"""
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: Arial, sans-serif; color: #333; }}
            h1 {{ color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #f1f5f9; padding: 12px; text-align: left; border-bottom: 2px solid #cbd5e1; }}
            td {{ padding: 12px; border-bottom: 1px solid #e2e8f0; font-size: 11pt; }}
        </style>
    </head>
    <body>
        <h1>AutoMate - Relatório de Manutenções</h1>
        <p>Localidade: São Luís - MA | Data: 18/04/2026</p>
        <table>
            <thead>
                <tr>
                    <th>Código</th>
                    <th>Descrição</th>
                    <th>Última Manut.</th>
                    <th>Próxima Manut.</th>
                </tr>
            </thead>
            <tbody>
                {linha_html}
            </tbody>
        </table>
    </body>
    </html>
    """

    HTML(string=html_template).write_pdf(nome_arquivo)

    return nome_arquivo