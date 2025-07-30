from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
import markdown
import json
import datetime
import uuid
import sys
import zipfile
import io
from werkzeug.utils import secure_filename

# 添加xhs-tools目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'xhs-tools'))

try:
    from parser import parse_article_from_url
    from nlp_gen import generate_title, generate_desc
    from html_render import render_article_html
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保xhs-tools目录中的模块文件存在")

import base64
from io import BytesIO
from PIL import Image
import re

# 尝试导入html2image用于HTML转图片
try:
    from html2image import Html2Image
    HTML2IMAGE_AVAILABLE = True
except ImportError:
    print("html2image未安装，将使用备用方案。可运行: pip install html2image")
    HTML2IMAGE_AVAILABLE = False

app = Flask(__name__)
# app.secret_key = 'xhs-content-generator-2024' # 移除 session 相关代码
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
# app.config['SESSION_TYPE'] = 'filesystem' # 移除 session 相关代码
# app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), 'session_files') # 移除 session 相关代码
# os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True) # 移除 session 相关代码
# Session(app) # 移除 session 相关代码

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
os.makedirs('web_history', exist_ok=True)

STYLE_MAP = {
    '纯白极简': 'clean',
    '极简黑白': 'minimal', 
    '杂志卡片': 'card',
    '简约清新风': 'simple',
    '梦幻渐变': 'gradient',
    '清新自然': 'fresh',
    '暗黑科技': 'darktech',
    '卡哇伊风格': 'kawaii',
    'emoji风': 'emoji',
    '马卡龙风': 'macaron',
    '贴纸风': 'sticker',
    '复古学习感': 'retro',
    '苹果备忘录': 'apple',
    '奶油胶风': 'cream',
}

def split_markdown_blocks(content, n):
    """优化的markdown内容分割函数"""
    blocks = []
    lines = content.split('\n')
    buf = []
    in_code = False
    code_lang = ''
    
    for line in lines:
        if line.strip().startswith('```'):
            if not in_code:
                if buf:
                    blocks.append({'type': 'text', 'content': '\n'.join(buf)})
                    buf = []
                in_code = True
                code_lang = line.strip()[3:].strip()
                buf = [line]
            else:
                buf.append(line)
                blocks.append({'type': 'code', 'content': '\n'.join(buf), 'lang': code_lang})
                buf = []
                in_code = False
                code_lang = ''
        else:
            buf.append(line)
    
    if buf:
        blocks.append({'type': 'code' if in_code else 'text', 'content': '\n'.join(buf), 'lang': code_lang})
    
    # 优化分割逻辑，确保 n 个非空块如果可能
    total_len = sum(len(b['content']) for b in blocks)
    if total_len == 0:
        return [[] for _ in range(n)]
    
    avg_len = total_len // n
    avg_len = max(avg_len, 1)  # 至少1字符
    
    # 优化 split_markdown_blocks
    # 先按平均长度分割
    result = []
    cur = []
    cur_len = 0
    for b in blocks:
        block_len = len(b['content'])
        if cur_len >= avg_len and len(result) < n-1:
            result.append(cur)
            print(f"[DEBUG] 分块 {len(result)}: 长度 {cur_len}, 摘要: {''.join([b['content'][:20] for b in cur])}...")
            cur = []
            cur_len = 0
        cur.append(b)
        cur_len += block_len
    if cur:
        result.append(cur)
        print(f"[DEBUG] 分块 {len(result)}: 长度 {cur_len}, 摘要: {''.join([b['content'][:20] for b in cur])}...")
    
    # 如果少于 n，尝试从现有块中拆分
    while len(result) < n and len(result) > 0:
        # 取最后一个块拆分
        last = result.pop()
        mid = len(last) // 2
        if mid > 0:
            result.append(last[:mid])
            result.append(last[mid:])
        else:
            result.append(last)
            result.append([])  # 添加空块
        print(f"[DEBUG] 拆分后块数: {len(result)}")
    
    # 如果还是少，添加空块
    while len(result) < n:
        result.append([])
    
    # 如果多，合并
    if len(result) > n:
        last_group = []
        for group in result[n-1:]:
            last_group.extend(group)
        result = result[:n-1] + [last_group]
        print(f"[DEBUG] 合并后最后一个块长度: {sum(len(b['content']) for b in last_group)}")
    
    # 打印最终块
    for i, group in enumerate(result):
        group_content = '\n'.join([b['content'] for b in group])
        print(f"[DEBUG] 最终块 {i+1}: 长度 {len(group_content)}, 摘要: {group_content[:50]}...")
    
    return result

def smart_split_text_content(content, target_count):
    """智能文本内容分割"""
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    if not lines:
        return [''] * target_count
    
    total_chars = sum(len(line) for line in lines)
    target_chars_per_group = max(total_chars // target_count, 50)
    
    groups = []
    current_group = []
    current_chars = 0
    
    for line in lines:
        line_chars = len(line)
        if current_group and (current_chars + line_chars > target_chars_per_group * 1.3) and len(groups) < target_count - 1:
            groups.append('\n'.join(current_group))
            print(f"[DEBUG] 文本分块 {len(groups)}: 长度 {current_chars}, 摘要: {groups[-1][:50]}...")
            current_group = []
            current_chars = 0
        current_group.append(line)
        current_chars += line_chars
    
    if current_group:
        groups.append('\n'.join(current_group))
        print(f"[DEBUG] 文本分块 {len(groups)}: 长度 {current_chars}, 摘要: {groups[-1][:50]}...")
    
    # 如果少于 target_count，尝试拆分
    while len(groups) < target_count and len(groups) > 0:
        last = groups.pop()
        lines_last = last.split('\n')
        mid = len(lines_last) // 2
        if mid > 0:
            groups.append('\n'.join(lines_last[:mid]))
            groups.append('\n'.join(lines_last[mid:]))
        else:
            groups.append(last)
            groups.append('')
        print(f"[DEBUG] 文本拆分后块数: {len(groups)}")
    
    while len(groups) < target_count:
        groups.append('')
    
    if len(groups) > target_count:
        last_content = '\n'.join(groups[target_count-1:])
        groups = groups[:target_count-1] + [last_content]
    
    # 打印最终文本块
    for i, g in enumerate(groups):
        print(f"[DEBUG] 最终文本块 {i+1}: 长度 {len(g)}, 摘要: {g[:50]}...")
    
    return groups

def html_to_image(html_content, width=600, height=800):
    """将HTML转换为图片 - 优化版本"""
    filename = f'img_{uuid.uuid4().hex}.png'
    image_path = os.path.join(app.config['TEMP_FOLDER'], filename)
    
    try:
        print(f"[DEBUG] 开始生成图片: {filename}")
        print(f"[DEBUG] HTML内容长度: {len(html_content)} 字符")
        print(f"[DEBUG] 目标尺寸: {width}x{height}")
        
        if HTML2IMAGE_AVAILABLE:
            # 使用html2image生成图片
            from html2image import Html2Image
            
            # 创建Html2Image实例，增加更多配置选项
            # 修改 Html2Image 初始化，尝试多个路径
            # 使用 Edge 路径
            edge_paths = [
                'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
                'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
                'C:\\Users\\%USERNAME%\\AppData\\Local\\Microsoft\\Edge\\Application\\msedge.exe'
            ]
            success = False
            for path in edge_paths:
                try:
                    print(f"[DEBUG] 尝试 Edge 路径: {path}")
                    hti = Html2Image(
                        size=(width, height),
                        output_path=app.config['TEMP_FOLDER'],
                        browser='edge',
                        browser_executable=path
                    )
                    # 测试截图
                    result = hti.screenshot(
                        html_str=html_content,
                        save_as=filename,
                        size=(width, height)
                    )
                    if os.path.exists(image_path) and os.path.getsize(image_path) > 0:
                        print(f"[DEBUG] 使用路径 {path} 生成成功")
                        success = True
                        break
                except Exception as path_error:
                    print(f"[WARNING] 路径 {path} 失败: {str(path_error)}")
                    continue
            
            if success:
                return image_path
            else:
                print(f"[ERROR] 所有 Edge 路径都失败，使用 PIL 备用")
                raise Exception("所有路径失败")
                
        else:
            print(f"[DEBUG] html2image不可用，使用PIL备用方案")
            raise Exception("html2image不可用")
            
    except Exception as e:
        print(f"[ERROR] 图片生成失败: {str(e)}")
        
        # 备用方案：使用PIL创建简单图片
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 优化 PIL 备用方案：添加更多文本和样式
            # 创建白色背景图片
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # 尝试添加文本内容（简化版）
            try:
                # 从HTML中提取文本内容
                import re
                text_content = re.sub(r'<[^>]+>', '', html_content)
                text_content = text_content.strip()[:500]  # 扩展长度
                
                # 加载字体（如果可用）
                try:
                    font = ImageFont.truetype('arial.ttf', 20)  # 假设系统有 arial
                except:
                    font = ImageFont.load_default()
                
                # 绘制标题
                draw.text((20, 20), title or "小红书图片", fill='black', font=font)
                
                # 绘制内容
                y_pos = 60
                lines = text_content.split('\n')
                for line in lines[:30]:  # 最多30行
                    if line.strip():
                        draw.text((20, y_pos), line.strip()[:50], fill='#333333', font=font)
                        y_pos += 30
                
                # 添加边框
                draw.rectangle([(10,10), (width-10, height-10)], outline='black', width=2)
                
            except Exception as text_error:
                print(f"[WARNING] 文本绘制失败: {text_error}")
                draw.text((20, 20), "图片生成中...", fill='black')
            
            # 保存图片
            img.save(image_path, 'PNG', quality=95)
            print(f"[DEBUG] PIL备用图片生成成功: {image_path}")
            return image_path
            
        except Exception as pil_error:
            print(f"[ERROR] PIL备用方案也失败: {pil_error}")
            
            # 最后备用方案：创建纯色图片
            try:
                img = Image.new('RGB', (width, height), color='#f0f0f0')
                img.save(image_path, 'PNG')
                print(f"[DEBUG] 纯色图片生成成功: {image_path}")
                return image_path
            except Exception as final_error:
                print(f"[FATAL] 所有图片生成方案都失败: {final_error}")
                return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/parse_url', methods=['POST'])
def parse_url():
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': '请输入有效的URL'}), 400
        
        title, content = parse_article_from_url(url)
        xhs_title = generate_title(title, content)
        xhs_desc = generate_desc(content)
        
        return jsonify({
            'success': True,
            'title': xhs_title,
            'description': xhs_desc,
            'content': content,
            'is_markdown': False
        })
    
    except Exception as e:
        return jsonify({'error': f'解析失败: {str(e)}'}), 500

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if file and file.filename.lower().endswith(('.md', '.txt', '.html')):
            filename = secure_filename(file.filename)
            content = file.read().decode('utf-8')
            
            title = os.path.splitext(filename)[0]
            xhs_title = generate_title(title, content)
            xhs_desc = generate_desc(content)
            is_md = filename.lower().endswith('.md')
            
            return jsonify({
                'success': True,
                'title': xhs_title,
                'description': xhs_desc,
                'content': content,
                'is_markdown': is_md
            })
        else:
            return jsonify({'error': '不支持的文件格式，请上传 .md、.txt 或 .html 文件'}), 400
    
    except Exception as e:
        return jsonify({'error': f'文件处理失败: {str(e)}'}), 500

@app.route('/api/generate_images', methods=['POST'])
def generate_images():
    """生成预览图片 - 优化版本"""
    print(f"[API] 收到图片生成请求")
    
    try:
        data = request.json
        print(f"[API] 请求数据键: {list(data.keys()) if data else 'None'}")
        
        content = data.get('content')
        title = data.get('title')
        description = data.get('description')
        style_type = data.get('style', 'clean')
        split_count = int(data.get('split_count', 3))
        is_markdown = data.get('is_markdown')
        highlight_theme = data.get('highlight_theme', 'github')
        
        print(f"[API] 参数 - 内容长度: {len(content)}, 标题: {title[:20]}..., 样式: {style_type}, 分割数: {split_count}, Markdown: {is_markdown}")
        
        if not content:
            print(f"[ERROR] 内容为空")
            return jsonify({'error': '没有内容可处理'}), 400
        
        # 分割内容
        print(f"[API] 开始分割内容，模式: {'Markdown' if is_markdown else '纯文本'}")
        
        if is_markdown:
            groups = split_markdown_blocks(content, split_count)
            md_blocks = ['\n'.join([b['content'] for b in group]) for group in groups]
        else:
            md_blocks = smart_split_text_content(content, split_count)
        
        print(f"[API] 内容分割完成，生成 {len(md_blocks)} 个片段")
        
        # 生成HTML预览
        html_previews = []
        for i, md in enumerate(md_blocks):
            if not md.strip():
                print(f"[WARNING] 第{i+1}个片段为空，跳过")
                continue
                
            print(f"[API] 生成第{i+1}个片段的HTML，长度: {len(md)} 字符")
            
            if is_markdown:
                html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
                html = render_article_html(
                    title, html_content, description if i == 0 else '',
                    style_type, is_html=True, highlight=True, highlight_theme=highlight_theme
                )
            else:
                html = render_article_html(
                    title, md, description if i == 0 else '',
                    style_type, highlight=True, highlight_theme=highlight_theme
                )
            
            html_previews.append({
                'index': i + 1,
                'html': html,
                'content': md,
                'word_count': len(md),
                'summary': md.strip().replace('\n', ' ')[:50] + ('...' if len(md.strip()) > 50 else '')
            })
        
        print(f"[API] HTML生成完成，共 {len(html_previews)} 个有效预览")
        
        print(f"[API] 返回预览数据")
        
        return jsonify({
            'success': True,
            'previews': html_previews,
            'total_count': len(html_previews)
        })
    
    except Exception as e:
        print(f"[ERROR] 生成预览异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'生成预览失败: {str(e)}'}), 500

@app.route('/api/download_single', methods=['POST'])
def download_single():
    """下载单张图片 - 独立版本，不依赖session"""
    print(f"[API] 开始处理单张下载请求 - 独立版本")
    
    try:
        data = request.json
        if not data:
            print(f"[ERROR] 请求数据为空")
            return jsonify({'error': '请求数据为空'}), 400
        
        content = data.get('content', '').strip()
        title = data.get('title', '')
        description = data.get('description', '')
        style_type = data.get('style', 'clean')
        split_count = int(data.get('split_count', 1))  # 默认1张
        index = int(data.get('index', 0))  # 0-based index
        is_markdown = data.get('is_markdown', False)
        highlight_theme = data.get('highlight_theme', 'github')
        
        print(f"[API] 参数 - 内容长度: {len(content)}, 标题: {title[:20]}..., 样式: {style_type}, 分割数: {split_count}, 索引: {index}, Markdown: {is_markdown}")
        
        if not content:
            print(f"[ERROR] 内容为空")
            return jsonify({'error': '没有内容可处理'}), 400
        
        if index < 0:
            print(f"[ERROR] 无效索引")
            return jsonify({'error': '无效的图片索引'}), 400
        
        # 分割内容
        print(f"[API] 开始分割内容，模式: {'Markdown' if is_markdown else '纯文本'}")
        
        if is_markdown:
            groups = split_markdown_blocks(content, split_count)
            md_blocks = ['\n'.join([b['content'] for b in group]) for group in groups]
        else:
            md_blocks = smart_split_text_content(content, split_count)
        
        print(f"[API] 内容分割完成，生成 {len(md_blocks)} 个片段")
        
        if index >= len(md_blocks):
            print(f"[ERROR] 索引超出范围: {index} >= {len(md_blocks)}")
            return jsonify({'error': '图片索引超出范围'}), 400
        
        md = md_blocks[index]
        print(f"[DEBUG] 下载索引 {index} (第 {index+1} 张), 内容摘要: {md[:100]}...")
        if not md.strip():
            print(f"[WARNING] 指定片段为空")
            return jsonify({'error': '指定内容为空'}), 400
        
        print(f"[API] 生成HTML，长度: {len(md)} 字符")
        
        if is_markdown:
            html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
            html = render_article_html(
                title, html_content, description,
                style_type, is_html=True, highlight=True, highlight_theme=highlight_theme
            )
        else:
            html = render_article_html(
                title, md, description,
                style_type, highlight=True, highlight_theme=highlight_theme
            )
        
        # 计算图片尺寸
        content_length = len(html)
        if content_length > 2000:
            width, height = 600, 1200
        elif content_length > 1000:
            width, height = 600, 900
        else:
            width, height = 600, 600
        
        # 生成图片
        image_path = html_to_image(html, width, height)
        
        if not image_path or not os.path.exists(image_path):
            print(f"[ERROR] 图片生成失败，路径: {image_path}")
            return jsonify({'error': '图片生成失败，请稍后重试'}), 500
        
        file_size = os.path.getsize(image_path)
        print(f"[API] 图片生成成功，路径: {image_path}，大小: {file_size} bytes")
        
        # 生成安全的下载文件名
        safe_title = re.sub(r'[^\w\u4e00-\u9fff\-_]+', '_', title)[:50]
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{safe_title}_{index + 1}_{timestamp}.png'
        
        print(f"[API] 准备发送文件，文件名: {filename}")
        
        # 发送文件前检查
        if not os.path.exists(image_path):
            print(f"[ERROR] 发送前文件丢失: {image_path}")
            return jsonify({'error': '文件生成后丢失'}), 500
        
        # 发送文件
        response = send_file(
            image_path,
            as_attachment=True,
            download_name=filename,
            mimetype='image/png'
        )
        
        # 设置清理回调
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"[DEBUG] 清理临时文件: {image_path}")
            except Exception as e:
                print(f"[WARNING] 清理文件失败: {e}")
        
        print(f"[API] 文件发送成功: {filename}")
        return response
    
    except Exception as e:
        print(f"[ERROR] 单张下载API异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'下载失败: {str(e)}'}), 500

@app.route('/api/export_images', methods=['POST'])
def export_images():
    """批量导出所有图片为ZIP文件 - 独立版本，不依赖 session"""
    print(f"[API] 开始处理批量导出请求 - 独立版本")
    
    try:
        data = request.json
        if not data:
            print(f"[ERROR] 请求数据为空")
            return jsonify({'error': '请求数据为空'}), 400
        
        content = data.get('content', '').strip()
        title = data.get('title', '')
        description = data.get('description', '')
        style_type = data.get('style', 'clean')
        split_count = int(data.get('split_count', 3))
        is_markdown = data.get('is_markdown', False)
        highlight_theme = data.get('highlight_theme', 'github')
        
        print(f"[API] 参数 - 内容长度: {len(content)}, 标题: {title[:20]}..., 样式: {style_type}, 分割数: {split_count}, Markdown: {is_markdown}")
        
        if not content:
            print(f"[ERROR] 内容为空")
            return jsonify({'error': '没有内容可处理'}), 400
        
        # 分割内容
        print(f"[API] 开始分割内容，模式: {'Markdown' if is_markdown else '纯文本'}")
        
        if is_markdown:
            groups = split_markdown_blocks(content, split_count)
            md_blocks = ['\n'.join([b['content'] for b in group]) for group in groups]
        else:
            md_blocks = smart_split_text_content(content, split_count)
        
        print(f"[DEBUG] 分割结果: {len(md_blocks)} 个块")
        for j, block in enumerate(md_blocks):
            print(f"[DEBUG] 块 {j}: 长度 {len(block)}, 摘要: {block[:50]}...")
        
        print(f"[API] 内容分割完成，生成 {len(md_blocks)} 个片段")
        
        # 生成HTML
        html_previews = []
        for i, md in enumerate(md_blocks):
            print(f"[DEBUG] 批量处理第 {i+1} 张, 内容摘要: {md[:100]}...")
            if not md.strip():
                print(f"[WARNING] 第{i+1}个片段为空，跳过")
                continue
                
            print(f"[API] 生成第{i+1}个片段的HTML，长度: {len(md)} 字符")
            
            if is_markdown:
                html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
                html = render_article_html(
                    title, html_content, description if i == 0 else '',
                    style_type, is_html=True, highlight=True, highlight_theme=highlight_theme
                )
            else:
                html = render_article_html(
                    title, md, description if i == 0 else '',
                    style_type, highlight=True, highlight_theme=highlight_theme
                )
            
            html_previews.append(html)
        
        print(f"[API] HTML生成完成，共 {len(html_previews)} 个")
        
        # 生成安全的文件名
        safe_title = re.sub(r'[^\w\u4e00-\u9fff\-_]+', '_', title)[:30]
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 创建内存中的ZIP文件
        memory_file = io.BytesIO()
        successful_images = 0
        failed_images = 0
        
        print(f"[API] 开始生成{len(html_previews)}张图片")
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for i, html_content in enumerate(html_previews):
                try:
                    print(f"[API] 处理第{i+1}张图片")
                    
                    if not html_content:
                        print(f"[WARNING] 第{i+1}张图片HTML内容为空，跳过")
                        failed_images += 1
                        continue
                    
                    # 计算合适的图片尺寸
                    content_length = len(html_content)
                    if content_length > 2000:
                        width, height = 600, 1200
                    elif content_length > 1000:
                        width, height = 600, 900
                    else:
                        width, height = 600, 600
                    
                    # 生成图片
                    image_path = html_to_image(html_content, width, height)
                    
                    if image_path and os.path.exists(image_path):
                        file_size = os.path.getsize(image_path)
                        print(f"[API] 第{i+1}张图片生成成功，大小: {file_size} bytes")
                        
                        # 添加到ZIP文件
                        image_filename = f'{safe_title}_{i + 1:02d}.png'
                        zf.write(image_path, image_filename)
                        successful_images += 1
                        
                        # 清理临时文件
                        try:
                            os.remove(image_path)
                            print(f"[DEBUG] 清理临时文件: {image_path}")
                        except Exception as cleanup_error:
                            print(f"[WARNING] 清理文件失败: {cleanup_error}")
                    else:
                        print(f"[WARNING] 第{i+1}张图片生成失败")
                        failed_images += 1
                        
                except Exception as img_error:
                    print(f"[ERROR] 处理第{i+1}张图片时出错: {img_error}")
                    failed_images += 1
                    continue
            
            # 添加导出信息文件
            export_info = f"""小红书图片导出信息

标题: {title}
导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
成功生成: {successful_images} 张
失败图片: {failed_images} 张
总计: {len(html_previews)} 张

感谢使用小红书内容生成工具！
"""
            zf.writestr('导出信息.txt', export_info.encode('utf-8'))
        
        print(f"[API] ZIP文件生成完成，成功: {successful_images}，失败: {failed_images}")
        
        if successful_images == 0:
            return jsonify({'error': '所有图片生成都失败了，请检查内容格式'}), 500
        
        # 检查ZIP文件大小
        memory_file.seek(0)
        zip_size = len(memory_file.getvalue())
        print(f"[API] ZIP文件大小: {zip_size} bytes")
        
        if zip_size == 0:
            return jsonify({'error': 'ZIP文件生成失败'}), 500
        
        # 重置文件指针
        memory_file.seek(0)
        
        # 生成下载文件名
        zip_filename = f'{safe_title}_小红书图片_{timestamp}.zip'
        
        print(f"[API] 准备发送ZIP文件: {zip_filename}")
        
        # 创建response
        response = send_file(
            memory_file,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
        print(f"[API] ZIP文件发送成功")
        return response
    
    except Exception as e:
        print(f"[ERROR] 批量导出API异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'批量导出失败: {str(e)}'}), 500

@app.route('/api/export_text')
def export_text():
    """导出所有文案内容"""
    try:
        # 移除 session 相关代码
        # previews = session.get('current_previews', [])
        # if not previews:
        #     return jsonify({'error': '没有可导出的内容'}), 400
        
        # title = session.get('current_title', '小红书内容')
        # description = session.get('current_desc', '')
        
        # 生成文本文件内容
        text_content = f"标题：{title}\n\n"
        text_content += f"描述：{description}\n\n"
        text_content += "=" * 50 + "\n\n"
        
        # for i, preview in enumerate(previews):
        #     text_content += f"第 {i + 1} 张内容：\n"
        #     text_content += "-" * 30 + "\n"
        #     text_content += preview['content'] + "\n\n"
        
        # 创建临时文件
        temp_file = io.BytesIO(text_content.encode('utf-8'))
        
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]+', '_', title)
        filename = f'{safe_title}_文案.txt'
        
        return send_file(
            temp_file,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    
    except Exception as e:
        return jsonify({'error': f'导出文案失败: {str(e)}'}), 500

@app.route('/api/smart_split', methods=['POST'])
def smart_split():
    try:
        data = request.json
        # 移除 session 相关代码
        # content = data.get('content') or session.get('last_content', '')
        content = data.get('content')
        is_markdown = data.get('is_markdown')
        
        if not content:
            return jsonify({'error': '没有内容可分析'}), 400
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        total_chars = sum(len(line) for line in lines)
        
        # 智能分割算法
        n_by_length = max(1, total_chars // 800)
        n_by_lines = max(1, len(lines) // 15)
        n_by_structure = 1
        
        if is_markdown:
            n_title = sum(1 for l in lines if l.startswith('#'))
            n_code = sum(1 for l in lines if l.startswith('```'))
            n_by_structure = max(n_title, n_code // 2, 1)
        
        recommended_count = min(max(n_by_length, n_by_lines, n_by_structure), 12)
        recommended_count = max(recommended_count, 1)
        
        return jsonify({
            'success': True,
            'recommended_count': recommended_count,
            'analysis': {
                'total_chars': total_chars,
                'total_lines': len(lines),
                'by_length': n_by_length,
                'by_lines': n_by_lines,
                'by_structure': n_by_structure
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'智能分析失败: {str(e)}'}), 500

@app.route('/api/save_history', methods=['POST'])
def save_history():
    try:
        data = request.json
        
        history_data = {
            'id': str(uuid.uuid4()),
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'content': data.get('content', ''),
            'style': data.get('style', 'clean'),
            'split_count': data.get('split_count', 1),
            'is_markdown': data.get('is_markdown', False),
            'created_at': datetime.datetime.now().isoformat(),
            'previews_count': 0 # 移除 session 相关代码
        }
        
        filename = f"web_history/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{history_data['title'][:10]}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'history_id': history_data['id']})
    
    except Exception as e:
        return jsonify({'error': f'保存失败: {str(e)}'}), 500

@app.route('/api/get_history', methods=['GET'])
def get_history():
    try:
        history_files = []
        if os.path.exists('web_history'):
            files = [f for f in os.listdir('web_history') if f.endswith('.json')]
            files.sort(reverse=True)  # 最新的在前
            
            for file in files[:20]:  # 只返回最近20条
                try:
                    with open(f'web_history/{file}', 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        history_files.append(data)
                except Exception:
                    continue
        
        return jsonify({'success': True, 'history': history_files})
    
    except Exception as e:
        return jsonify({'error': f'获取历史记录失败: {str(e)}'}), 500

# 清理临时文件的定时任务
@app.before_request
def cleanup_temp_files():
    """清理超过1小时的临时文件"""
    try:
        temp_folder = app.config['TEMP_FOLDER']
        if os.path.exists(temp_folder):
            current_time = datetime.datetime.now()
            for filename in os.listdir(temp_folder):
                file_path = os.path.join(temp_folder, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                    if (current_time - file_time).total_seconds() > 3600:  # 1小时
                        try:
                            os.remove(file_path)
                        except:
                            pass
    except:
        pass

# 移除 /api/debug/session 等调试接口如果不需要

# 新增独立的导出图片接口
@app.route('/api/export_images_independent', methods=['POST'])
def export_images_independent():
    """独立的批量导出图片接口，不依赖session"""
    print(f"[API] 开始处理独立批量导出请求")
    
    try:
        data = request.json
        if not data:
            print(f"[ERROR] 请求数据为空")
            return jsonify({'error': '请求数据为空'}), 400
        
        content = data.get('content', '').strip()
        title = data.get('title', '')
        description = data.get('description', '')
        style_type = data.get('style', 'clean')
        split_count = int(data.get('split_count', 3))
        is_markdown = data.get('is_markdown', False)
        highlight_theme = data.get('highlight_theme', 'github')
        
        print(f"[API] 参数 - 内容长度: {len(content)}, 标题: {title[:20]}..., 样式: {style_type}, 分割数: {split_count}, Markdown: {is_markdown}")
        
        if not content:
            print(f"[ERROR] 内容为空")
            return jsonify({'error': '没有内容可处理'}), 400
        
        # 分割内容
        print(f"[API] 开始分割内容，模式: {'Markdown' if is_markdown else '纯文本'}")
        
        if is_markdown:
            groups = split_markdown_blocks(content, split_count)
            md_blocks = ['\n'.join([b['content'] for b in group]) for group in groups]
        else:
            md_blocks = smart_split_text_content(content, split_count)
        
        print(f"[API] 内容分割完成，生成 {len(md_blocks)} 个片段")
        
        # 生成HTML
        html_previews = []
        for i, md in enumerate(md_blocks):
            if not md.strip():
                print(f"[WARNING] 第{i+1}个片段为空，跳过")
                continue
                
            print(f"[API] 生成第{i+1}个片段的HTML，长度: {len(md)} 字符")
            
            if is_markdown:
                html_content = markdown.markdown(md, extensions=['extra', 'codehilite'])
                html = render_article_html(
                    title, html_content, description if i == 0 else '',
                    style_type, is_html=True, highlight=True, highlight_theme=highlight_theme
                )
            else:
                html = render_article_html(
                    title, md, description if i == 0 else '',
                    style_type, highlight=True, highlight_theme=highlight_theme
                )
            
            html_previews.append(html)
        
        print(f"[API] HTML生成完成，共 {len(html_previews)} 个")
        
        # 生成安全的文件名
        safe_title = re.sub(r'[^\w\u4e00-\u9fff\-_]+', '_', title)[:30]
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 创建内存中的ZIP文件
        memory_file = io.BytesIO()
        successful_images = 0
        failed_images = 0
        
        print(f"[API] 开始生成{len(html_previews)}张图片")
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for i, html_content in enumerate(html_previews):
                try:
                    print(f"[API] 处理第{i+1}张图片")
                    
                    if not html_content:
                        print(f"[WARNING] 第{i+1}张图片HTML内容为空，跳过")
                        failed_images += 1
                        continue
                    
                    # 计算合适的图片尺寸
                    content_length = len(html_content)
                    if content_length > 2000:
                        width, height = 600, 1200
                    elif content_length > 1000:
                        width, height = 600, 900
                    else:
                        width, height = 600, 600
                    
                    # 生成图片
                    image_path = html_to_image(html_content, width, height)
                    
                    if image_path and os.path.exists(image_path):
                        file_size = os.path.getsize(image_path)
                        print(f"[API] 第{i+1}张图片生成成功，大小: {file_size} bytes")
                        
                        # 添加到ZIP文件
                        image_filename = f'{safe_title}_{i + 1:02d}.png'
                        zf.write(image_path, image_filename)
                        successful_images += 1
                        
                        # 清理临时文件
                        try:
                            os.remove(image_path)
                            print(f"[DEBUG] 清理临时文件: {image_path}")
                        except Exception as cleanup_error:
                            print(f"[WARNING] 清理文件失败: {cleanup_error}")
                    else:
                        print(f"[WARNING] 第{i+1}张图片生成失败")
                        failed_images += 1
                        
                except Exception as img_error:
                    print(f"[ERROR] 处理第{i+1}张图片时出错: {img_error}")
                    failed_images += 1
                    continue
            
            # 添加导出信息文件
            export_info = f"""小红书图片导出信息

标题: {title}
导出时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
成功生成: {successful_images} 张
失败图片: {failed_images} 张
总计: {len(html_previews)} 张

感谢使用小红书内容生成工具！
"""
            zf.writestr('导出信息.txt', export_info.encode('utf-8'))
        
        print(f"[API] ZIP文件生成完成，成功: {successful_images}，失败: {failed_images}")
        
        if successful_images == 0:
            return jsonify({'error': '所有图片生成都失败了，请检查内容格式'}), 500
        
        # 检查ZIP文件大小
        memory_file.seek(0)
        zip_size = len(memory_file.getvalue())
        print(f"[API] ZIP文件大小: {zip_size} bytes")
        
        if zip_size == 0:
            return jsonify({'error': 'ZIP文件生成失败'}), 500
        
        # 重置文件指针
        memory_file.seek(0)
        
        # 生成下载文件名
        zip_filename = f'{safe_title}_小红书图片_{timestamp}.zip'
        
        print(f"[API] 准备发送ZIP文件: {zip_filename}")
        
        # 创建response
        response = send_file(
            memory_file,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
        print(f"[API] ZIP文件发送成功")
        return response
    
    except Exception as e:
        print(f"[ERROR] 独立批量导出API异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'批量导出失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 