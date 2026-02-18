package com.yanshi.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.yanshi.entity.ArticleKnowledgeRelation;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

/**
 * 文章-知识点关联Mapper接口
 */
@Mapper
public interface ArticleKnowledgeRelationMapper extends BaseMapper<ArticleKnowledgeRelation> {

    /**
     * 获取文章的所有知识点关联
     */
    List<ArticleKnowledgeRelation> getByArticleId(Long articleId);

    /**
     * 获取知识点关联的所有文章
     */
    List<ArticleKnowledgeRelation> getByKnowledgePointId(Long knowledgePointId);

    /**
     * 统计知识点的文章数
     */
    int countByKnowledgePointId(Long knowledgePointId);
}
