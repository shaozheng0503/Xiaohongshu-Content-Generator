def generate_title(title, content):
    # 智能生成标题：优先用原文标题，若内容有明显小节或首行可用，则自动提炼，否则截取前30字
    if title and title.strip():
        return title.strip()[:30]
    # 若内容首行有#或明显标题
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    for l in lines:
        if l.startswith('#'):
            return l.lstrip('#').strip()[:30]
    if lines:
        return lines[0][:30]
    return '小红书内容'  # 兜底

def generate_desc(content):
    desc = content.strip().replace('\n', '')[:100]
    return desc + '\n#内容干货 #小红书推荐\n关注我获取更多优质内容！' 