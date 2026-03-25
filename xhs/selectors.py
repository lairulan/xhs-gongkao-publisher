# xhs/selectors.py
# 小红书页面 CSS 选择器集中管理
# XHS 改版时只需修改此文件，无需遍寻全项目
#
# 更新日志：
# - 2026-03-25 v3.0.0 新建，集中管理所有 CSS 选择器

from dataclasses import dataclass
from typing import Optional


@dataclass
class XHSSelectors:
    """
    小红书页面元素选择器集合
    所有选择器基于当前 XHS Web 版本（2026-03）
    XHS 改版后优先尝试以下方案：
      1. 浏览器 DevTools Elements 面板查找
      2. 页面 DOM 结构分析（window.__INITIAL_STATE__）
      3. 如选择器失效，对比旧/新选择器并更新本文件
    """

    # ============================================================
    # 创作服务平台 - 发布页
    # https://creator.xiaohongshu.com/publish/publish
    # ============================================================

    publish_page = {
        "url": "https://creator.xiaohongshu.com/publish/publish",
        "upload_tab": '[data-v-4eb81f2c] .tabs li:nth-child(1)',  # 上传图文 Tab
        "upload_tab_text": "图文",
    }

    # 图片上传
    image_upload = {
        "input": 'input.upload-input[type=file]',
        "thumbnail_wrapper": ".img-list .img-item",  # 上传后缩略图容器
        "thumbnail_first": ".img-list .img-item:first-child",  # 第一张（封面）
        "delete_btn": ".img-item .delete-icon",  # 删除按钮
        "upload_progress": ".upload-progress",
    }

    # 标题输入
    title = {
        "input": 'textarea.title-input[data-v-4eb81f2c], div.title-input[data-v-4eb81f2c] textarea',
        "counter": ".title-input .word-counter",
        "placeholder": "填写标题会有更多赞哦",
    }

    # 正文编辑
    content = {
        "editor": 'div.editor-input[data-v-4eb81f2c] textarea, div.content-editor textarea',
        "placeholder": "填写正文",
        "word_count": ".content-editor .word-count",
    }

    # 话题标签
    tags = {
        "button": 'button[data-v-4eb81f2c]:has-text("# 话题"), div.tag-area button',
        "search_input": ".tag-search-input input, .topic-search input",
        "search_result": ".tag-list .tag-item, .topic-list .topic-item",
        "selected": ".selected-tags .tag-item",
        "add_topic_btn": ".add-topic-btn",
    }

    # 权限设置（下拉选择）
    visibility = {
        "dropdown": ".visibility-select .d-select, div.publish-type select",
        "option_public": 'option[value="public"], .d-option:has-text("公开")',
        "option_private": 'option[value="private"], .d-option:has-text("仅自己可见")',
        "current_value": ".visibility-select .current-value, .d-select .current",
    }

    # 发布按钮
    publish = {
        "btn": 'button[data-v-4eb81f2c].publish-btn, button.publish-button, button.submit-btn',
        "btn_text": "发布",
        "confirm_btn": ".confirm-btn, button[data-v-4eb81f2c]:has-text('确认')",
    }

    # 发布成功
    publish_success = {
        "indicator": ".success-modal, .publish-success, [data-v-4eb81f2c] .success",
        "note_link": ".published-link a, .success-modal a",
        "close_btn": ".success-modal .close, .modal-close",
    }

    # ============================================================
    # 小红书首页 / 发现页
    # https://www.xiaohongshu.com
    # ============================================================

    home = {
        "search_bar": 'input.search-input, input[name="keyword"], .search-input',
        "login_btn": ".login-btn, .login",
        "user_avatar": ".user-avatar, .avatar",
    }

    # ============================================================
    # 搜索结果页
    # https://www.xiaohongshu.com/search_result?keyword=xxx
    # ============================================================

    search = {
        "result_container": ".search-result-list, .feeds-container",
        "note_card": ".note-item, .search-card",
        "note_title": ".note-title, .title",
        "note_author": ".author-wrapper .name, .user-name",
        "note_likes": ".like-wrapper .count, .like-count",
        "note_cover": ".note-cover img, .cover img",
        "filter_tabs": ".filter-tabs .tab, .search-tabs .tab",
    }

    # ============================================================
    # 笔记详情页
    # https://www.xiaohongshu.com/explore/xxx
    # ============================================================

    note_detail = {
        "title": ".note-content .title, h1.title",
        "author": ".author-info .name, .user-name",
        "author_avatar": ".author-info .avatar img",
        "content": ".note-content .desc, .content",
        "tags": ".tag-list .tag, .topic-link",
        "like_btn": ".like-wrapper button, button.like-btn",
        "like_count": ".like-count, .like-wrapper span",
        "collect_btn": ".collect-btn, .collect-wrapper button",
        "comment_input": ".comment-input input, textarea.comment",
        "comment_list": ".comment-list, .comments",
        "share_btn": ".share-btn",
        "initial_state": "window.__INITIAL_STATE__",  # 页面数据
    }

    # ============================================================
    # 用户主页
    # https://www.xiaohongshu.com/user/profile/xxx
    # ============================================================

    user_profile = {
        "tabs": ".user-tab .tab-item, .profile-tabs .tab",
        "notes_tab": '[data-tab="note"], .notes-tab',
        "like_tab": '[data-tab="like"], .like-tab',
        "note_list": ".note-list, .user-notes",
        "note_card": ".note-card",
        "follow_btn": ".follow-btn, button.follow",
        "following_count": ".following-count",
        "follower_count": ".fans-count, .follower-count",
    }

    # ============================================================
    # 登录页
    # https://www.xiaohongshu.com/login
    # ============================================================

    login = {
        "qr_tab": ".qrcode-tab, .tab-qr",
        "qr_image": ".qrcode-img img, .qr-image",
        "qr_expired": ".qrcode-expired, .qr-expired",
        "refresh_qr": ".refresh-qrcode, .qr-refresh",
        "switch_qr": ".switch-qr, .re-qr",
        "phone_tab": ".phone-tab, .tab-phone",
        "phone_input": 'input[type="tel"], input.phone-input',
        "code_input": 'input[name="code"], input.code-input',
        "get_code_btn": ".get-code-btn, button.getCode",
        "login_btn": 'button.login-btn[type="submit"]',
    }

    # ============================================================
    # 通用 / 弹窗
    # ============================================================

    common = {
        "toast": ".toast, .message, .tips",
        "modal": ".modal, .dialog",
        "loading": ".loading, .spinner",
        "error_tips": ".error-tips, .error-msg",
        "confirm_btn": ".confirm, button.confirm",
        "cancel_btn": ".cancel, button.cancel",
        "close_btn": ".close, button.close",
        "overlay": ".overlay, .mask",
    }

    # ============================================================
    # 辅助方法
    # ============================================================

    @classmethod
    def for_publish(cls, element: str) -> str:
        """获取发布页指定元素的 CSS 选择器"""
        mapping = {
            "image_input": cls.publish_page["upload_tab"],  # 需先切到图文tab
            "title_input": cls.title["input"],
            "content_input": cls.content["editor"],
            "tag_btn": cls.tags["button"],
            "publish_btn": cls.publish["btn"],
            "visibility_dropdown": cls.visibility["dropdown"],
        }
        return mapping.get(element, "")

    @classmethod
    def for_note(cls, element: str) -> str:
        """获取笔记详情页指定元素的 CSS 选择器"""
        mapping = {
            "title": cls.note_detail["title"],
            "content": cls.note_detail["content"],
            "tags": cls.note_detail["tags"],
            "like_btn": cls.note_detail["like_btn"],
            "collect_btn": cls.note_detail["collect_btn"],
            "comment_input": cls.note_detail["comment_input"],
            "comment_list": cls.note_detail["comment_list"],
            "share_btn": cls.note_detail["share_btn"],
        }
        return mapping.get(element, "")

    @classmethod
    def for_search(cls, element: str) -> str:
        """获取搜索结果页指定元素的 CSS 选择器"""
        mapping = {
            "result_container": cls.search["result_container"],
            "note_card": cls.search["note_card"],
            "note_title": cls.search["note_title"],
            "note_author": cls.search["note_author"],
            "note_likes": cls.search["note_likes"],
            "note_cover": cls.search["note_cover"],
            "filter_tabs": cls.search["filter_tabs"],
        }
        return mapping.get(element, "")


# ============================================================
# 选择器版本追踪（XHS 改版时记录）
# ============================================================

SELECTOR_VERSION = "2026-03-25"

# 已知的 XHS 改版时间线（用于快速定位问题）
# 2025-06: 创作平台发布页改版，class 名从 data-v-xxx 切换
# 2025-09: 搜索结果页 DOM 结构变化
# 2026-01: 笔记详情页性能优化，部分元素懒加载
# 2026-03: 当前版本

# ============================================================
# Stealth JS 反检测注入脚本
# ============================================================

STEALTH_JS = """
// Stealth mode: 模拟真实用户行为特征
// 注入到页面控制台，绕过基础反自动化检测

Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
    configurable: true
});

// 移除自动化标识
delete window.cdp_automation;
delete window.__webdriver;
delete window.__selenium;
delete window.__webdriver_script_function;
delete window.__webdriver_script_func;
delete window.__webdriver_script_at;
delete window.__selenium;
delete window.__Selenium_IDE_Recorder;
delete window.__driver_undefined;

// 模拟真实浏览器属性
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5],
    configurable: true
});

Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'zh', 'en-US', 'en'],
    configurable: true
});

// 随机化 canvas fingerprint
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function(...args) {
    const ctx = this.getContext('2d');
    if (ctx) {
        const imageData = ctx.getImageData(0, 0, this.width, this.height);
        for (let i = 0; i < imageData.data.length; i += 4) {
            imageData.data[i] += Math.random() * 0.5;
            imageData.data[i + 1] += Math.random() * 0.5;
            imageData.data[i + 2] += Math.random() * 0.5;
        }
        ctx.putImageData(imageData, 0, 0);
    }
    return originalToDataURL.apply(this, args);
};
"""


def get_stealth_js() -> str:
    """返回反检测 JS 代码"""
    return STEALTH_JS


# ============================================================
# 选择器失效时的降级策略
# ============================================================

FALLBACK_SELECTORS = {
    "image_input": [
        'input[type="file"][accept*="image"]',
        'input.upload-input',
        '[data-v-4eb81f2c] input[type=file]',
        'form input[type=file]',
    ],
    "title_input": [
        'textarea.title-input',
        'div[contenteditable="true"].title-input',
        'input[name="title"]',
        '[placeholder*="标题"]',
    ],
    "content_input": [
        'div[contenteditable="true"].editor-input',
        'textarea.editor-input',
        '[placeholder*="正文"]',
    ],
    "publish_btn": [
        'button[data-v-4eb81f2c].publish-btn',
        'button:has-text("发布")',
        '[class*="publish"] button[type="submit"]',
    ],
}


def get_fallback_selector(primary_key: str) -> list:
    """获取降级选择器列表（按优先级排序）"""
    return FALLBACK_SELECTORS.get(primary_key, [])
