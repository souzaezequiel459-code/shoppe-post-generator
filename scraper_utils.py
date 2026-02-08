import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re

def extrair_dados_produto(url):
    """
    Extrai título, descrição, preço e imagem do link do produto.
    Funciona com Open Graph tags (og:title, og:description, og:image)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrair dados com Open Graph tags
        def extrair_og(propriedade):
            tag = soup.find('meta', property=f'og:{propriedade}')
            return tag['content'] if tag else None
        
        titulo = extrair_og('title')
        descricao = extrair_og('description')
        imagem_url = extrair_og('image')
        preco_texto = extrair_og('price:amount')
        
        # Se não encontrou, tenta title e description normais
        if not titulo:
            title_tag = soup.find('title')
            titulo = title_tag.text.strip() if title_tag else "Produto sem título"
        
        if not descricao:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            descricao = meta_desc['content'] if meta_desc else "Sem descrição"
        
        # Tenta extrair preço de padrões comuns
        preco = None
        if preco_texto:
            preco = preco_texto
        else:
            # Busca por padrões de preço na página
            padroes_preco = [
                r'R\$\s*[\d.,]+',
                r'Price:\s*[\d.,]+',
                r'Preço:\s*[\d.,]+',
            ]
            for padrao in padroes_preco:
                match = re.search(padrao, response.text, re.IGNORECASE)
                if match:
                    preco = match.group(0)
                    break
        
        # Baixar imagem se encontrada
        imagem_local = None
        if imagem_url:
            try:
                imagem_local = baixar_imagem(imagem_url)
            except:
                pass
        
        return {
            'titulo': titulo[:60] if titulo else "",
            'descricao': descricao[:200] if descricao else "",
            'preco': preco if preco else "",
            'imagem_url': imagem_url,
            'imagem_local': imagem_local,
            'sucesso': True
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'titulo': "",
            'descricao': f"Erro ao acessar URL: {str(e)}",
            'preco': "",
            'imagem_url': None,
            'imagem_local': None,
            'sucesso': False,
            'erro': str(e)
        }
    except Exception as e:
        return {
            'titulo': "",
            'descricao': f"Erro ao processar: {str(e)}",
            'preco': "",
            'imagem_url': None,
            'imagem_local': None,
            'sucesso': False,
            'erro': str(e)
        }

def baixar_imagem(url_imagem):
    """Baixa imagem e salva localmente"""
    import os
    import time
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url_imagem, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Determinar extensão
        ext = '.jpg'
        if 'image/png' in response.headers.get('content-type', ''):
            ext = '.png'
        elif 'image/webp' in response.headers.get('content-type', ''):
            ext = '.webp'
        
        os.makedirs('uploads', exist_ok=True)
        filename = f"scraped_{int(time.time())}{ext}"
        caminho = os.path.join('uploads', filename)
        
        with open(caminho, 'wb') as f:
            f.write(response.content)
        
        return caminho
    except:
        return None
