package com.yanshi.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.yanshi.dto.ArticleQueryDTO;
import com.yanshi.entity.Article;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * 文章Mapper
 */
@Mapper
public interface ArticleMapper extends BaseMapper<Article> {

    IPage<Article> selectArticlePage(Page<Article> page, @Param("query") ArticleQueryDTO query);

    List<Map<String, Object>> countBySource();

    List<Map<String, Object>> countByCategory();

    Map<String, Object> getDateRange();

    List<Map<String, Object>> countByDate(@Param("startDate") LocalDate startDate,
                                          @Param("endDate") LocalDate endDate);

    Long countToday();
}
