<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:param name="article_lang" />
    <xsl:param name="is_translation" />
    <xsl:param name="issue_label" />
    <xsl:param name="styles_css_path" />
    
    <xsl:param name="INTERFACE_LANG"><xsl:value-of select="$article_lang"/></xsl:param>
    <xsl:param name="TEXT_LANG"><xsl:value-of select="$article_lang"/></xsl:param>
    <xsl:param name="ARTICLE_LANG"><xsl:value-of select="$article_lang"/></xsl:param>
    <xsl:param name="IMAGES_PATH"></xsl:param>
    <xsl:param name="CSS_PATH">/Users/roberta.takenaka/Documents/xml/htmlgenerator/2017-01-10-scielo/static/css</xsl:param>
    <xsl:param name="JS_PATH">/Users/roberta.takenaka/Documents/xml/htmlgenerator/2017-01-10-scielo/static/js</xsl:param>
    <xsl:param name="WEBSITE_IMG_PATH">/Users/roberta.takenaka/Documents/xml/htmlgenerator/2017-01-10-scielo/static/img</xsl:param>
    
</xsl:stylesheet>