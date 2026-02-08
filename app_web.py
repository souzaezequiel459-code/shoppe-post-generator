import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="🛒 Gerador de Posts Multiplatforma", layout="wide")

st.title("🛒 Gerador de Posts Multiplatforma")
st.markdown("_Crie posts automáticos para Shopee, Mercado Livre, OLX, Trocafone e mais!_")

# Sidebar com configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Selecionar plataforma
    plataforma = st.selectbox(
        "Escolha a plataforma:",
        ["🛍️ Shopee", "🏪 Mercado Livre", "📱 OLX", "🔄 Trocafone", "📦 Genérico"]
    )
    
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

st.divider()

# Colunas principais
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Informações do Produto")
    
    produto = st.text_input("Nome do Produto", placeholder="Ex: Fone sem fio Bluetooth")
    preco = st.text_input("Preço", placeholder="Ex: 89,90")
    desconto = st.number_input("Desconto (%)", min_value=0, max_value=100, value=0)
    link = st.text_input("Link do Produto", placeholder="https://exemplo.com.br/...", key="link")
    
    # Upload de imagem
    uploaded = st.file_uploader("Imagem do produto", type=["png", "jpg", "jpeg"], key="uploaded")
    if uploaded:
        import os, time
        os.makedirs("uploads", exist_ok=True)
        filename = f"{int(time.time())}_{uploaded.name}"
        path = os.path.join("uploads", filename)
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.session_state["uploaded_path"] = path
        st.image(path, use_column_width=True)
    else:
        # manter caminho entre reruns
        _ = st.session_state.get("uploaded_path")
    avaliacao = st.slider("Avaliação do Produto ⭐", 0.0, 5.0, 4.5, step=0.5)
    
    # Detalhes adicionais
    with st.expander("📦 Detalhes Adicionais"):
        estoque = st.text_input("Quantidade em Estoque", placeholder="Ex: Limitado")
        frete = st.toggle("Frete Grátis?", value=True)
        condicao = st.selectbox("Condição", ["Novo", "Seminovo", "Recondicionado"])

def gerar_post(produto_nome, preco_valor, link_af, plataforma_selecionada, estilo_selecionado, ton_post, aval, desc, est, frete_gratis, cond, imagem_path=None):
    """Gera posts específicos para cada plataforma"""
    
    if not all([produto_nome, preco_valor, link_af]):
        return None
    
    preco_final = preco_valor
    if desc > 0:
        preco_final = f"~~R$ {preco_valor}~~ → R$ {preco_valor} (-{desc}%)"
    else:
        preco_final = f"R$ {preco_valor}"
    
    avaliacao_stars = "⭐" * int(aval)
    
    # Templates por PLATAFORMA
    if plataforma_selecionada == "🛍️ Shopee":
        templates = {
            "🚨 Urgente": f"""🚨 ACHADO IMPERDÍVEL NA SHOPEE! 🚨

📦 {produto_nome}
⭐ Avaliação: {avaliacao_stars}
💰 {preco_final}
📊 Status: {est if est else 'Em Estoque'}
{'🚚 Frete Grátis!' if frete_gratis else '📦 Frete Cobrado'}
🏷️ Condição: {cond}

🛒 Compre aqui: {link_af}

#shopee #achadinhos #oferta #imperdível #promoção""",
            
            "🌟 Premium": f"""✨ PRODUTO PREMIUM NA SHOPEE ✨

🎯 {produto_nome}
⭐ Avaliação: {avaliacao_stars}

💎 Preço Especial: {preco_final}
{'✅ Frete Grátis' if frete_gratis else '📦 Frete Disponível'}
🆕 Condição: {cond}

👉 Clique e aproveite: {link_af}

#shopee #premium #qualidade #exclusivo #seleção""",
            
            "💎 Luxo": f"""💎 LUXO E ELEGÂNCIA NA SHOPEE 💎

{produto_nome}
Avaliação: {avaliacao_stars}

Investimento: {preco_final}
Seleção Premium | {cond}
{'Entrega Grátis' if frete_gratis else 'Entrega Rápida'} 🚀

Descubra: {link_af}

#shopee #luxo #seleção #estilo #shopeeluisinho""",
            
            "🎉 Celebração": f"""🎉 CELEBRE COM A SHOPEE! 🎉

Apresentamos: {produto_nome}
⭐ Clientes Adoram!

🎁 De: ~~R$ {preco_valor}~~ Por: {preco_final}
{est if est else 'Estoque limitado'}
{'🎁 Brinde: Frete Grátis' if frete_gratis else '🚚 Entrega Rápida'}

Quero o meu: {link_af}

#shopee #promoção #celebração #oferta #imperdível""",
            
            "⚡ Flash Sale": f"""⚡ FLASH SALE NA SHOPEE ⚡
🔥 SUPER PROMOÇÃO 🔥

{produto_nome}
Nota: {avaliacao_stars}

ANTES: ~~R$ {preco_valor}~~
AGORA: {preco_final} {f'({desc}% OFF)' if desc > 0 else ''}

{'✅ FRETE GRÁTIS' if frete_gratis else 'Entrega Cobrada'} | {cond}
{est if est else '⏰ Aproveita Enquanto Duraaaaa!'}

LINK: {link_af}

#shopee #fleshsale #promoção #desconto #urgente"""
        }
    
    elif plataforma_selecionada == "🏪 Mercado Livre":
        templates = {
            "🚨 Urgente": f"""🚨 OPORTUNIDADE NO MERCADO LIVRE! 🚨

📦 {produto_nome}
⭐ Vendedor: ⭐⭐⭐⭐⭐
💰 {preco_final}
📊 {est if est else 'Em Estoque'}
{'📦 Frete Grátis Por ML!' if frete_gratis else '📦 Frete Cobrado'}

👉 Acesse: {link_af}

#mercadolivre #oferta #promoção #confiança #achadinhos""",
            
            "🌟 Premium": f"""✨ PRODUTO DESTAQUE - MERCADO LIVRE ✨

{produto_nome}
⭐ Avaliação: ⭐⭐⭐⭐⭐

💎 Oferta: {preco_final}
✅ Vendedor Verificado
{'Frete Grátis' if frete_gratis else 'Frete Rápido'}

Confira: {link_af}

#mercadolivre #premium #confiável #melhor_preço""",
            
            "💎 Luxo": f"""💎 PRODUTO DE QUALIDADE - MERCADO LIVRE 💎

{produto_nome}
Classificação: ⭐⭐⭐⭐⭐

Preço: {preco_final}
Vendedor Certificado ✅
{'Entrega Sem Custo' if frete_gratis else 'Entrega Rápida'}

Detalhes: {link_af}

#mercadolivre #qualidade #seguro #avaliado""",
            
            "🎉 Celebração": f"""🎉 QUEIMA DE ESTOQUE - MERCADO LIVRE! 🎉

Produto: {produto_nome}
Nota: ⭐ Clientela Satisfeita!

Ofertão: ~~R$ {preco_valor}~~ → {preco_final}
{est if est else 'Stock Limitado!'}
{'🎯 Envio Sem Taxa' if frete_gratis else 'Envio Rápido'}

Link: {link_af}

#mercadolivre #oferta #promoção #qualidade""",
            
            "⚡ Flash Sale": f"""⚡ DESCONTO RELÂMPAGO - MERCADO LIVRE ⚡
🔥 LIQUIDAÇÃO JÁ! 🔥

{produto_nome}
⭐ Avaliação Excelente

ANTES: ~~R$ {preco_valor}~~
AGORA: {preco_final} {f'({desc}% ABATIDO)' if desc > 0 else ''}

{'✅ FRETE 0' if frete_gratis else 'Frete Variável'}
Vendedor Top!

CLIQUE: {link_af}

#mercadolivre #fleshsale #desconto #promoção"""
        }
    
    elif plataforma_selecionada == "📱 OLX":
        templates = {
            "🚨 Urgente": f"""🚨 APROVEITA - OLX 🚨

📦 {produto_nome}
⭐ {avaliacao_stars}
💰 {preco_final}
{est if est else 'Em Estoque'}
{'🚚 Pode Entregar' if frete_gratis else 'Retirada no Local'}

Contato: {link_af}

#olx #venda #promoção #oportunidade""",
            
            "🌟 Premium": f"""✨ PRODUTO DE QUALIDADE - OLX ✨

{produto_nome}
⭐ {avaliacao_stars}

Preço: {preco_final}
Condição: {cond}
{'Entrega Disponível' if frete_gratis else 'Retirada no Local'}

Saiba Mais: {link_af}

#olx #venda #confiança #qualidade""",
            
            "💎 Luxo": f"""💎 PRODUTO SELECIONADO - OLX 💎

{produto_nome}
Nota: {avaliacao_stars}

Investimento: {preco_final}
Estado: {cond}
{'Entrega Segura' if frete_gratis else 'Retirada Possível'}

Detalhes: {link_af}

#olx #selecionado #qualidade #confiável""",
            
            "🎉 Celebração": f"""🎉 Super PROMOÇÃO NA OLX! 🎉

{produto_nome}
⭐ Ótimo Estado!

De: ~~R$ {preco_valor}~~ Por: {preco_final}
{est if est else 'Stock Limitado'}
{'Entrega Inclusa' if frete_gratis else 'Retirada Local'}

Contacte: {link_af}

#olx #promoção #oferta #oportunidade""",
            
            "⚡ Flash Sale": f"""⚡ OFERTA RELÂMPAGO NA OLX ⚡
🔥 URGENTE! 🔥

{produto_nome}
Nota: {avaliacao_stars}

APENAS: {preco_final} {f'(Desconto de {desc}%)' if desc > 0 else ''}
Condição: {cond}
{'Entrega Rápida' if frete_gratis else 'Retirada'}

CONTACTO: {link_af}

#olx #oferta #desconto #urgente"""
        }
    
    elif plataforma_selecionada == "🔄 Trocafone":
        templates = {
            "🚨 Urgente": f"""🚨 APARELHO IMPRESCINDÍVEL NA TROCAFONE! 🚨

📱 {produto_nome}
⭐ {avaliacao_stars}
💰 {preco_final}
{'♻️ Trocafone Garante' if frete_gratis else '📦 Frete Cobrado'}

Aproveita: {link_af}

#trocafone #celular #oferta #promoção""",
            
            "🌟 Premium": f"""✨ TELEFONE DE QUALIDADE - TROCAFONE ✨

{produto_nome}
⭐ {avaliacao_stars}

Preço: {preco_final}
♻️ Produto Verificado
Entrega Rápida

Saiba Mais: {link_af}

#trocafone #qualidade #confiável #celular""",
            
            "💎 Luxo": f"""💎 CELULAR PREMIUM - TROCAFONE 💎

{produto_nome}
Nota: {avaliacao_stars}

Investimento: {preco_final}
Estado: {cond}
Garantia Trocafone ✅

Detalhes: {link_af}

#trocafone #premium #celular #garantia""",
            
            "🎉 Celebração": f"""🎉 OFERTA IMPERDÍVEL NA TROCAFONE! 🎉

{produto_nome}
⭐ Testado e Aprovado!

De: ~~R$ {preco_valor}~~ Por: {preco_final}
Pronta Entrega!
Trocafone Autoriza ✅

Pegue o Seu: {link_af}

#trocafone #oferta #celular #promoção""",
            
            "⚡ Flash Sale": f"""⚡ SUPER PROMOÇÃO NA TROCAFONE ⚡
🔥 CELULAR COM DESCONTO! 🔥

{produto_nome}
Avaliação: {avaliacao_stars}

OFERTA: {preco_final} {f'({desc}% OFF)' if desc > 0 else ''}
♻️ Garantia Trocafone
Entrega Rápida!

RESERVE JÁ: {link_af}

#trocafone #fleshsale #celular #desconto"""
        }
    
    else:  # Genérico
        templates = {
            "🚨 Urgente": f"""🚨 ACHADO IMPERDÍVEL! 🚨

📦 {produto_nome}
⭐ {avaliacao_stars}
💰 {preco_final}
{'🚚 Entrega Rápida' if frete_gratis else '📦 Frete Cobrado'}

👉 Compre: {link_af}

#produto #oferta #promoção #imperdível""",
            
            "🌟 Premium": f"""✨ PRODUTO DE QUALIDADE ✨

{produto_nome}
⭐ {avaliacao_stars}

Preço: {preco_final}
{'✅ Entrega Grátis' if frete_gratis else '📦 Frete Disponível'}

Saiba Mais: {link_af}

#qualidade #premium #confiável""",
            
            "💎 Luxo": f"""💎 LUXO E ELEGÂNCIA 💎

{produto_nome}
Nota: {avaliacao_stars}

Investimento: {preco_final}
{'Entrega Grátis' if frete_gratis else 'Entrega Rápida'}

Descubra: {link_af}

#luxo #seleção #qualidade""",
            
            "🎉 Celebração": f"""🎉 CELEBRE COM A GENTE! 🎉

{produto_nome}
⭐ Clientes Adoram!

De: ~~R$ {preco_valor}~~ Por: {preco_final}
{'Brinde: Entrega Grátis' if frete_gratis else 'Entrega Rápida'}

Quero: {link_af}

#promoção #celebração #oferta""",
            
            "⚡ Flash Sale": f"""⚡ FLASH SALE ⚡
🔥 SUPER PROMOÇÃO 🔥

{produto_nome}
Nota: {avaliacao_stars}

AGORA: {preco_final} {f'({desc}% OFF)' if desc > 0 else ''}
{'FRETE GRÁTIS' if frete_gratis else 'Frete Cobrado'}

LINK: {link_af}

#fleshsale #promoção #desconto"""
        }
    
    post = templates.get(estilo_selecionado, templates["🚨 Urgente"])
    
    if ton_post == "Casual":
        post = post.replace("Aproveita", "Bora lá").replace("Compre", "Pega o seu").replace("Saiba Mais", "Vem ver")
    elif ton_post == "Divertido":
        post = post.replace("Aproveita", "Corre logo! 😂").replace("Compre", "Quer? Clica aí! 🎉").replace("Apresentamos", "Olha só que bacana!")
    
    return post

with col2:
    st.subheader("👁️ Preview do Post")
    
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
    
    if gerar or st.session_state.get("post_gerado"):
        post_gerado = gerar_post(
            produto, preco, link, plataforma, estilo, ton,
            avaliacao, desconto, estoque, frete, condicao
        )
        
        if post_gerado:
            st.session_state.post_gerado = post_gerado
            
            chars = len(post_gerado)
            st.metric("Caracteres", chars)
            
            st.code(post_gerado, language="text")
            
            if st.button("📋 Copiar para Clipboard", use_container_width=True):
                st.success("✅ Copie o texto acima usando Ctrl+C!")
            
            if salvar:
                if "historico" not in st.session_state:
                    st.session_state.historico = []
                
                st.session_state.historico.append({
                    "tempo": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "plataforma": plataforma,
                    "produto": produto,
                    "preco": preco,
                    "post": post_gerado
                })
                st.success("✅ Post salvo no histórico!")
        else:
            st.error("⚠️ Preencha todos os campos obrigatórios!")

st.divider()
st.subheader("📚 Histórico de Posts")

if "historico" in st.session_state and st.session_state.historico:
    for i, item in enumerate(reversed(st.session_state.historico), 1):
        with st.expander(f"Post {i} - {item['plataforma']} | {item['produto']} ({item['tempo']})"):
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

st.divider()
st.markdown("""
<div style='text-align: center'>
    <p style='color: gray; font-size: 0.9em'>
    🚀 Gerador de Posts Multiplatforma v2.1 | Shopee • Mercado Livre • OLX • Trocafone
    </p>
</div>
""", unsafe_allow_html=True)
