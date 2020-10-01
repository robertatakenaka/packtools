<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="disp-formula">
        <xsl:apply-templates select="." mode="expanded"/>
    </xsl:template>

    <xsl:template match="disp-formula" mode="expanded">
        <!-- formula expandida, não miniatura -->
        <div class="row formula" id="e{@id}">
            <a name="{@id}"></a>
            <div class="col-md-12">
                <div class="formula-container">
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula" mode="thumbnail">
        <!-- formula em miniatura --> 
        <xsl:variable name="location">
            <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"></xsl:apply-templates>
        </xsl:variable>
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-4 col-sm-4">
                <a href="" data-toggle="modal" data-target="#ModalScheme{@id}">
                    <div>
                        <xsl:choose>
                        <xsl:when test="$location != ''">
                            <xsl:attribute name="class">thumb</xsl:attribute>
                            <xsl:attribute name="style">background-image: url(<xsl:value-of select="$location"/>);</xsl:attribute>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:attribute name="class">thumbOff</xsl:attribute>
                        </xsl:otherwise>
                    </xsl:choose>
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <strong><xsl:apply-templates select="label"/></strong>
            </div>
        </div>
    </xsl:template>

	<xsl:template match="disp-formula/label">
		<xsl:value-of select="."/>
	</xsl:template>

    <xsl:template match="disp-formula[alternatives]" mode="file-location">
        <xsl:apply-templates select="alternatives" />
    </xsl:template>

    <xsl:template match="tex-math">
        <span class="formula-body">
            <xsl:choose>
                <xsl:when test="contains(.,'\begin{document}') and contains(.,'\end{document}')">
                    <xsl:value-of select="substring-after(substring-before(.,'\end{document}'),'\begin{document}')"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    
</xsl:stylesheet>