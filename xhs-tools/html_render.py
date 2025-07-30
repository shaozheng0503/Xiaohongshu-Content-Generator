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
    elif style_type == 'darktech':
        badge = f"<div style='position:absolute;top:10px;right:18px;background:#00ff88;color:#000;padding:4px 12px;border-radius:8px;font-size:12px;font-weight:bold;'>{badge_text}</div>"
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
        # 纯白底极简模板 - 专为长文设计
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
        # 极简黑白 - 经典简约
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #fff; 
            color: #111; 
            {font_family}
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
        # 杂志卡片 - 小红书经典风格
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #f6f7fb; 
            color: #222; 
            {font_family}
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
    elif style_type == 'gradient':
        # 梦幻渐变 - 彩虹渐变效果
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: #fff; 
            {font_family}
            padding: 40px 30px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.95); 
            border-radius: 20px; 
            padding: 35px 25px;
            position: relative;
            color: #333;
        }}
        h1 {{ 
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 26px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
        }}
        .desc {{ 
            background: linear-gradient(45deg, #f093fb, #f5576c);
            color: #fff;
            font-size: 15px; 
            border-radius: 12px; 
            padding: 15px 18px; 
            margin-bottom: 25px; 
            text-align: center;
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 12px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
            margin-bottom: 12px;
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
    elif style_type == 'fresh':
        # 清新自然 - 绿色自然风
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
            color: #2c3e50; 
            {font_family}
            padding: 40px 30px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: rgba(255,255,255,0.9); 
            border-radius: 18px; 
            padding: 35px 25px;
            position: relative;
            border: 2px solid #4dd0e1;
        }}
        h1 {{ 
            color: #00695c; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
            border-bottom: 3px solid #4dd0e1;
            padding-bottom: 10px;
        }}
        .desc {{ 
            background: #e0f7fa;
            color: #00695c;
            font-size: 15px; 
            border-radius: 10px; 
            padding: 15px 18px; 
            margin-bottom: 25px; 
            border-left: 4px solid #4dd0e1;
        }}
        .content p {{ 
            margin-bottom: 16px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 10px 0;
            border-bottom: 1px solid #b2dfdb;
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
    elif style_type == 'darktech':
        # 暗黑科技 - 赛博朋克风格
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%); 
            color: #00ff88; 
            {font_family}
            padding: 40px 30px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: rgba(26, 26, 46, 0.95); 
            border-radius: 15px; 
            padding: 35px 25px;
            position: relative;
            border: 2px solid #00ff88;
        }}
        h1 {{ 
            color: #00ff88; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
            text-shadow: 0 0 10px #00ff88;
        }}
        .desc {{ 
            background: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            font-size: 15px; 
            border-radius: 8px; 
            padding: 15px 18px; 
            margin-bottom: 25px; 
            border: 1px solid #00ff88;
        }}
        .content p {{ 
            margin-bottom: 16px; 
            line-height: 1.8; 
            font-size: 16px; 
            color: #e0e0e0;
            border-left: 3px solid #00ff88;
            padding-left: 15px;
            margin-bottom: 20px;
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
    elif style_type == 'kawaii':
        # 卡哇伊风格 - 可爱粉色系
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
            color: #333; 
            {font_family}
            padding: 40px 30px;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fff0fa; 
            border-radius: 25px; 
            padding: 35px 25px;
            position: relative;
            border: 3px solid #ffb6d5;
        }}
        h1 {{ 
            color: #e91e63; 
            font-size: 26px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
        }}
        .desc {{ 
            background: #ffe0f0;
            color: #e91e63;
            font-size: 16px; 
            border-radius: 15px; 
            padding: 18px 20px; 
            margin-bottom: 25px; 
            text-align: center;
            border: 2px solid #ffb6d5;
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 15px;
            background: rgba(255, 182, 213, 0.2);
            border-radius: 12px;
            margin-bottom: 15px;
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
        # 简约清新风 - 温馨粉橙色系
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #fff8f0; 
            color: #333; 
            {font_family}
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
    elif style_type == 'emoji':
        # emoji风 - 表情丰富风格
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #fffde7 0%, #fff3e0 100%); 
            color: #333; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fffef7; 
            border-radius: 20px; 
            padding: 35px 25px;
            position: relative;
            border: 3px solid #ffd54f;
        }}
        h1 {{ 
            color: #f57c00; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
        }}
        h1:before {{ 
            content: "🌟 ";
        }}
        h1:after {{ 
            content: " 🌟";
        }}
        .desc {{ 
            background: #fff8e1;
            color: #f57c00;
            font-size: 16px; 
            border-radius: 12px; 
            padding: 18px 20px; 
            margin-bottom: 25px; 
            text-align: center;
            border: 2px solid #ffd54f;
        }}
        .desc:before {{ 
            content: "✨ ";
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 12px 15px;
            background: rgba(255, 213, 79, 0.1);
            border-radius: 10px;
            margin-bottom: 15px;
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
    elif style_type == 'macaron':
        # 马卡龙风 - 柔和糖果色
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #ffe0f7 0%, #e1bee7 100%); 
            color: #333; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.9); 
            border-radius: 25px; 
            padding: 35px 25px;
            position: relative;
            border: 3px solid #a259ff;
        }}
        h1 {{ 
            color: #8e24aa; 
            font-size: 26px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
        }}
        .desc {{ 
            background: #f3e5f5;
            color: #8e24aa;
            font-size: 16px; 
            border-radius: 15px; 
            padding: 18px 20px; 
            margin-bottom: 25px; 
            text-align: center;
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 15px;
            background: linear-gradient(45deg, rgba(162, 89, 255, 0.1), rgba(225, 190, 231, 0.1));
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #a259ff;
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
    elif style_type == 'sticker':
        # 贴纸风 - 撕贴效果
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #f8fff4 0%, #e8f5e8 100%); 
            color: #333; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fff; 
            border-radius: 15px; 
            padding: 35px 25px;
            position: relative;
            border: 3px solid #43a047;
            border-style: dashed;
        }}
        h1 {{ 
            color: #2e7d32; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
            background: #e8f5e8;
            padding: 12px;
            border-radius: 10px;
        }}
        .desc {{ 
            background: #f1f8e9;
            color: #2e7d32;
            font-size: 15px; 
            border-radius: 8px; 
            padding: 15px 18px; 
            margin-bottom: 25px; 
            border: 2px solid #a5d6a7;
            border-style: dotted;
        }}
        .content p {{ 
            margin-bottom: 16px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 12px 15px;
            border: 1px solid #c8e6c9;
            border-radius: 8px;
            margin-bottom: 15px;
            background: #f9fff9;
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
    elif style_type == 'retro':
        # 复古学习感 - 复古纸张效果
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #fdf6e3 0%, #f4e8d0 100%); 
            color: #b58900; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fdf6e3; 
            border-radius: 15px; 
            padding: 35px 25px;
            position: relative;
            border: 2px dashed #b58900;
        }}
        h1 {{ 
            color: #b58900; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
            border-bottom: 2px solid #b58900;
            padding-bottom: 10px;
        }}
        .desc {{ 
            background: #f7f3e3;
            color: #b58900;
            font-size: 15px; 
            border-radius: 5px; 
            padding: 15px 18px; 
            margin-bottom: 25px; 
            border: 1px solid #d4c04a;
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            font-family: 'Courier New', monospace;
            border-bottom: 1px dotted #d4c04a;
            padding-bottom: 10px;
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
    elif style_type == 'apple':
        # 苹果备忘录 - 简洁现代风格
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: #fffbe7; 
            color: #222; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fffbe7; 
            border-radius: 15px; 
            padding: 35px 25px;
            position: relative;
            border: 2px solid #e1e1e1;
        }}
        h1 {{ 
            color: #222; 
            font-size: 24px; 
            margin-bottom: 15px; 
            font-weight: 600;
            text-align: left;
        }}
        .desc {{ 
            color: #666;
            font-size: 15px; 
            margin-bottom: 25px; 
            padding-bottom: 15px;
            border-bottom: 1px solid #e1e1e1;
        }}
        .content p {{ 
            margin-bottom: 16px; 
            line-height: 1.7; 
            font-size: 16px; 
            color: #333;
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
    elif style_type == 'cream':
        # 奶油胶风 - 温柔奶油色
        html = f'''
        <html><head>
        <meta charset="utf-8">
        {highlight_css}
        <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #fff0e6 0%, #ffe4d1 100%); 
            color: #333; 
            {font_family}
            padding: 40px 30px;
        }}
        .container {{ 
            max-width: 570px; 
            margin: 0 auto; 
            background: #fff0e6; 
            border-radius: 25px; 
            padding: 35px 25px;
            position: relative;
            border: 3px solid #ffd6b3;
        }}
        h1 {{ 
            color: #ff8c42; 
            font-size: 26px; 
            margin-bottom: 15px; 
            font-weight: bold;
            text-align: center;
        }}
        .desc {{ 
            background: #ffe9d9;
            color: #ff8c42;
            font-size: 16px; 
            border-radius: 15px; 
            padding: 18px 20px; 
            margin-bottom: 25px; 
            text-align: center;
        }}
        .content p {{ 
            margin-bottom: 18px; 
            line-height: 1.8; 
            font-size: 16px; 
            padding: 15px;
            background: rgba(255, 140, 66, 0.1);
            border-radius: 15px;
            margin-bottom: 15px;
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
        # 默认使用纯白极简模板
        return render_article_html(title, content, desc, style_type='clean', is_html=is_html, highlight=highlight, highlight_theme=highlight_theme, badge_text=badge_text)
    
    return html 