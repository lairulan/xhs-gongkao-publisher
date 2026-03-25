# xhs/content_analyzer.py
# 竞品笔记分析模块
# v3.0.0 新增：从选题到爆款特征分析，辅助内容决策
#
# 分析维度：
#   1. 标题模板（句式/关键词位置/字数）
#   2. 封面模板（文字层级/配色风格）
#   3. 正文模板（开场钩子/段落结构/结尾CTA）
#   4. 互动模板（评论区引导/话题选择）
#   5. 标签策略（数量/类型/组合）
#
# 输出：改写方向 + 选题建议

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# ============================================================
# 数据结构
# ============================================================

@dataclass
class CompetitorNote:
    """竞品笔记原始数据"""
    url: str
    title: str = ""
    author: str = ""
    likes: int = 0
    collects: int = 0
    comments: int = 0
    tags: list[str] = field(default_factory=list)
    content: str = ""
    cover_style: str = ""  # 封面风格
    publish_time: str = ""

    def total_engagement(self) -> int:
        return self.likes + self.collects + self.comments


@dataclass
class NoteAnalysis:
    """笔记分析结果"""
    # 标题分析
    title_template: str  # 句式类型：数字痛点/疑问/感叹/陈述
    title_length: int    # 字数
    title_keywords: list[str]  # 关键词位置
    title_hook_type: str  # 钩子类型

    # 封面分析
    cover_text_hierarchy: str  # 文字层级
    cover_color_style: str  # 配色风格
    cover_has_emoji: bool  # 是否用emoji

    # 正文分析
    content_opening: str  # 开场钩子
    content_length: int  # 正文字数
    content_paragraphs: int  # 段落数
    content_ending: str  # 结尾类型
    content_cta: str  # CTA类型

    # 互动分析
    comment_guidance: str  # 评论引导方式
    topic_count: int  # 话题数量
    topic_types: list[str]  # 话题类型

    # 综合评分
    virality_score: float  # 爆款指数 0-10

    # 改写方向
    rewrite_direction: str  # 如何保留结构替换内容
    suggested_angles: list[str]  # 可差异化的角度


# ============================================================
# 竞品分析引擎
# ============================================================

class ContentAnalyzer:
    """
    竞品笔记分析器
    输入：CompetitorNote（原始数据）
    输出：NoteAnalysis（分析结果）+ 改写建议
    """

    # 标题句式模式
    TITLE_PATTERNS = [
        (r"^\d+[个点招].*", "数字列举"),
        (r".*?!$", "感叹句"),
        (r".*\?$", "疑问句"),
        (r"^.*我.*了.*$", "个人经历"),
        (r"^.*终于.*$", "转折惊喜"),
        (r"^.*真的.*$", "真诚强调"),
        (r"^.*分享.*$", "分享型"),
        (r"^.*指南.*$", "攻略型"),
        (r"^.*技巧.*$", "技巧型"),
    ]

    # 开场钩子模式
    OPENING_PATTERNS = [
        (r"^.*最近.*", "近况切入"),
        (r"^.*终于.*", "结果前置"),
        (r"^.*没想到.*", "意外反转"),
        (r"^.*姐妹们.*", "称呼召唤"),
        (r"^.*坦白说.*", "坦诚直入"),
        (r"^.*刷到.*", "场景代入"),
    ]

    # CTA 类型
    CTA_TYPES = [
        "评论区提问",
        "征集经历",
        "求收藏",
        "求点赞",
        "关注引导",
        "互动投票",
        "无明显CTA",
    ]

    def __init__(self):
        self.notes_db_path = Path("~/.claude/skills/xhs-gongkao-publisher/output/competitor_notes.json").expanduser()

    def analyze(self, note: CompetitorNote) -> NoteAnalysis:
        """
        分析单篇笔记

        Args:
            note: 竞品笔记数据

        Returns:
            NoteAnalysis: 分析结果
        """
        # 标题分析
        title_template = self._detect_title_template(note.title)
        title_keywords = self._extract_title_keywords(note.title)
        title_hook = self._detect_title_hook(note.title)

        # 封面分析（从内容推断）
        cover_analysis = self._analyze_cover(note)

        # 正文分析
        content_analysis = self._analyze_content(note.content)

        # 互动分析
        topic_analysis = self._analyze_topics(note.tags)
        comment_guide = self._detect_comment_guidance(note.content)

        # 计算爆款指数
        virality = self._calc_virality_score(note)

        # 生成改写方向
        rewrite_dir = self._generate_rewrite_direction(note, title_template, content_analysis)

        return NoteAnalysis(
            title_template=title_template,
            title_length=len(note.title),
            title_keywords=title_keywords,
            title_hook_type=title_hook,
            cover_text_hierarchy=cover_analysis["hierarchy"],
            cover_color_style=cover_analysis["color"],
            cover_has_emoji=bool(re.search(r"[\U0001F300-\U0001F9FF]", note.title)),
            content_opening=content_analysis["opening"],
            content_length=len(note.content),
            content_paragraphs=note.content.count("\n\n") + 1,
            content_ending=content_analysis["ending"],
            content_cta=content_analysis["cta"],
            comment_guidance=comment_guide,
            topic_count=len(note.tags),
            topic_types=topic_analysis["types"],
            virality_score=virality,
            rewrite_direction=rewrite_dir,
            suggested_angles=self._generate_angles(note, virality),
        )

    def _detect_title_template(self, title: str) -> str:
        """检测标题句式模板"""
        for pattern, label in self.TITLE_PATTERNS:
            if re.search(pattern, title):
                return label
        return "陈述句"

    def _extract_title_keywords(self, title: str) -> list[str]:
        """提取标题关键词"""
        # 常见关键词模式
        patterns = [
            r"行测|申论|省考|国考|公务员",
            r"上岸|备考|复习|冲刺",
            r"资料|技巧|方法|干货",
            r"分享|经验|心得|体会",
        ]
        keywords = []
        for p in patterns:
            matches = re.findall(p, title)
            keywords.extend(matches)
        return list(set(keywords))

    def _detect_title_hook(self, title: str) -> str:
        """检测标题钩子类型"""
        if re.search(r"^\d+", title):
            return "数字开头"
        elif "?" in title or "？" in title:
            return "疑问句"
        elif re.search(r"[!！~]", title):
            return "感叹强调"
        elif re.search(r"终于|终于了", title):
            return "结果悬念"
        return "普通陈述"

    def _analyze_cover(self, note: CompetitorNote) -> dict:
        """分析封面风格（基于已有信息推断）"""
        # 简化版：实际应分析封面图片
        has_emoji = bool(re.search(r"[\U0001F300-\U0001F9FF]", note.title))
        has_number = bool(re.search(r"^\d+", note.title))
        has_colon = "：" in note.title or ":" in note.title

        hierarchy = "文字为主"
        if has_emoji:
            hierarchy = "emoji+文字"
        if has_number and has_colon:
            hierarchy = "数字+冒号+文字"

        color = "未知（需图片分析）"
        return {"hierarchy": hierarchy, "color": color}

    def _analyze_content(self, content: str) -> dict:
        """分析正文结构"""
        paragraphs = [p for p in content.split("\n\n") if p.strip()]
        first_para = paragraphs[0] if paragraphs else ""

        # 检测开场
        opening = "普通叙述"
        for pattern, label in self.OPENING_PATTERNS:
            if re.search(pattern, first_para):
                opening = label
                break

        # 检测结尾
        last_para = paragraphs[-1] if paragraphs else ""
        ending = "总结型"
        if re.search(r"大家.*|姐妹.*", last_para):
            ending = "召唤互动"
        elif re.search(r"有问题.*|可以.*", last_para):
            ending = "开放引导"
        elif len(last_para) < 20:
            ending = "简短干脆"

        # 检测 CTA
        cta = "无明显CTA"
        if re.search(r"评论区|评论", content):
            cta = "评论区提问"
        elif re.search(r"收藏|收", content):
            cta = "求收藏"
        elif re.search(r"点赞|喜欢", content):
            cta = "求点赞"

        return {"opening": opening, "ending": ending, "cta": cta}

    def _analyze_topics(self, tags: list[str]) -> dict:
        """分析话题标签策略"""
        types = []
        for tag in tags:
            if any(k in tag for k in ["公考", "省考", "国考", "公务员"]):
                types.append("公考通用")
            elif any(k in tag for k in ["行测", "申论"]):
                types.append("科目")
            elif any(k in tag for k in ["上岸", "备考", "经验"]):
                types.append("经验")
            elif any(k in tag for k in ["上岸", "加油"]):
                types.append("心态")
            else:
                types.append("其他")

        return {"types": list(set(types))}

    def _detect_comment_guidance(self, content: str) -> str:
        """检测评论区引导方式"""
        if re.search(r"评论区.*|你们.*|大家.*", content):
            return "征集评论"
        elif re.search(r"有问题.*|不懂.*|可以问", content):
            return "开放提问"
        elif re.search(r".*了吗|.*怎么样", content):
            return "征求意见"
        return "无明显引导"

    def _calc_virality_score(self, note: CompetitorNote) -> float:
        """
        计算爆款指数（0-10）
        简化版：基于互动数据估算
        """
        engagement = note.total_engagement()
        if engagement > 10000:
            return 9.0
        elif engagement > 5000:
            return 8.0
        elif engagement > 1000:
            return 7.0
        elif engagement > 500:
            return 6.0
        elif engagement > 100:
            return 5.0
        else:
            return 4.0

    def _generate_rewrite_direction(self, note: CompetitorNote, title_template: str, content_analysis: dict) -> str:
        """生成改写方向"""
        return (
            f"保留「{title_template}」句式，"
            f"替换为公考相关内容，"
            f"开场用「{content_analysis['opening']}」方式切入，"
            f"结尾用「{content_analysis['ending']}」收尾"
        )

    def _generate_angles(self, note: CompetitorNote, virality: float) -> list[str]:
        """生成可差异化角度"""
        angles = []

        if virality >= 7:
            angles.append("从个人真实经历角度切入（避免同质化）")
            angles.append("补充更新/更实用的细节")
            angles.append("换个切入角度（如从失败经验出发）")

        angles.append("增加真实细节（时间/地点/人物/感受）")
        angles.append("调整话题标签组合")

        return angles[:3]

    # ============================================================
    # 竞品数据库
    # ============================================================

    def save_note(self, note: CompetitorNote):
        """保存竞品笔记到本地数据库"""
        self.notes_db_path.parent.mkdir(parents=True, exist_ok=True)

        existing = []
        if self.notes_db_path.exists():
            with open(self.notes_db_path, "r", encoding="utf-8") as f:
                existing = json.load(f)

        # 去重（按 URL）
        urls = {n["url"] for n in existing}
        if note.url not in urls:
            existing.append({
                "url": note.url,
                "title": note.title,
                "author": note.author,
                "likes": note.likes,
                "collects": note.collects,
                "comments": note.comments,
                "tags": note.tags,
                "content": note.content,
                "publish_time": note.publish_time,
                "saved_at": datetime.now().isoformat(),
            })

        with open(self.notes_db_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

    def load_notes(self, min_likes: int = 100) -> list[CompetitorNote]:
        """加载高互动笔记"""
        if not self.notes_db_path.exists():
            return []

        with open(self.notes_db_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        notes = []
        for item in data:
            if item.get("likes", 0) >= min_likes:
                notes.append(CompetitorNote(
                    url=item["url"],
                    title=item.get("title", ""),
                    author=item.get("author", ""),
                    likes=item.get("likes", 0),
                    collects=item.get("collects", 0),
                    comments=item.get("comments", 0),
                    tags=item.get("tags", []),
                    content=item.get("content", ""),
                    publish_time=item.get("publish_time", ""),
                ))

        return notes

    def get_top_templates(self, n: int = 5) -> list[dict]:
        """
        获取 Top N 爆款标题模板
        用于选题参考
        """
        notes = self.load_notes(min_likes=500)
        templates = {}

        for note in notes:
            template = self._detect_title_template(note.title)
            if template not in templates:
                templates[template] = {"count": 0, "avg_likes": 0, "titles": []}
            templates[template]["count"] += 1
            templates[template]["avg_likes"] += note.likes
            if len(templates[template]["titles"]) < 3:
                templates[template]["titles"].append(note.title)

        # 计算平均点赞
        for t in templates.values():
            if t["count"] > 0:
                t["avg_likes"] = t["avg_likes"] / t["count"]

        # 排序
        sorted_templates = sorted(
            templates.items(),
            key=lambda x: x[1]["avg_likes"],
            reverse=True
        )

        return [
            {
                "template": t,
                "count": d["count"],
                "avg_likes": int(d["avg_likes"]),
                "examples": d["titles"],
            }
            for t, d in sorted_templates[:n]
        ]


# ============================================================
# 选题建议生成
# ============================================================

def generate_topic_suggestions(analyzer: ContentAnalyzer, pillar: str, n: int = 3) -> list[str]:
    """
    基于竞品分析生成选题建议

    Args:
        analyzer: ContentAnalyzer 实例
        pillar: 内容方向
        n: 返回数量

    Returns:
        list[str]: 选题建议列表
    """
    templates = analyzer.get_top_templates(n=5)
    suggestions = []

    # 映射内容方向到关键词
    pillar_keywords = {
        "备考干货": ["行测技巧", "申论模板", "资料分析", "秒杀"],
        "资料种草": ["资料推荐", "书单", "APP", "课程"],
        "上岸经验": ["备考经历", "时间安排", "二战", "上岸"],
        "岗位解析": ["选岗", "部门", "待遇", "适合"],
        "时事热点": ["两会", "政策", "申论热点"],
        "心态调节": ["焦虑", "坚持", "动力", "鼓励"],
    }

    keywords = pillar_keywords.get(pillar, ["备考", "上岸"])

    for tmpl in templates[:n]:
        template_name = tmpl["template"]
        example = tmpl["examples"][0] if tmpl["examples"] else ""

        # 生成新选题
        suggestion = f"「{template_name}」类标题 + {pillar}内容"
        suggestions.append(suggestion)

    # 添加差异化角度
    suggestions.append(f"从「{keywords[0]}」角度切入的独特视角")

    return suggestions[:n]
