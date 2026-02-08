import customtkinter as ctk
import pyperclip
from datetime import datetime
import json
import os

# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛍️ Gerador de Posts Shopee v2.0")
        self.geometry("900x750")
        self.historico_posts = []
        self.carregar_historico()
        
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(main_frame, text="🛍️ Gerador de Posts Shopee v2.0", 
                             font=("Arial", 24, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)
        
        # ===== COLUNA ESQUERDA - ENTRADA =====
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_frame, text="📝 Informações do Produto", 
                    font=("Arial", 16, "bold")).pack(pady=10)
        
        # Campos de entrada
        ctk.CTkLabel(left_frame, text="Nome do Produto:").pack(anchor="w", padx=10)
        self.produto = ctk.CTkEntry(left_frame, placeholder_text="Ex: Fone Bluetooth")
        self.produto.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Preço:").pack(anchor="w", padx=10)
        self.preco = ctk.CTkEntry(left_frame, placeholder_text="Ex: 89,90")
        self.preco.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Desconto (%):").pack(anchor="w", padx=10)
        self.desconto = ctk.CTkEntry(left_frame, placeholder_text="Ex: 15")
        self.desconto.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Link de Afiliado:").pack(anchor="w", padx=10)
        self.link = ctk.CTkEntry(left_frame, placeholder_text="https://shopee.com.br/...")
        self.link.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(left_frame, text="Avaliação (⭐):").pack(anchor="w", padx=10)
        self.avaliacao = ctk.CTkSlider(left_frame, from_=0, to=5, number_of_steps=10)
        self.avaliacao.set(4.5)
        self.avaliacao.pack(fill="x", padx=10, pady=(0, 10))
        
        # Checkboxes
        self.frete_gratis = ctk.CTkCheckBox(left_frame, text="✅ Frete Grátis")
        self.frete_gratis.pack(anchor="w", padx=10, pady=5)
        
        self.estoque_limitado = ctk.CTkCheckBox(left_frame, text="⏰ Estoque Limitado")
        self.estoque_limitado.pack(anchor="w", padx=10, pady=5)
        
        # Seleção de Estilo
        ctk.CTkLabel(left_frame, text="Estilo do Post:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        self.estilo = ctk.CTkOptionMenu(left_frame, values=["🚨 Urgente", "🌟 Premium", "💎 Luxo", "🎉 Celebração", "⚡ Flash Sale"])
        self.estilo.set("🚨 Urgente")
        self.estilo.pack(fill="x", padx=10, pady=(0, 10))
        
        # Tone
        ctk.CTkLabel(left_frame, text="Tom do Post:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        self.tom = ctk.CTkOptionMenu(left_frame, values=["Casual", "Profissional", "Divertido"])
        self.tom.set("Casual")
        self.tom.pack(fill="x", padx=10, pady=(0, 20))
        
        # ===== COLUNA DIREITA - PREVIEW E AÇÕES =====
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_frame, text="👁️ Preview", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Text widget para preview
        self.preview = ctk.CTkTextbox(right_frame, width=400, height=350)
        self.preview.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Contador de caracteres
        self.char_count = ctk.CTkLabel(right_frame, text="📊 Caracteres: 0")
        self.char_count.pack(anchor="e", padx=10, pady=5)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(right_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_gerar = ctk.CTkButton(btn_frame, text="✨ Gerar", command=self.gerar_post, height=40)
        self.btn_gerar.pack(side="left", fill="both", expand=True, padx=5)
        
        self.btn_copiar = ctk.CTkButton(btn_frame, text="📋 Copiar", command=self.copiar_clipboard, height=40)
        self.btn_copiar.pack(side="left", fill="both", expand=True, padx=5)
        
        self.btn_salvar = ctk.CTkButton(btn_frame, text="💾 Salvar", command=self.salvar_post, height=40)
        self.btn_salvar.pack(side="left", fill="both", expand=True, padx=5)
        
        # Histórico
        hist_frame = ctk.CTkFrame(main_frame)
        hist_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(20, 0))
        
        ctk.CTkLabel(hist_frame, text="📚 Histórico de Posts", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=10)
        
        # Scrollable frame para histórico
        scroll_frame = ctk.CTkScrollableFrame(hist_frame, height=150)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.historico_frame = scroll_frame
        
        self.atualizar_historico_ui()
        
        # Status
        self.status = ctk.CTkLabel(main_frame, text="", text_color="green")
        self.status.grid(row=3, column=0, columnspan=2, pady=10)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def gerar_post(self):
        """Gera o post baseado nas informações inseridas"""
        p = self.produto.get()
        v = self.preco.get()
        l = self.link.get()
        desc = self.desconto.get()
        aval = self.avaliacao.get()
        frete = self.frete_gratis.get()
        estoque = self.estoque_limitado.get()
        estilo = self.estilo.get()
        tom = self.tom.get()
        
        if not all([p, v, l]):
            self.status.configure(text="⚠️ Preencha Nome, Preço e Link!")
            return
        
        # Formatar preço com desconto
        try:
            desc_num = float(desc) if desc else 0
        except:
            desc_num = 0
        
        preco_formatado = f"R$ {v}" if desc_num == 0 else f"~~R$ {v}~~ → R$ {v} (-{desc_num:.0f}%)"
        avaliacao_stars = "⭐" * int(aval)
        
        # Templates
        templates = {
            "🚨 Urgente": f"""🚨 ACHADO IMPERDÍVEL! 🚨

📦 {p}
⭐ {avaliacao_stars}
💰 {preco_formatado}
{"🚚 Frete Grátis!" if frete else "📦 Frete Cobrado"}
{"⏰ Estoque Limitado!" if estoque else ""}

🛒 Compre aqui: {l}

#shopee #achadinhos #oferta #imperdível""",
            
            "🌟 Premium": f"""✨ PRODUTO PREMIUM ✨

{p}
⭐ Avaliação: {avaliacao_stars}

💎 Preço: {preco_formatado}
{"✅ Frete Grátis" if frete else "📦 Frete Cobrado"}
{"⏰ Quantidade Limitada" if estoque else ""}

👉 Clique aqui: {l}

#shopee #premium #qualidade""",
            
            "💎 Luxo": f"""💎 LUXO E ELEGÂNCIA 💎

{p}
Nota: {avaliacao_stars}

Investimento: {preco_formatado}
{"Entrega Grátis" if frete else "Entrega Rápida"} 🚀
{"Exclusivo e Limitado" if estoque else "Disponível"}

Descubra: {l}

#shopee #luxo #seleção""",
            
            "🎉 Celebração": f"""🎉 CELEBRE COM A GENTE! 🎉

Apresentamos: {p}
{avaliacao_stars}

De: ~~R$ {v}~~ Para: {preco_formatado}
{"🎁 Brinde: Frete Grátis" if frete else "Entrega Rápida"}
{"Aproveita Enquanto Duraaaaa!" if estoque else ""}

Quero o meu: {l}

#shopee #promoção #celebração""",
            
            "⚡ Flash Sale": f"""⚡ FLASH SALE ⚡
🔥 SUPER PROMOÇÃO 🔥

{p}
Nota: {avaliacao_stars}

AGORA: {preco_formatado}
{"✅ FRETE GRÁTIS" if frete else "Entrega Cobrada"}
{"⏰ APROVEITA!" if estoque else "Em Estoque"}

LINK: {l}

#shopee #fleshsale #promoção"""
        }
        
        post = templates.get(estilo, templates["🚨 Urgente"])
        
        # Aplicar tom
        if tom == "Divertido":
            post = post.replace("Clique aqui", "Pula pra cá! 😂").replace("Compre", "Bora logo")
        elif tom == "Profissional":
            post = post.replace("Achado", "Produto").replace("Imperdível", "Excepcional")
        
        # Exibir preview
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", post)
        
        # Contar caracteres
        char_count = len(post)
        self.char_count.configure(text=f"📊 Caracteres: {char_count}")
        
        self.status.configure(text="✨ Post gerado com sucesso!")

    def copiar_clipboard(self):
        """Copia o post para a área de transferência"""
        texto = self.preview.get("1.0", "end").strip()
        if texto:
            pyperclip.copy(texto)
            self.status.configure(text="✅ Copiado para a área de transferência!")
        else:
            self.status.configure(text="⚠️ Gere um post primeiro!")

    def salvar_post(self):
        """Salva o post no histórico"""
        texto = self.preview.get("1.0", "end").strip()
        produto = self.produto.get()
        
        if texto and produto:
            post_data = {
                "tempo": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "produto": produto,
                "preco": self.preco.get(),
                "post": texto
            }
            self.historico_posts.append(post_data)
            self.salvar_historico()
            self.atualizar_historico_ui()
            self.status.configure(text="💾 Post salvo no histórico!")
        else:
            self.status.configure(text="⚠️ Gere um post primeiro!")

    def atualizar_historico_ui(self):
        """Atualiza a exibição do histórico"""
        for widget in self.historico_frame.winfo_children():
            widget.destroy()
        
        if not self.historico_posts:
            ctk.CTkLabel(self.historico_frame, text="Nenhum post salvo ainda").pack(padx=10, pady=20)
        else:
            for i, item in enumerate(reversed(self.historico_posts)):
                btn = ctk.CTkButton(
                    self.historico_frame,
                    text=f"📌 {item['produto']} - {item['tempo']}",
                    command=lambda idx=i: self.carregar_post(idx),
                    width=300,
                    height=35
                )
                btn.pack(fill="x", padx=5, pady=5)

    def carregar_post(self, idx):
        """Carrega um post do histórico para o preview"""
        post = self.historico_posts[idx]
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", post["post"])
        self.char_count.configure(text=f"📊 Caracteres: {len(post['post'])}")
        self.status.configure(text=f"📌 Post restaurado: {post['produto']}")

    def salvar_historico(self):
        """Salva histórico em arquivo JSON"""
        try:
            with open("historico_posts.json", "w", encoding="utf-8") as f:
                json.dump(self.historico_posts, f, ensure_ascii=False, indent=2)
        except:
            pass

    def carregar_historico(self):
        """Carrega histórico de arquivo JSON"""
        try:
            if os.path.exists("historico_posts.json"):
                with open("historico_posts.json", "r", encoding="utf-8") as f:
                    self.historico_posts = json.load(f)
        except:
            self.historico_posts = []

app = App()
app.mainloop()