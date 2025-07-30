// 全局变量
let currentContent = '';
let currentTitle = '';
let currentDescription = '';
let isMarkdown = false;
let currentPreviews = [];
let selectedStyle = 'clean'; // 默认样式

// 样式映射
const STYLE_NAMES = {
    'clean': '纯白极简',
    'minimal': '极简黑白',
    'card': '杂志卡片',
    'simple': '简约清新风',
    'gradient': '梦幻渐变',
    'fresh': '清新自然',
    'darktech': '暗黑科技',
    'kawaii': '卡哇伊风格',
    'emoji': 'emoji风',
    'macaron': '马卡龙风',
    'sticker': '贴纸风',
    'retro': '复古学习感',
    'apple': '苹果备忘录',
    'cream': '奶油胶风'
};

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setupDragAndDrop();
    setupStyleSelection();
});

// 初始化应用
function initializeApp() {
    // 添加动画效果
    document.querySelectorAll('.hero-card, .input-card').forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 100);
    });
    
    // 初始化工具提示
    initializeTooltips();
    
    // 设置默认样式
    updateCurrentStyle('clean');
}

// 设置事件监听器
function setupEventListeners() {
    // Enter键支持
    document.getElementById('url-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            parseUrl();
        }
    });
    
    // 分割数量变化时的实时更新
    document.getElementById('split-count').addEventListener('change', function() {
        if (currentContent && currentPreviews.length > 0) {
            generatePreviews();
        }
    });
    
    // 代码高亮主题变化
    document.getElementById('highlight-theme').addEventListener('change', function() {
        if (currentContent && currentPreviews.length > 0) {
            generatePreviews();
        }
    });
}

// 设置样式选择功能
function setupStyleSelection() {
    const styleOptions = document.querySelectorAll('.style-option');
    
    styleOptions.forEach(option => {
        option.addEventListener('click', function() {
            const style = this.getAttribute('data-style');
            selectStyle(style);
        });
    });
    
    // 默认选中纯白极简
    selectStyle('clean');
}

// 选择样式
function selectStyle(style) {
    // 移除所有活动状态
    document.querySelectorAll('.style-option').forEach(option => {
        option.classList.remove('active');
    });
    
    // 添加活动状态到选中的样式
    const selectedOption = document.querySelector(`[data-style="${style}"]`);
    if (selectedOption) {
        selectedOption.classList.add('active');
    }
    
    // 更新全局变量和界面
    selectedStyle = style;
    updateCurrentStyle(style);
    
    // 如果有内容，重新生成预览
    if (currentContent && currentPreviews.length > 0) {
        generatePreviews();
    }
}

// 更新当前样式显示
function updateCurrentStyle(style) {
    const styleName = STYLE_NAMES[style] || style;
    const currentStyleInput = document.getElementById('current-style');
    if (currentStyleInput) {
        currentStyleInput.value = styleName;
    }
}

// 设置拖拽上传
function setupDragAndDrop() {
    const uploadArea = document.querySelector('.upload-area');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        uploadArea.classList.add('dragover');
    }
    
    function unhighlight() {
        uploadArea.classList.remove('dragover');
    }
    
    uploadArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    }
}

// 初始化工具提示
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 显示加载状态
function showLoading(message = '正在处理中，请稍候...') {
    const overlay = document.getElementById('loading-overlay');
    const content = overlay.querySelector('.loading-content p');
    content.textContent = message;
    overlay.style.display = 'flex';
}

// 隐藏加载状态
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// 显示通知
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const icon = {
        'success': 'fas fa-check-circle',
        'warning': 'fas fa-exclamation-triangle',
        'danger': 'fas fa-times-circle',
        'info': 'fas fa-info-circle'
    }[type];
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            <i class="${icon} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // 在页面顶部显示通知
    const container = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.innerHTML = alertHtml;
    container.insertBefore(alertDiv.firstElementChild, container.firstChild);
    
    // 5秒后自动隐藏
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// 解析URL
async function parseUrl() {
    const url = document.getElementById('url-input').value.trim();
    
    if (!url) {
        showNotification('请输入有效的URL', 'warning');
        return;
    }
    
    showLoading('正在解析链接内容...');
    
    try {
        const response = await fetch('/api/parse_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentContent = result.content;
            currentTitle = result.title;
            currentDescription = result.description;
            isMarkdown = result.is_markdown;
            
            updateContentFields();
            showContentAndStyleSections();
            showNotification('链接解析成功！', 'success');
        } else {
            showNotification(result.error || '解析失败', 'danger');
        }
    } catch (error) {
        showNotification('网络错误，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 上传文件
function uploadFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (file) {
        handleFileUpload(file);
    }
}

// 处理文件上传
async function handleFileUpload(file) {
    if (!file) return;
    
    // 检查文件类型
    const allowedTypes = ['.md', '.txt', '.html'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showNotification('不支持的文件格式，请上传 .md、.txt 或 .html 文件', 'warning');
        return;
    }
    
    // 检查文件大小 (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showNotification('文件过大，请选择小于16MB的文件', 'warning');
        return;
    }
    
    showLoading('正在处理文件...');
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/api/upload_file', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentContent = result.content;
            currentTitle = result.title;
            currentDescription = result.description;
            isMarkdown = result.is_markdown;
            
            updateContentFields();
            showContentAndStyleSections();
            showNotification('文件上传成功！', 'success');
        } else {
            showNotification(result.error || '文件处理失败', 'danger');
        }
    } catch (error) {
        showNotification('上传失败，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 处理直接输入的文本
function processText() {
    const textInput = document.getElementById('text-input');
    const markdownCheckbox = document.getElementById('is-markdown');
    
    const content = textInput.value.trim();
    
    if (!content) {
        showNotification('请输入内容', 'warning');
        return;
    }
    
    currentContent = content;
    currentTitle = '直接输入的内容';
    currentDescription = content.substring(0, 100) + (content.length > 100 ? '...' : '');
    isMarkdown = markdownCheckbox.checked;
    
    updateContentFields();
    showContentAndStyleSections();
    showNotification('内容已加载！', 'success');
}

// 更新内容字段
function updateContentFields() {
    document.getElementById('content-title').value = currentTitle;
    document.getElementById('content-description').value = currentDescription;
    
    // 获取最新值
    currentTitle = document.getElementById('content-title').value;
    currentDescription = document.getElementById('content-description').value;
}

// 显示内容编辑和样式选择区域
function showContentAndStyleSections() {
    document.getElementById('content-section').style.display = 'block';
    document.getElementById('style-section').style.display = 'block';
    document.getElementById('settings-section').style.display = 'block';
    
    // 滚动到内容区域
    document.getElementById('content-section').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    // 添加动画效果
    setTimeout(() => {
        document.getElementById('content-section').classList.add('fade-in-up');
        document.getElementById('style-section').classList.add('fade-in-up');
        document.getElementById('settings-section').classList.add('fade-in-up');
    }, 100);
}

// 智能分割推荐
async function smartSplit() {
    if (!currentContent) {
        showNotification('请先添加内容', 'warning');
        return;
    }
    
    showLoading('正在分析内容结构...');
    
    try {
        const response = await fetch('/api/smart_split', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: currentContent,
                is_markdown: isMarkdown
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('split-count').value = result.recommended_count;
            
            const analysis = result.analysis;
            const message = `推荐分割为 ${result.recommended_count} 张图片
                <br><small>分析结果：内容长度 ${analysis.total_chars} 字符，${analysis.total_lines} 行</small>`;
            
            showNotification(message, 'info');
            
            // 自动生成预览
            setTimeout(generatePreviews, 500);
        } else {
            showNotification(result.error || '分析失败', 'danger');
        }
    } catch (error) {
        showNotification('网络错误，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 一键美化
function oneClickBeautify() {
    if (!currentContent) {
        showNotification('请先添加内容', 'warning');
        return;
    }
    
    // 根据内容长度选择最佳样式
    const contentLength = currentContent.length;
    let recommendedStyle = 'clean';
    let recommendedCount = 3;
    
    if (contentLength > 1000) {
        recommendedStyle = 'clean';
        recommendedCount = Math.min(Math.max(Math.ceil(contentLength / 500), 3), 8);
    } else if (contentLength > 500) {
        recommendedStyle = 'minimal';
        recommendedCount = Math.min(Math.max(Math.ceil(contentLength / 300), 2), 5);
    } else {
        recommendedStyle = 'card';
        recommendedCount = Math.min(Math.max(Math.ceil(contentLength / 200), 1), 3);
    }
    
    // 选择推荐样式
    selectStyle(recommendedStyle);
    document.getElementById('split-count').value = recommendedCount;
    
    showNotification('已应用最佳设置，正在生成预览...', 'success');
    
    // 自动生成预览
    setTimeout(generatePreviews, 500);
}

// 生成预览
async function generatePreviews() {
    // 更新当前内容
    currentTitle = document.getElementById('content-title').value;
    currentDescription = document.getElementById('content-description').value;
    
    if (!currentContent) {
        showNotification('请先添加内容', 'warning');
        return;
    }
    
    const splitCount = parseInt(document.getElementById('split-count').value);
    const highlightTheme = document.getElementById('highlight-theme').value;
    
    showLoading('正在生成预览图片...');
    
    try {
        const response = await fetch('/api/generate_images', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: currentContent,
                title: currentTitle,
                description: currentDescription,
                style: selectedStyle,
                split_count: splitCount,
                is_markdown: isMarkdown,
                highlight_theme: highlightTheme
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentPreviews = result.previews;
            displayPreviews(result.previews);
            showPreviewSection();
            showNotification(`成功生成 ${result.total_count} 张预览图片！`, 'success');
        } else {
            showNotification(result.error || '生成失败', 'danger');
        }
    } catch (error) {
        showNotification('网络错误，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 显示预览结果
function displayPreviews(previews) {
    const container = document.getElementById('preview-container');
    const countBadge = document.getElementById('preview-count');
    
    container.innerHTML = '';
    countBadge.textContent = previews.length;
    
    previews.forEach((preview, index) => {
        const styleName = STYLE_NAMES[selectedStyle] || selectedStyle;
        const previewHtml = `
            <div class="col-lg-6 col-xl-4 preview-item">
                <div class="preview-content">
                    <div class="preview-header">
                        <span>第 ${preview.index} 张 - ${styleName}</span>
                        <span class="badge bg-info">${preview.word_count} 字</span>
                    </div>
                    <div class="preview-body">
                        <iframe class="preview-html" srcdoc="${escapeHtml(preview.html)}"></iframe>
                        <div class="preview-controls">
                            <button class="btn btn-sm btn-outline-primary" onclick="editPreview(${index})" title="编辑内容">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-success" onclick="downloadSingle(${index})" title="下载此图">
                                <i class="fas fa-download"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-info" onclick="copyContent(${index})" title="复制内容">
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                    </div>
                    <div class="preview-footer">
                        <span>${preview.summary}</span>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>刚刚生成
                        </small>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += previewHtml;
    });
}

// 显示预览区域
function showPreviewSection() {
    document.getElementById('preview-section').style.display = 'block';
    
    // 滚动到预览区域
    setTimeout(() => {
        document.getElementById('preview-section').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        document.getElementById('preview-section').classList.add('fade-in-up');
    }, 100);
}

// 转义HTML
function escapeHtml(html) {
    return html
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// 编辑预览内容
function editPreview(index) {
    if (index >= currentPreviews.length) return;
    
    const preview = currentPreviews[index];
    const newContent = prompt('编辑内容：', preview.content);
    
    if (newContent !== null && newContent.trim() !== '') {
        // 更新预览内容并重新生成该项
        currentPreviews[index].content = newContent.trim();
        currentPreviews[index].word_count = newContent.trim().length;
        currentPreviews[index].summary = newContent.trim().replace('\n', ' ').substring(0, 50) + 
                                         (newContent.trim().length > 50 ? '...' : '');
        
        // 重新生成这一项的HTML
        regeneratePreview(index);
    }
}

// 重新生成单个预览
async function regeneratePreview(index) {
    // 这里可以调用后端API重新生成单个预览
    showNotification('内容已更新！重新生成预览请点击"生成预览"', 'info');
}

// 更新下载单张图片函数
function downloadSingle(index) {
    console.log(`[前端] 调用 downloadSingle, 输入 index: ${index}`);
    // 假设 index 是1-based，转换为0-based
    const zeroIndex = index - 1;
    console.log(`[前端] 发送的 zeroIndex: ${zeroIndex}`);
    
    console.log(`[前端] 当前状态: content=${!!currentContent}, previews长度=${currentPreviews.length}`);
    // 从本地变量获取数据（假设 generateImages 后已保存）
    if (!currentContent || zeroIndex < 0 || zeroIndex >= currentPreviews.length) {
        console.error(`[前端] 无效索引: ${zeroIndex}, 预览长度: ${currentPreviews.length}`);
        alert('无效的图片索引或内容未准备好');
        return;
    }
    
    console.log(`[前端] 发送参数: content长度=${currentContent.length}, title=${currentTitle}, split_count=${currentPreviews.length}, index=${zeroIndex}`);
    
    fetch('/api/download_single', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: currentContent,
            title: currentTitle,
            description: currentDescription,
            style: selectedStyle,
            split_count: currentPreviews.length,
            index: zeroIndex,
            is_markdown: isMarkdown,
            highlight_theme: document.getElementById('highlight-theme').value
        })
    })
    .then(response => {
        console.log(`[前端] 下载响应状态: ${response.status}`);
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || '下载失败'); });
        }
        return response.blob();
    })
    .then(blob => {
        console.log(`[前端] 下载 blob 大小: ${blob.size}`);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `image_${index}.png`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => {
        console.error('[前端] 下载错误:', error);
        alert('下载失败: ' + error.message);
    });
}

// 更新批量导出函数
function exportAll() {
    if (!currentContent || currentPreviews.length === 0) {
        alert('没有内容可导出');
        return;
    }
    
    fetch('/api/export_images', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            content: currentContent,
            title: currentTitle,
            description: currentDescription,
            style: selectedStyle,
            split_count: currentPreviews.length,
            is_markdown: isMarkdown,
            highlight_theme: document.getElementById('highlight-theme').value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('导出失败');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'images.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
    })
    .catch(error => {
        console.error('导出错误:', error);
        alert('导出失败: ' + error.message);
    });
}

// 导出文案
async function exportText() {
    // 如果没有预览，先自动生成
    if (currentPreviews.length === 0) {
        // 如果没有内容，先尝试从输入框获取
        if (!currentContent) {
            const textInput = document.getElementById('text-input');
            const content = textInput.value.trim();
            if (!content) {
                showNotification('请先输入内容', 'warning');
                return;
            }
            // 自动处理文本
            processText();
            // 等待处理完成
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        showNotification('正在自动生成预览...', 'info');
        await generatePreviews();
        
        // 生成失败则返回
        if (currentPreviews.length === 0) {
            showNotification('无法生成预览，请先添加内容', 'warning');
            return;
        }
    }
    
    showLoading('正在生成文案文件...');
    
    try {
        const response = await fetch('/api/export_text');
        
        if (response.ok) {
            // 获取文件名
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'content.txt';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch) {
                    filename = filenameMatch[1];
                }
            }
            
            // 下载文件
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showNotification('文案导出成功！', 'success');
        } else {
            const result = await response.json();
            showNotification(result.error || '导出失败', 'danger');
        }
    } catch (error) {
        showNotification('导出失败，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 保存历史记录
async function saveHistory() {
    if (!currentContent) {
        showNotification('没有内容可保存', 'warning');
        return;
    }
    
    showLoading('正在保存...');
    
    try {
        const response = await fetch('/api/save_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: currentTitle,
                description: currentDescription,
                content: currentContent,
                style: selectedStyle,
                split_count: parseInt(document.getElementById('split-count').value),
                is_markdown: isMarkdown
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showNotification('保存成功！', 'success');
        } else {
            showNotification(result.error || '保存失败', 'danger');
        }
    } catch (error) {
        showNotification('保存失败，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 显示历史记录
async function showHistory() {
    showLoading('正在加载历史记录...');
    
    try {
        const response = await fetch('/api/get_history');
        const result = await response.json();
        
        if (result.success) {
            displayHistoryModal(result.history);
        } else {
            showNotification(result.error || '加载历史记录失败', 'danger');
        }
    } catch (error) {
        showNotification('网络错误，请稍后重试', 'danger');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// 显示历史记录模态框
function displayHistoryModal(history) {
    const historyList = document.getElementById('history-list');
    
    if (history.length === 0) {
        historyList.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-history fa-3x text-muted mb-3"></i>
                <p class="text-muted">暂无历史记录</p>
            </div>
        `;
    } else {
        historyList.innerHTML = '';
        
        history.forEach(item => {
            const date = new Date(item.created_at).toLocaleString('zh-CN');
            const styleName = STYLE_NAMES[item.style] || item.style;
            const historyHtml = `
                <div class="history-item" onclick="loadHistoryItem('${item.id}')">
                    <h6>${item.title}</h6>
                    <p class="text-muted mb-2">${item.description.substring(0, 100)}...</p>
                    <div class="history-meta">
                        <div>
                            <span class="badge bg-info me-2">${styleName}</span>
                            <span class="badge bg-success me-2">${item.split_count} 张</span>
                            ${item.is_markdown ? '<span class="badge bg-warning">Markdown</span>' : ''}
                        </div>
                        <small>${date}</small>
                    </div>
                </div>
            `;
            historyList.innerHTML += historyHtml;
        });
    }
    
    // 显示模态框
    const modal = new bootstrap.Modal(document.getElementById('historyModal'));
    modal.show();
}

// 加载历史记录项目
function loadHistoryItem(id) {
    // 这里应该根据ID加载具体的历史记录
    showNotification('历史记录加载功能开发中...', 'info');
    
    // 关闭模态框
    const modal = bootstrap.Modal.getInstance(document.getElementById('historyModal'));
    modal.hide();
}

// 工具函数：防抖
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 工具函数：节流
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 响应式处理
function handleResize() {
    // 在小屏幕上调整预览布局
    const previewItems = document.querySelectorAll('.preview-item');
    if (window.innerWidth < 768) {
        previewItems.forEach(item => {
            item.className = 'col-12 preview-item';
        });
    } else if (window.innerWidth < 1200) {
        previewItems.forEach(item => {
            item.className = 'col-lg-6 preview-item';
        });
    } else {
        previewItems.forEach(item => {
            item.className = 'col-lg-6 col-xl-4 preview-item';
        });
    }
}

// 监听窗口大小变化
window.addEventListener('resize', throttle(handleResize, 250));

// 键盘快捷键支持
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter 快速生成预览
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (currentContent) {
            generatePreviews();
        }
    }
    
    // Ctrl/Cmd + S 保存历史记录
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveHistory();
    }
});

// 错误处理
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('发生了未知错误，请刷新页面重试', 'danger');
});

// 调试状态
async function debugStatus() {
    console.log(`[调试] 开始调试状态检查`);
    
    try {
        // 前端状态
        const frontendStatus = {
            currentContent: currentContent ? `${currentContent.length} 字符` : 'null',
            currentTitle: currentTitle || 'null',
            currentDescription: currentDescription || 'null',
            currentPreviews: currentPreviews.length,
            selectedStyle: selectedStyle || 'null',
            isMarkdown: isMarkdown
        };
        
        console.log(`[调试] 前端状态:`, frontendStatus);
        
        // 获取session状态
        const response = await fetch('/api/debug/session');
        const sessionStatus = await response.json();
        
        console.log(`[调试] Session状态:`, sessionStatus);
        
        // 显示调试信息
        const debugInfo = `
=== 前端状态 ===
当前内容: ${frontendStatus.currentContent}
当前标题: ${frontendStatus.currentTitle}
当前描述: ${frontendStatus.currentDescription}
当前预览: ${frontendStatus.currentPreviews} 个
选择样式: ${frontendStatus.selectedStyle}
Markdown模式: ${frontendStatus.isMarkdown}

=== Session状态 ===
有预览数据: ${sessionStatus.has_previews}
预览数量: ${sessionStatus.preview_count}
当前样式: ${sessionStatus.current_style}
当前标题: ${sessionStatus.current_title}
Session键: ${sessionStatus.session_keys.join(', ')}
临时文件夹存在: ${sessionStatus.temp_folder_exists}
临时文件数量: ${sessionStatus.temp_files_count}
        `;
        
        alert(debugInfo);
        
        // 如果需要，提供修复建议
        if (frontendStatus.currentPreviews === 0 && sessionStatus.preview_count === 0) {
            if (!frontendStatus.currentContent) {
                showNotification('问题：没有内容。请在文本输入框中添加内容。', 'warning');
            } else {
                showNotification('建议：尝试手动点击"生成预览"按钮。', 'info');
            }
        }
        
    } catch (error) {
        console.error(`[调试] 调试状态检查失败:`, error);
        alert(`调试失败: ${error.message}`);
    }
}

// 页面卸载前的确认
window.addEventListener('beforeunload', function(e) {
    if (currentContent && currentPreviews.length > 0) {
        e.preventDefault();
        e.returnValue = '确定要离开吗？未保存的内容将会丢失。';
    }
}); 