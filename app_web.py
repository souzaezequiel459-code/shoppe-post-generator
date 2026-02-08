import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="🛍️ Gerador de Posts Shopee", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .success-box {
        background-color: #90EE90;
        padding: 1rem;
        border-radius: 0.5rem;
        color: black;
        font-weight: bold;
    }
    .copy-btn {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        cursor: pointer;
    }
    .preview-box {
        background-color: #f0f0f0;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007bff;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ Gerador de Posts Shopee")
st.markdown("_Crie posts incríveis para suas promoções na Shopee!_")

# Sidebar com configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Tema/Estilo
    estilo = st.selectbox(
        "Escolha o estilo do post:",
        ["🚨 Urgente", "🌟 Premium", "💎 Luxo", "🎉 Celebração", "⚡ Flash Sale"]
    )
    
    # Tom do post
    ton = st.radio(
        "Tom do post:",
        ["Casual", "Profissional", "Divertido"]
    )

# Divider
st.divider()

# Colunas principais
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Informações do Produto")
    
    produto = st.text_input("Nome do Produto", placeholder="Ex: Fone sem fio Bluetooth")
    preco = st.text_input("Preço", placeholder="Ex: 89,90")
    desconto = st.number_input("Desconto (%)", min_value=0, max_value=100, value=0)
    link = st.text_input("Link de Afiliado", placeholder="https://shopee.com.br/...", key="link")
    
    avaliacao = st.slider("Avaliação do Produto ⭐", 0.0, 5.0, 4.5, step=0.5)
    
    # Detalhes adicionais
    with st.expander("📦 Detalhes Adicionais"):
        estoque = st.text_input("Quantidade em Estoque", placeholder="Ex: Limitado")
        frete = st.toggle("Frete Grátis?", value=True)
        condicao = st.selectbox("Condição", ["Novo", "Seminovo", "Recondicionado"])

# Geração dos templates
def gerar_post(produto_nome, preco_valor, link_af, estilo_selecionado, ton_post, aval, desc, est, frete_gratis, cond):
    """Gera diferentes templates de posts baseado nas preferências"""
    
    if not all([produto_nome, preco_valor, link_af]):
        return None
    
    preco_final = preco_valor
    if desc > 0:
        preco_final = f"~~R$ {preco_valor}~~ → R$ {preco_valor} (-{desc}%)"
    else:
        preco_final = f"R$ {preco_valor}"
    
    avaliacao_stars = "⭐" * int(aval)
    
    # Template base com emojis
    templates = {
        "🚨 Urgente": f"""🚨 ACHADO IMPERDÍVEL! 🚨

📦 {produto_nome}
⭐ Avaliação: {avaliacao_stars}
💰 {preco_final}
📊 Status: {est if est else 'Em Estoque'}
{'🚚 Frete Grátis!' if frete_gratis else '📦 Frete Cobrado'}
🏷️ Condição: {cond}

🛒 Compre aqui: {link_af}

#shopee #achadinhos #oferta #imperdível""",
        
        "🌟 Premium": f"""✨ PRODUTO PREMIUM ✨

🎯 {produto_nome}
⭐ Avaliação: {avaliacao_stars}

💎 Preço Especial: {preco_final}
{'✅ Frete Grátis' if frete_gratis else '📦 Frete Disponível'}
🆕 Condição: {cond}

👉 Clique e aproveite: {link_af}

#shopee #premium #qualidade #exclusivo""",
        
        "💎 Luxo": f"""💎 LUXO E ELEGÂNCIA 💎

{produto_nome}
Avaliação: {avaliacao_stars}

Investimento: {preco_final}
Seleção Premium | {cond}
{'Entrega Grátis' if frete_gratis else 'Entrega Rápida'} 🚀

Descubra: {link_af}

#shopee #luxo #seleção #estilo""",
        
        "🎉 Celebração": f"""🎉 CELEBRE COM A GENTE! 🎉

Apresentamos: {produto_nome}
⭐⭐⭐⭐⭐ Clients Adoram!

🎁 De: ~~R$ {preco_valor}~~ Por: {preco_final}
{est if est else 'Estoque limitado'}
{'🎁 Brinde: Frete Grátis' if frete_gratis else '🚚 Entrega Rápida'}

Quero o meu: {link_af}

#shopee #promoção #celebração #oferta""",
        
        "⚡ Flash Sale": f"""⚡ FLASH SALE ⚡
🔥 SUPER PROMOÇÃO 🔥

{produto_nome}
Nota: {avaliacao_stars}

ANTES: ~~R$ {preco_valor}~~
AGORA: {preco_final} {f'({desc}% OFF)' if desc > 0 else ''}

{'✅ FRETE GRÁTIS' if frete_gratis else 'Entrega Cobrada'} | {cond}
{est if est else '⏰ Aproveita Enquanto Duraaaaa!'}

LINK: {link_af}

#shopee #fleshsale #promoção #desconto""",
    }
    
    # Ajustar tom do post
    post = templates.get(estilo_selecionado, templates["🚨 Urgente"])
    
    if ton_post == "Casual":
        post = post.replace("Apresentamos:", "Olha só que bacana!").replace("Descubra:", "Conferir →")
    elif ton_post == "Divertido":
        post = post.replace("Aproveita", "Vem logo pra não perder! 😂").replace("Clique", "Pula pra cá")
    
    return post

# Gerar post ao lado
with col2:
    st.subheader("👁️ Preview do Post")
    
    # Botões de ação
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        gerar = st.button("✨ Gerar Post", use_container_width=True, type="primary")
    
    with col_btn2:
        limpar = st.button("🔄 Limpar Tudo", use_container_width=True)
    
    with col_btn3:
        salvar = st.button("💾 Salvar", use_container_width=True)
    
    if limpar:
        st.session_state.clear()
        st.rerun()
    
    # Gerar e exibir post
    if gerar or st.session_state.get("post_gerado"):
        post_gerado = gerar_post(
            produto, preco, link, estilo, ton,
            avaliacao, desconto, estoque, frete, condicao
        )
        
        if post_gerado:
            st.session_state.post_gerado = post_gerado
            
            # Contar caracteres
            chars = len(post_gerado)
            st.metric("Caracteres", chars)
            
            # Preview
            st.markdown('<div class="preview-box">' + post_gerado + '</div>', unsafe_allow_html=True)
            
            # Copiar para clipboard
            st.code(post_gerado, language="text")
            
            if st.button("📋 Copiar para Clipboard", use_container_width=True):
                st.write(post_gerado)  # Em um ambiente real, usaríamos pyperclip
                st.success("✅ Copie o texto acima usando Ctrl+C!")
            
            # Salvar no histórico
            if salvar:
                if "historico" not in st.session_state:
                    st.session_state.historico = []
                
                st.session_state.historico.append({
                    "tempo": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "produto": produto,
                    "preco": preco,
                    "post": post_gerado
                })
                st.success("✅ Post salvo no histórico!")
        else:
            st.error("⚠️ Preencha todos os campos obrigatórios!")

# Histórico
st.divider()
st.subheader("📚 Histórico de Posts")

if "historico" in st.session_state and st.session_state.historico:
    for i, item in enumerate(reversed(st.session_state.historico), 1):
        with st.expander(f"Post {i} - {item['produto']} ({item['tempo']})"):
            st.code(item["post"], language="text")
            col_a, col_b = st.columns(2)
            with col_a:
                st.text(f"Preço: {item['preco']}")
            with col_b:
                if st.button(f"🗑️ Deletar Post {i}", key=f"del_{i}"):
                    st.session_state.historico = [x for j, x in enumerate(reversed(st.session_state.historico)) if j != i-1]
                    st.rerun()
else:
    st.info("📝 Nenhum post salvo ainda. Crie seu primeiro post!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p style='color: gray; font-size: 0.9em'>
    🚀 Gerador de Posts Shopee v2.0 | Otimizado para Vendas
    </p>
</div>
""", unsafe_allow_html=True)
