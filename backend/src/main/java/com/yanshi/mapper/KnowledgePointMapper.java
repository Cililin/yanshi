package com.yanshi.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yanshi.entity.KnowledgePoint;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 知识点Mapper接口
 */
@Mapper
public interface KnowledgePointMapper extends BaseMapper<KnowledgePoint> {

    /**
     * 查找相似的知识点
     */
    List<KnowledgePoint> findSimilarPoints(@Param("name") String name, @Param("category") String category);

    /**
     * 按分类统计
     */
    List<KnowledgePoint> countByCategory();

    /**
     * 获取热门知识点
     */
    List<KnowledgePoint> getTopPoints(@Param("limit") int limit);

    /**
     * 搜索知识点
     */
    IPage<KnowledgePoint> search(Page<KnowledgePoint> page,
                                  @Param("keyword") String keyword,
                                  @Param("type") String type,
                                  @Param("category") String category);

    /**
     * 按文章ID获取知识点列表
     */
    List<KnowledgePoint> getByArticleId(@Param("articleId") Long articleId);
}
