import streamlit as st
import json
import os
import time
from datetime import datetime

st.set_page_config(page_title="🛒 Gerador de Posts Multiplatforma", layout="wide")

st.title("🛒 Gerador de Posts Multiplatforma")
st.markdown("_Crie posts para Shopee, Mercado Livre, OLX, Trocafone e mais!_")

# Criar pasta uploads se não existir
os.makedirs("uploads", exist_ok=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    plataforma = st.selectbox(
        "Escolha a plataforma:",
        ["🛍️ Shopee", "🏪 Mercado Livre", "📱 OLX", "🔄 Trocafone", "📦 Genérico"]
    )
    
    estilo = st.selectbox(
        "Escolha o estilo:",
        ["🚨 Urgente", "🌟 Premium", "💎 Luxo", "🎉 Celebração", "⚡ Flash Sale"]
    )
    
    tom = st.radio("Tom:", ["Casual", "Profissional", "Divertido"])

st.divider()
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("📝 Informações do Produto")
    
    produto = st.text_input("Nome do Produto", placeholder="Ex: Fone Bluetooth")
    preco = st.text_input("Preço", placeholder="Ex: 89,90")
    desconto = st.number_input("Desconto (%)", min_value=0, max_value=100, value=0)
    link = st.text_input("Link", placeholder="https://...")
    avaliacao = st.slider("Avaliação ⭐", 0.0, 5.0, 4.5, step=0.5)
    
    with st.expander("📦 Detalhes"):
        estoque = st.text_input("Estoque", placeholder="Limitado")
        frete = st.toggle("Frete Grátis?", value=True)
        condicao = st.selectbox("Condição", ["Novo", "Seminovo", "Recondicionado"])
    
    # Upload imagem
    uploaded = st.file_uploader("📷 Imagem do produto", type=["png", "jpg", "jpeg"])
    if uploaded:
        filename = f"{int(time.time())}_{uploaded.name}"
        path = os.path.join("uploads", filename)
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.session_state["img_path"] = path
        st.success("✅ Imagem enviada!")

def gerar_post(pnome, ppreco, plink, plat, estilo_s, ton_s, paval, pdesc, pest, pfrete, pcond, pimg=None):
    if not all([pnome, ppreco, plink]):
        return None
    
    pf = ppreco if pdesc == 0 else f"~~R$ {ppreco}~~ → R$ {ppreco} (-{pdesc}%)"
    stars = "⭐" * int(paval)
    
    if plat == "🛍️ Shopee":
        templates = {
            "🚨 Urgente": f"🚨 ACHADO IMPERDÍVEL NA SHOPEE!\n\n📦 {pnome}\n⭐ {stars}\n💰 {pf}\n{'🚚 Frete Grátis!' if pfrete else '📦 Frete'}\n\n🛒 {plink}\n\n#shopee #oferta",
            "🌟 Premium": f"✨ PRODUTO PREMIUM SHOPEE ✨\n\n{pnome}\n⭐ {stars}\n💎 {pf}\n{'✅ Frete Grátis' if pfrete else 'Frete'}\n\n👉 {plink}\n\n#shopee #premium",
            "💎 Luxo": f"💎 LUXO E ELEGÂNCIA SHOPEE 💎\n\n{pnome}\n⭐ {stars}\nInvestimento: {pf}\n{'Entrega Grátis' if pfrete else 'Entrega Rápida'}\n\n{plink}\n\n#shopee #luxo",
            "🎉 Celebração": f"🎉 CELEBRE COM A SHOPEE! 🎉\n\n{pnome}\n⭐ Adoram!\n\nDe: ~~R$ {ppreco}~~ Por: {pf}\n\n👉 {plink}\n\n#shopee #promoção",
            "⚡ Flash Sale": f"⚡ FLASH SALE SHOPEE ⚡\n🔥 SUPER PROMOÇÃO 🔥\n\n{pnome}\n⭐ {stars}\nAGORA: {pf}\n{'FRETE GRÁTIS' if pfrete else 'Frete'}\n\n{plink}\n\n#shopee #desconto",
        }
    elif plat == "🏪 Mercado Livre":
        templates = {
            "🚨 Urgente": f"🚨 OPORTUNIDADE MERCADO LIVRE!\n\n{pnome}\n⭐⭐⭐⭐⭐\n💰 {pf}\n{'Frete Grátis' if pfrete else 'Frete'}\n\n{plink}\n\n#mercadolivre",
            "🌟 Premium": f"✨ DESTAQUE MERCADO LIVRE ✨\n\n{pnome}\n⭐⭐⭐⭐⭐\n💎 {pf}\n\n{plink}\n\n#mercadolivre #premium",
            "💎 Luxo": f"💎 QUALIDADE MERCADO LIVRE 💎\n\n{pnome}\n⭐⭐⭐⭐⭐\nPreço: {pf}\n\n{plink}\n\n#mercadolivre",
            "🎉 Celebração": f"🎉 QUEIMA DE ESTOQUE MERCADO LIVRE!\n\n{pnome}\nOfertão: {pf}\n\n{plink}\n\n#mercadolivre",
            "⚡ Flash Sale": f"⚡ DESCONTO RELÂMPAGO MERCADO LIVRE ⚡\n\n{pnome}\nAGORA: {pf}\n\n{plink}\n\n#mercadolivre #desconto",
        }
    elif plat == "📱 OLX":
        templates = {
            "🚨 Urgente": f"🚨 APROVEITA OLX!\n\n{pnome}\n⭐ {stars}\n💰 {pf}\n\n{plink}\n\n#olx",
            "🌟 Premium": f"✨ QUALIDADE OLX ✨\n\n{pnome}\n⭐ {stars}\nPreço: {pf}\n\n{plink}\n\n#olx",
            "💎 Luxo": f"💎 SELECIONADO OLX 💎\n\n{pnome}\n⭐ {stars}\n{pf}\n\n{plink}\n\n#olx",
            "🎉 Celebração": f"🎉 PROMOÇÃO OLX! 🎉\n\n{pnome}\nDe: ~~R$ {ppreco}~~ Para: {pf}\n\n{plink}\n\n#olx",
            "⚡ Flash Sale": f"⚡ OFERTA RELÂMPAGO OLX ⚡\n\n{pnome}\nAPENAS: {pf}\n\n{plink}\n\n#olx",
        }
    elif plat == "🔄 Trocafone":
        templates = {
            "🚨 Urgente": f"🚨 APARELHO IMPRESCINDÍVEL TROCAFONE!\n\n📱 {pnome}\n⭐ {stars}\n💰 {pf}\n\n{plink}\n\n#trocafone",
            "🌟 Premium": f"✨ QUALIDADE TROCAFONE ✨\n\n{pnome}\n⭐ {stars}\nPreço: {pf}\n\n{plink}\n\n#trocafone",
            "💎 Luxo": f"💎 CELULAR PREMIUM TROCAFONE 💎\n\n{pnome}\n⭐ {stars}\n{pf}\n\n{plink}\n\n#trocafone",
            "🎉 Celebração": f"🎉 OFERTA IMPERDÍVEL TROCAFONE! 🎉\n\n{pnome}\nDe: ~~R$ {ppreco}~~ Para: {pf}\n\n{plink}\n\n#trocafone",
            "⚡ Flash Sale": f"⚡ PROMOÇÃO TROCAFONE ⚡\n\n{pnome}\nOFERTA: {pf}\n\n{plink}\n\n#trocafone",
        }
    else:
        templates = {
            "🚨 Urgente": f"🚨 IMPERDÍVEL!\n\n{pnome}\n⭐ {stars}\n💰 {pf}\n\n{plink}\n\n#oferta",
            "🌟 Premium": f"✨ QUALIDADE ✨\n\n{pnome}\n⭐ {stars}\n{pf}\n\n{plink}",
            "💎 Luxo": f"💎 LUXO 💎\n\n{pnome}\n⭐ {stars}\n{pf}\n\n{plink}",
            "🎉 Celebração": f"🎉 CELEBRE! 🎉\n\n{pnome}\n{pf}\n\n{plink}",
            "⚡ Flash Sale": f"⚡ FLASH SALE ⚡\n\n{pnome}\n{pf}\n\n{plink}",
        }
    
    post = templates.get(estilo_s, templates["🚨 Urgente"])
    
    if ton_s == "Casual":
        post = post.replace("Frete", "Entrega").replace("Clique", "Vem")
    elif ton_s == "Divertido":
        post = post.replace("Aproveita", "Corre! 😂").replace("Compre", "Quer? 🎉")
    
    return post

with col2:
    st.subheader("👁️ Preview")
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        gerar = st.button("✨ Gerar", use_container_width=True, type="primary")
    with col_btn2:
        limpar = st.button("🔄 Limpar", use_container_width=True)
    with col_btn3:
        salvar = st.button("💾 Salvar", use_container_width=True)
    
    if limpar:
        st.session_state.clear()
        st.rerun()
    
    if gerar or st.session_state.get("post_gerado"):
        img_path = st.session_state.get("img_path")
        post = gerar_post(produto, preco, link, plataforma, estilo, tom, avaliacao, desconto, estoque, frete, condicao, img_path)
        
        if post:
            st.session_state.post_gerado = post
            
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            
            st.metric("Caracteres", len(post))
            st.code(post, language="text")
            
            if st.button("📋 Copiar", use_container_width=True):
                st.success("✅ Copie com Ctrl+C!")
            
            if salvar:
                if "historico" not in st.session_state:
                    st.session_state.historico = []
                
                st.session_state.historico.append({
                    "tempo": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "plataforma": plataforma,
                    "produto": produto,
                    "preco": preco,
                    "image": img_path,
                    "post": post
                })
                st.success("✅ Salvo!")
        else:
            st.error("⚠️ Preencha: Produto, Preço e Link!")

st.divider()
st.subheader("📚 Histórico")

if "historico" in st.session_state and st.session_state.historico:
    for i, item in enumerate(reversed(st.session_state.historico), 1):
        with st.expander(f"{i}. {item['plataforma']} | {item['produto']}"):
            st.code(item["post"], language="text")
            col_a, col_b = st.columns(2)
            with col_a:
                st.text(f"R$ {item['preco']}")
            with col_b:
                if st.button(f"🗑️ {i}", key=f"del_{i}", use_container_width=True):
                    st.session_state.historico = [x for j, x in enumerate(reversed(st.session_state.historico)) if j != i-1]
                    st.rerun()
else:
    st.info("📝 Nenhum post salvo")

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
🚀 Gerador de Posts Multiplatforma v2.2 | Shopee • Mercado Livre • OLX • Trocafone
</div>
""", unsafe_allow_html=True)
