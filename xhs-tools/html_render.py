def get_highlight_css(theme):
    # 仅内置三种主流主题，可扩展
    if theme == 'monokai':
        return '''<style>
        /* Monokai theme (简化版) */
        .codehilite { background: #272822; color: #f8f8f2; border-radius: 8px; padding: 1em; }
        .codehilite .hll { background-color: #49483e }
        .codehilite .c { color: #75715e } /* Comment */
        .codehilite .err { color: #960050; background-color: #1e0010 } /* Error */
        .codehilite .k { color: #66d9ef } /* Keyword */
        .codehilite .o { color: #f92672 } /* Operator */
        .codehilite .ch { color: #75715e } /* Comment.Hashbang */
        .codehilite .cm { color: #75715e } /* Comment.Multiline */
        .codehilite .cp { color: #75715e } /* Comment.Preproc */
        .codehilite .cpf { color: #75715e } /* Comment.PreprocFile */
        .codehilite .c1 { color: #75715e } /* Comment.Single */
        .codehilite .cs { color: #75715e } /* Comment.Special */
        .codehilite .gd { color: #f92672 } /* Generic.Deleted */
        .codehilite .ge { font-style: italic }
        .codehilite .gh { color: #66d9ef } /* Generic.Heading */
        .codehilite .gi { color: #a6e22e } /* Generic.Inserted */
        .codehilite .go { color: #75715e } /* Generic.Output */
        .codehilite .gp { color: #75715e } /* Generic.Prompt */
        .codehilite .gs { font-weight: bold }
        .codehilite .gu { color: #75715e } /* Generic.Subheading */
        .codehilite .kc { color: #66d9ef } /* Keyword.Constant */
        .codehilite .kd { color: #66d9ef } /* Keyword.Declaration */
        .codehilite .kn { color: #f92672 } /* Keyword.Namespace */
        .codehilite .kp { color: #66d9ef } /* Keyword.Pseudo */
        .codehilite .kr { color: #66d9ef } /* Keyword.Reserved */
        .codehilite .kt { color: #66d9ef } /* Keyword.Type */
        .codehilite .m { color: #ae81ff } /* Literal.Number */
        .codehilite .s { color: #e6db74 } /* Literal.String */
        .codehilite .na { color: #a6e22e } /* Name.Attribute */
        .codehilite .nb { color: #f8f8f2 } /* Name.Builtin */
        .codehilite .nc { color: #a6e22e } /* Name.Class */
        .codehilite .no { color: #66d9ef } /* Name.Constant */
        .codehilite .nd { color: #a6e22e } /* Name.Decorator */
        .codehilite .ni { color: #f8f8f2 } /* Name.Entity */
        .codehilite .ne { color: #a6e22e } /* Name.Exception */
        .codehilite .nf { color: #a6e22e } /* Name.Function */
        .codehilite .nl { color: #f8f8f2 } /* Name.Label */
        .codehilite .nn { color: #f8f8f2 } /* Name.Namespace */
        .codehilite .nt { color: #f92672 } /* Name.Tag */
        .codehilite .nv { color: #f8f8f2 } /* Name.Variable */
        .codehilite .ow { color: #f92672 } /* Operator.Word */
        .codehilite .w { color: #f8f8f2 } /* Text.Whitespace */
        .codehilite .mb { color: #ae81ff } /* Literal.Number.Bin */
        .codehilite .mf { color: #ae81ff } /* Literal.Number.Float */
        .codehilite .mh { color: #ae81ff } /* Literal.Number.Hex */
        .codehilite .mi { color: #ae81ff } /* Literal.Number.Integer */
        .codehilite .mo { color: #ae81ff } /* Literal.Number.Oct */
        .codehilite .sb { color: #e6db74 } /* Literal.String.Backtick */
        .codehilite .sc { color: #e6db74 } /* Literal.String.Char */
        .codehilite .sd { color: #e6db74 } /* Literal.String.Doc */
        .codehilite .s2 { color: #e6db74 } /* Literal.String.Double */
        .codehilite .se { color: #ae81ff } /* Literal.String.Escape */
        .codehilite .sh { color: #e6db74 } /* Literal.String.Heredoc */
        .codehilite .si { color: #e6db74 } /* Literal.String.Interpol */
        .codehilite .sx { color: #e6db74 } /* Literal.String.Other */
        .codehilite .sr { color: #e6db74 } /* Literal.String.Regex */
        .codehilite .s1 { color: #e6db74 } /* Literal.String.Single */
        .codehilite .ss { color: #e6db74 } /* Literal.String.Symbol */
        .codehilite .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
        .codehilite .vc { color: #f8f8f2 } /* Name.Variable.Class */
        .codehilite .vg { color: #f8f8f2 } /* Name.Variable.Global */
        .codehilite .vi { color: #f8f8f2 } /* Name.Variable.Instance */
        .codehilite .il { color: #ae81ff } /* Literal.Number.Integer.Long */
        </style>'''
    elif theme == 'dracula':
        return '''<style>
        /* Dracula theme (简化版) */
        .codehilite { background: #282a36; color: #f8f8f2; border-radius: 8px; padding: 1em; }
        .codehilite .k { color: #ff79c6 }
        .codehilite .s { color: #f1fa8c }
        .codehilite .c { color: #6272a4 }
        .codehilite .n { color: #f8f8f2 }
        .codehilite .o { color: #ff79c6 }
        .codehilite .m { color: #bd93f9 }
        .codehilite .p { color: #f8f8f2 }
        .codehilite .nf { color: #50fa7b }
        .codehilite .nb { color: #8be9fd }
        .codehilite .nn { color: #f8f8f2 }
        .codehilite .nc { color: #8be9fd }
        .codehilite .no { color: #bd93f9 }
        .codehilite .nd { color: #8be9fd }
        .codehilite .ni { color: #f8f8f2 }
        .codehilite .ne { color: #ffb86c }
        .codehilite .nt { color: #ff79c6 }
        .codehilite .nv { color: #f8f8f2 }
        .codehilite .w { color: #f8f8f2 }
        </style>'''
    else:  # github默认
        return '''<style>
        /* GitHub theme (简化版) */
        .codehilite { background: #f6f8fa; color: #24292e; border-radius: 8px; padding: 1em; }
        .codehilite .k { color: #d73a49 }
        .codehilite .s { color: #032f62 }
        .codehilite .c { color: #6a737d }
        .codehilite .n { color: #24292e }
        .codehilite .o { color: #d73a49 }
        .codehilite .m { color: #005cc5 }
        .codehilite .p { color: #24292e }
        .codehilite .nf { color: #6f42c1 }
        .codehilite .nb { color: #24292e }
        .codehilite .nn { color: #24292e }
        .codehilite .nc { color: #6f42c1 }
        .codehilite .no { color: #005cc5 }
        .codehilite .nd { color: #6f42c1 }
        .codehilite .ni { color: #24292e }
        .codehilite .ne { color: #d73a49 }
        .codehilite .nt { color: #22863a }
        .codehilite .nv { color: #24292e }
        .codehilite .w { color: #24292e }
        </style>'''

def render_article_html(title, content, desc, style_type='simple', is_html=False, highlight=True, highlight_theme='github'):
    highlight_css = get_highlight_css(highlight_theme) if highlight else ''
    if is_html:
        paragraphs = content
    else:
        paragraphs = ''.join('<p>{}</p>'.format(line.strip()) for line in content.split('\n') if line.strip())
    if style_type == 'simple':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #fff8f0; font-family: '微软雅黑', Arial, sans-serif; color: #333; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px #f3cfcf; padding: 2em; }}
        h1 {{ color: #e57373; font-size: 2em; text-align: center; margin-bottom: 1em; }}
        .desc {{ color: #ba68c8; font-size: 1.1em; margin-bottom: 1.5em; text-align: center; }}
        .content p {{ margin: 1em 0; line-height: 1.8; font-size: 1.1em; }}
        </style></head><body>
        <div class="container">
          <h1>{title}</h1>
          <div class="desc">{desc}</div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'card':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #f6f7fb; font-family: '微软雅黑', Arial, sans-serif; color: #222; margin: 0; padding: 0; }}
        .container {{ max-width: 620px; margin: 2em auto; background: #fff; border-radius: 18px; box-shadow: 0 4px 24px #e0e0e0; padding: 2.5em 2em; }}
        h1 {{ color: #d32f2f; font-size: 2.2em; margin-bottom: 0.7em; text-align: left; }}
        .desc {{ background: #ffeaea; color: #d32f2f; font-size: 1.1em; border-radius: 8px; padding: 0.8em 1em; margin-bottom: 1.5em; }}
        .content p {{ margin: 1.2em 0; line-height: 1.9; font-size: 1.13em; border-bottom: 1px solid #f3cfcf; padding-bottom: 0.5em; }}
        </style></head><body>
        <div class="container">
          <h1>{title}</h1>
          <div class="desc">{desc}</div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'minimal':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #fff; font-family: '微软雅黑', Arial, sans-serif; color: #111; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fff; border: 2px solid #222; border-radius: 10px; padding: 2em; }}
        h1 {{ color: #111; font-size: 2em; font-weight: bold; text-align: left; border-bottom: 2px solid #111; padding-bottom: 0.5em; margin-bottom: 1em; }}
        .desc {{ color: #444; font-size: 1.1em; margin-bottom: 1.5em; border-left: 4px solid #111; padding-left: 1em; }}
        .content p {{ margin: 1.2em 0; line-height: 2.1; font-size: 1.15em; }}
        </style></head><body>
        <div class="container">
          <h1>{title}</h1>
          <div class="desc">{desc}</div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'kawaii':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #fff0fa; font-family: '幼圆', '微软雅黑', Arial, sans-serif; color: #ff69b4; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fff6fb; border-radius: 30px; box-shadow: 0 4px 24px #ffd6ec; padding: 2.5em 2em; border: 3px dashed #ffb6d5; }}
        h1 {{ color: #ff69b4; font-size: 2.1em; text-align: center; margin-bottom: 1em; letter-spacing: 2px; text-shadow: 1px 2px 8px #ffe4f7; }}
        .desc {{ background: #ffe4f7; color: #ff69b4; font-size: 1.1em; border-radius: 16px; padding: 1em 1.2em; margin-bottom: 1.5em; text-align: center; box-shadow: 0 2px 8px #ffd6ec; }}
        .content p {{ margin: 1.2em 0; line-height: 2.1; font-size: 1.13em; background: #fff0fa; border-radius: 12px; padding: 0.7em 1em; box-shadow: 0 1px 4px #ffd6ec; border-left: 6px solid #ffb6d5; }}
        </style></head><body>
        <div class="container">
          <h1>🌸{title}🌸</h1>
          <div class="desc">{desc} <span style='font-size:1.3em;'>ฅ^•ﻌ•^ฅ</span></div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'emoji':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #fffbe7; font-family: '幼圆', '微软雅黑', Arial, sans-serif; color: #ff9800; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fffde7; border-radius: 30px; box-shadow: 0 4px 24px #ffe082; padding: 2.5em 2em; border: 3px dashed #ffd54f; }}
        h1 {{ color: #ff9800; font-size: 2.1em; text-align: center; margin-bottom: 1em; letter-spacing: 2px; text-shadow: 1px 2px 8px #ffe082; }}
        .desc {{ background: #fff8e1; color: #ff9800; font-size: 1.1em; border-radius: 16px; padding: 1em 1.2em; margin-bottom: 1.5em; text-align: center; box-shadow: 0 2px 8px #ffe082; }}
        .content p {{ margin: 1.2em 0; line-height: 2.1; font-size: 1.13em; background: #fffbe7; border-radius: 12px; padding: 0.7em 1em; box-shadow: 0 1px 4px #ffe082; border-left: 6px solid #ffd54f; }}
        </style></head><body>
        <div class="container">
          <h1>✨{title}✨</h1>
          <div class="desc">{desc} <span style='font-size:1.3em;'>😊🚀🌈</span></div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'macaron':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: linear-gradient(135deg, #ffe0f7 0%, #e0f7fa 100%); font-family: '微软雅黑', Arial, sans-serif; color: #a259ff; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fff; border-radius: 32px; box-shadow: 0 8px 36px #b2f7ef; padding: 2.5em 2em; border: 3px solid #a259ff; }}
        h1 {{ color: #a259ff; font-size: 2.1em; text-align: center; margin-bottom: 1em; letter-spacing: 2px; text-shadow: 1px 2px 8px #ffe4f7; }}
        .desc {{ background: #e0f7fa; color: #a259ff; font-size: 1.1em; border-radius: 16px; padding: 1em 1.2em; margin-bottom: 1.5em; text-align: center; box-shadow: 0 2px 8px #ffd6ec; }}
        .content p {{ margin: 1.2em 0; line-height: 2.1; font-size: 1.13em; background: #ffe0f7; border-radius: 12px; padding: 0.7em 1em; box-shadow: 0 1px 4px #ffd6ec; border-left: 6px solid #a259ff; }}
        </style></head><body>
        <div class="container">
          <h1>🍬{title}🍬</h1>
          <div class="desc">{desc} <span style='font-size:1.3em;'>🧁🍭🍡</span></div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'sticker':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        body {{ background: #f9fbe7; font-family: '微软雅黑', Arial, sans-serif; color: #43a047; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 2em auto; background: #fff; border-radius: 28px; box-shadow: 0 6px 32px #c5e1a5; padding: 2.5em 2em; border: 3px dashed #43a047; position: relative; }}
        h1 {{ color: #43a047; font-size: 2em; text-align: left; margin-bottom: 1em; letter-spacing: 1px; }}
        .desc {{ background: #e8f5e9; color: #43a047; font-size: 1.1em; border-radius: 12px; padding: 0.8em 1em; margin-bottom: 1.5em; text-align: left; box-shadow: 0 2px 8px #c5e1a5; }}
        .content p {{ margin: 1.2em 0; line-height: 2.1; font-size: 1.13em; background: #f1f8e9; border-radius: 10px; padding: 0.7em 1em; box-shadow: 0 1px 4px #c5e1a5; border-left: 6px solid #43a047; }}
        .sticker {{ position: absolute; top: -18px; right: -18px; background: #fffde7; color: #ff9800; border: 2px solid #ffd54f; border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; font-size: 2em; box-shadow: 0 2px 8px #ffe082; }}
        </style></head><body>
        <div class="container">
          <div class="sticker">📎</div>
          <h1>{title}</h1>
          <div class="desc">{desc} <span style='font-size:1.2em;'>🌟</span></div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    else:
        # 默认用simple
        return render_article_html(title, content, desc, style_type='simple', is_html=is_html, highlight=highlight, highlight_theme=highlight_theme)
    return html 