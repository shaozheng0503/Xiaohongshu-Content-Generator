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

def render_article_html(title, content, desc, style_type='simple', is_html=False, highlight=True, highlight_theme='github', badge_text='原创'):
    highlight_css = get_highlight_css(highlight_theme) if highlight else ''
    if is_html:
        paragraphs = content
    else:
        # 段落前自动加emoji
        emoji_list = ['💡', '📌', '✨', '🌟', '📝', '🎯', '🔖', '🚀', '🎀', '🍀']
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        paragraphs = ''.join(f'<p>{emoji_list[i%len(emoji_list)]} {line}</p>' for i, line in enumerate(lines))
    
    # 角标内容 - 简化样式
    badge = ''
    if style_type in ['card', 'minimal', 'simple', 'gradient', 'fresh', 'macaron', 'cream']:
        badge = f"<div style='position:absolute;top:10px;right:18px;background:#ff9800;color:#fff;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:bold;'>{badge_text}</div>"
    elif style_type in ['kawaii', 'emoji', 'sticker', 'retro', 'apple']:
        badge = f"<div style='position:absolute;top:10px;right:18px;background:#1976d2;color:#fff;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:bold;'>{badge_text}</div>"
    elif style_type == 'clean':
        # 纯白底极简模板不使用角标，保持最大简洁性
        badge = ''
    
    # 自定义字体
    font_family = ''
    if style_type in ['kawaii', 'cream']:
        font_family = "font-family:'Comic Sans MS','幼圆','微软雅黑',cursive,sans-serif;"
    elif style_type == 'retro':
        font_family = "font-family:'Fira Mono','微软雅黑',monospace;"
    elif style_type == 'apple':
        font_family = "font-family:'SF Pro Display','微软雅黑',Arial,sans-serif;"
    else:
        font_family = "font-family:'微软雅黑',Arial,sans-serif;"
    
    if style_type == 'clean':
        # 纯白底极简模板 - 移除所有不支持的CSS属性
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #ffffff; 
            color: #333; 
            font-family: '微软雅黑', Arial, sans-serif; 
            padding: 30px 25px; 
            line-height: 1.6;
            font-size: 16px;
        }}
        .container {{ 
            max-width: 550px; 
            margin: 0 auto; 
            background: #ffffff; 
        }}
        h1 {{ 
            color: #222; 
            font-size: 24px; 
            font-weight: 600;
            margin-bottom: 20px; 
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .desc {{ 
            color: #666; 
            font-size: 14px; 
            margin-bottom: 25px; 
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
        }}
        .content {{ 
            font-size: 16px;
            color: #444;
            line-height: 1.8;
        }}
        .content p {{ 
            margin-bottom: 16px; 
            text-align: justify;
            word-wrap: break-word;
        }}
        .content h1, .content h2, .content h3, .content h4, .content h5, .content h6 {{
            color: #222;
            margin: 20px 0 10px 0;
            font-weight: 600;
        }}
        .content h2 {{ font-size: 20px; }}
        .content h3 {{ font-size: 18px; }}
        .content ul, .content ol {{
            margin: 15px 0;
            padding-left: 20px;
        }}
        .content li {{
            margin: 5px 0;
            line-height: 1.6;
        }}
        .content blockquote {{
            border-left: 4px solid #ddd;
            margin: 15px 0;
            padding: 10px 15px;
            background: #f9f9f9;
            color: #666;
        }}
        .content code {{
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 14px;
        }}
        .content pre {{
            background: #f8f8f8;
            border: 1px solid #e1e1e1;
            border-radius: 4px;
            padding: 12px;
            overflow: auto;
            margin: 15px 0;
            font-size: 14px;
        }}
        .content pre code {{
            background: none;
            padding: 0;
        }}
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #fff; 
            color: #111; 
            font-family: '微软雅黑', Arial, sans-serif; 
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 550px; 
            margin: 0 auto; 
            background: #fff; 
            border: 2px solid #111; 
            border-radius: 12px;
            padding: 30px 25px;
            position: relative;
        }}
        h1 {{ 
            color: #111; 
            font-size: 22px; 
            font-weight: bold;
            border-bottom: 2px solid #111; 
            padding-bottom: 8px; 
            margin-bottom: 15px; 
        }}
        .desc {{ 
            color: #444; 
            font-size: 15px; 
            margin-bottom: 20px; 
            border-left: 4px solid #111; 
            padding-left: 15px; 
        }}
        .content p {{ 
            margin-bottom: 15px; 
            line-height: 1.8; 
            font-size: 16px; 
            border-bottom: 1px solid #eee; 
            padding-bottom: 8px;
        }}
        </style></head><body>
        <div class="container">
          {badge}
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
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #f6f7fb; 
            color: #222; 
            font-family: '微软雅黑', Arial, sans-serif; 
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fff; 
            border-radius: 15px; 
            padding: 35px 25px;
            position: relative;
            border: 1px solid #e0e0e0;
        }}
        h1 {{ 
            color: #d32f2f; 
            font-size: 24px; 
            margin-bottom: 12px; 
            font-weight: bold;
        }}
        .desc {{ 
            background: #ffeaea; 
            color: #d32f2f; 
            font-size: 15px; 
            border-radius: 6px; 
            padding: 12px 15px; 
            margin-bottom: 20px; 
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.7; 
            font-size: 16px; 
            border-bottom: 1px solid #f3cfcf; 
            padding-bottom: 8px; 
        }}
        </style></head><body>
        <div class="container">
          {badge}
          <h1>{title}</h1>
          <div class="desc">{desc}</div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    elif style_type == 'simple':
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #fff8f0; 
            color: #333; 
            font-family: '微软雅黑', Arial, sans-serif; 
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 550px; 
            margin: 0 auto; 
            background: #fff; 
            border-radius: 10px; 
            padding: 30px 25px;
            position: relative;
            border: 1px solid #e1cad2;
        }}
        h1 {{ 
            color: #e57373; 
            font-size: 22px; 
            text-align: center; 
            margin-bottom: 15px; 
        }}
        .desc {{ 
            color: #ba68c8; 
            font-size: 15px; 
            margin-bottom: 20px; 
            text-align: center; 
        }}
        .content p {{ 
            margin: 15px 0; 
            line-height: 1.6; 
            font-size: 16px; 
        }}
        </style></head><body>
        <div class="container">
          {badge}
          <h1>{title}</h1>
          <div class="desc">{desc}</div>
          <div class="content">
            {paragraphs}
          </div>
        </div>
        </body></html>
        '''
    else:
        # 对于其他模板，使用简化的clean模板
        return render_article_html(title, content, desc, style_type='clean', is_html=is_html, highlight=highlight, highlight_theme=highlight_theme, badge_text=badge_text)
    
    return html 