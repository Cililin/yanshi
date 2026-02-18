#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研时系统 - AI知识点抽取脚本
使用通义千问API从时政文章中抽取知识点
"""

import sys
import json
import dashscope
from dashscope import Generation

# API密钥（从命令行参数或环境变量获取）
API_KEY = sys.argv[1] if len(sys.argv) > 1 else None

if not API_KEY:
    print(json.dumps({"error": "API_KEY is required"}))
    sys.exit(1)

dashscope.api_key = API_KEY


def extract_knowledge(article_title, article_content):
    """
    从文章中抽取知识点

    Args:
        article_title: 文章标题
        article_content: 文章内容

    Returns:
        List[dict]: 知识点列表
    """
    # 截取内容（避免过长）
    content = article_content[:3000] if article_content else ""

    prompt = f"""你是一个专业的时政知识抽取助手，请从以下时政新闻中抽取重要知识点。

文章标题：{article_title}

文章内容：
{content}

请按以下要求抽取：

1. 抽取类型：
   - 核心概念（2-6字）：如"新质生产力"、"乡村振兴"、"高质量发展"
   - 重要人物：国家领导人、部委负责人、重要企业家
   - 关键事件：会议名称、政策发布、重大活动
   - 重要政策：具体政策名称、法规、规划
   - 关键数据：重要统计数据、指标

2. 分类归属：
   - 政治：会议活动、政策法规、制度建设、党建工作
   - 经济：宏观经济、产业发展、区域发展、对外贸易
   - 社会：民生保障、教育科技、医疗卫生、生态环境
   - 外交：国际合作、多边机制、大国外交

3. 重要性评分（1-10）：
   - 10分：出现在标题或开头的核心概念
   - 8-9分：文章主要讨论的重要概念
   - 6-7分：次要但重要的概念
   - 1-5分：一般性提及

输出格式（每行一个知识点，使用|分隔）：
名称|类型|分类|重要性|描述

示例：
新质生产力|concept|经济|10|通过科技创新推动生产力发展的重要理念
乡村振兴|policy|社会|9|全面推进乡村振兴战略的实施
习近平|person|政治|10|国家主席

要求：
- 每行一个知识点
- 名称简洁准确，避免重复
- 分类归属明确
- 重要性根据其在文章中的地位判断
- 描述简洁明了（20-50字）"""

    try:
        response = Generation.call(
            model='qwen-turbo',
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7
        )

        if response.status_code != 200:
            return {"error": f"API调用失败: {response.message}"}

        result_text = response.output.text
        return parse_result(result_text)

    except Exception as e:
        return {"error": f"处理异常: {str(e)}"}


def parse_result(text):
    """
    解析LLM返回的结果

    Args:
        text: LLM返回的文本

    Returns:
        List[dict]: 知识点列表
    """
    points = []

    for line in text.strip().split('\n'):
        line = line.strip()

        # 跳过空行和分隔线
        if not line or line.startswith('-') or line.startswith('='):
            continue

        # 解析|分隔的行
        if '|' in line:
            parts = line.split('|')

            # 至少需要名称、类型、分类、重要性
            if len(parts) >= 4:
                try:
                    point = {
                        'name': parts[0].strip(),
                        'type': normalize_type(parts[1].strip()),
                        'category': parts[2].strip(),
                        'importance': int(parts[3].strip()),
                        'description': parts[4].strip() if len(parts) > 4 else ''
                    }

                    # 验证数据
                    if point['name'] and point['type'] and point['category']:
                        # 限制重要性分数在1-10之间
                        point['importance'] = max(1, min(10, point['importance']))
                        points.append(point)
                except (ValueError, IndexError):
                    continue

    return points


def normalize_type(type_str):
    """
    标准化类型字段

    Args:
        type_str: 原始类型字符串

    Returns:
        str: 标准化的类型
    """
    type_map = {
        '概念': 'concept',
        '核心概念': 'concept',
        '概念性': 'concept',
        '人物': 'person',
        '重要人物': 'person',
        '人名': 'person',
        '事件': 'event',
        '关键事件': 'event',
        '政策': 'policy',
        '重要政策': 'policy',
        '数据': 'data',
        '关键数据': 'data'
    }

    return type_map.get(type_str, 'concept')


def main():
    """主函数：从命令行参数读取文章内容并输出抽取结果"""
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: python ai_extract.py <api_key> <title> [content]"}))
        sys.exit(1)

    title = sys.argv[2]
    content = sys.argv[3] if len(sys.argv) > 3 else ""

    result = extract_knowledge(title, content)

    # 输出JSON格式
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
