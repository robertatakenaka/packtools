<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="boxed-text">
        <blockquote>
            <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
        </blockquote>
    </xsl:template>
</xsl:stylesheet>