# 🛍️ Gerador de Posts Shopee v2.0

Um sistema completo para gerar posts automáticos para a Shopee com múltiplos estilos, funcionalidades avançadas e histórico de posts.

## 📂 Arquivos do Projeto

- **`app_web.py`** — Versão web com Streamlit (publicável em Streamlit Cloud)
- **`teste.py`** — Versão desktop com CustomTkinter (executável local)
- **`requirements.txt`** — Dependências do projeto
- **`historico_posts.json`** — Histórico de posts gerados (criado automaticamente)

---

## 🚀 Funcionalidades v2.0

### ✨ Gerador com Múltiplos Estilos
- **🚨 Urgente** — Posts com tom de urgência
- **🌟 Premium** — Posts elegantes e profissionais
- **💎 Luxo** — Posts de alto padrão
- **🎉 Celebração** — Posts festivos e divertidos
- **⚡ Flash Sale** — Posts de promoção relâmpago

### 🎛️ Opções de Personalização
- Seleção de **tom do post** (Casual, Profissional, Divertido)
- Campo para **desconto em %**
- **Avaliação do produto** (⭐ 0-5 estrelas)
- Toggle para **frete grátis**
- Toggle para **estoque limitado**
- Contador de **caracteres em tempo real**

### 📚 Histórico e Gestão
- ✅ Salve automaticamente seus posts
- 📌 Carregue posts anteriores com um clique
- 💾 Histórico persistente em JSON

---

## 🖥️ Como Usar

### Versão Desktop (Recomendado para Uso Local)

```bash
# 1. Ativar o ambiente virtual
.venv\Scripts\activate.bat

# 2. Executar a aplicação
python teste.py
```

Funcionalidades:
- Interface gráfica completa
- Histórico salvo localmente no arquivo `historico_posts.json`
- Preview em tempo real
- Cópia direta para clipboard com `Ctrl+C` ou botão "Copiar"

### Versão Web (Recomendado para Publicar Online)

```bash
# 1. Ativar o ambiente virtual
.venv\Scripts\activate.bat

# 2. Executar com Streamlit
streamlit run app_web.py
```

A aplicação abrirá em: `http://localhost:8501`

---

## 📤 Publicar no Streamlit Cloud

1. **Prepare seu repositório GitHub:**
```bash
git init
git add .
git commit -m "Initial commit: Shoppe Post Generator v2.0"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
git push -u origin main
```

2. **Faça deploy:**
   - Acesse: https://share.streamlit.io
   - Clique em **New app**
   - Conecte ao GitHub
   - Escolha: repositório, branch `main`, arquivo `app_web.py`
   - Clique em **Deploy**

3. **Use no celular:**
   - Abra o link gerado
   - Android: Menu do Chrome → **Add to Home screen**
   - iOS: Safari → **Add to Home Screen**

---

## 📋 Requisitos

O `requirements.txt` inclui:
- `customtkinter==5.2.2` — Interface desktop moderna
- `pyperclip==1.11.0` — Cópia para clipboard
- `streamlit==1.54.0` — Framework web

---

## 🎨 Exemplos de Posts Gerados

### 🚨 Estilo Urgente:
```
🚨 ACHADO IMPERDÍVEL! 🚨
📦 Fone Bluetooth
⭐⭐⭐⭐
💰 R$ 89,90
🚚 Frete Grátis!
🛒 Compre aqui: [link]
#shopee #achadinhos #oferta
```

### 💎 Estilo Luxo:
```
💎 LUXO E ELEGÂNCIA 💎
Fone Bluetooth
Nota: ⭐⭐⭐⭐⭐
Investimento: R$ 89,90
Entrega Grátis 🚀
Descubra: [link]
#shopee #luxo #seleção
```

---

## 💡 Dicas de Uso

✅ **Para Melhor Performance:**
- Use a versão desktop para editar múltiplos posts rapidamente
- Use a versão web para compartilhar com equipe ou publicar online
- Mantenha seus posts com **até 150-200 caracteres** para máximo alcance no Shopee

✅ **Boas Práticas:**
- Adicione um desconto percentual para chamar mais atenção
- Use avaliações altas para criar confiança
- Marque "Estoque Limitado" para criar urgência
- Utilize o tom "Divertido" para produtos mais informais

---

## 📝 Histórico de Versões

### v2.0 (Atual)
- ✨ 5 estilos diferentes de posts
- 🎛️ Múltiplas opções de personalização
- 📚 Histórico persistente
- 🌐 Versão web em Streamlit
- 📊 Contador de caracteres

### v1.0 (Original)
- ✅ Gerador básico de posts
- 📋 Cópia para clipboard
- 🎨 Interface simples

---

## 🤝 Contribuições

Quer melhorar o projeto? Abra uma issue ou PR!

---

## 📄 Licença

Este projeto é de uso livre para fins comerciais e pessoais.

Se quiser, eu posso preparar os comandos `git` aqui ou te guiar passo a passo no push e no deploy. 🛠️