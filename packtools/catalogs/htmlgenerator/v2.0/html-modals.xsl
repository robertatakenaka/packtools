<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-modals">
        <xsl:apply-templates select="." mode="modal-contribs"/>

        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select="." mode="article-modals-for-selected-body">
                    <xsl:with-param name="body" select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//body"/>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="article-modals-for-selected-body">
                    <xsl:with-param name="body" select="body"/>
                </xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>

        <xsl:apply-templates select="." mode="modal-how2cite"/>
    </xsl:template>
    
    <xsl:template match="article" mode="article-modals-for-selected-body">
        <xsl:param name="body"/>
        <xsl:apply-templates select="." mode="modal-all-items">
            <xsl:with-param name="body" select="$body"/>
        </xsl:apply-templates>
        <xsl:apply-templates select="front | $body | back" mode="modal-figs"/>
        <xsl:apply-templates select="front | $body | back" mode="modal-tables"/>
        <xsl:apply-templates select="front | $body | back" mode="modal-disp-formulas"/>
    </xsl:template>
    
    <xsl:template match="front | body | back" mode="modal-tables">
        <xsl:apply-templates select=".//table-wrap" mode="modal"/>
    </xsl:template>
    
    <xsl:template match="front | body | back" mode="modal-disp-formulas">
        <xsl:apply-templates select=".//disp-formula" mode="modal"/>
    </xsl:template>
    
    <xsl:template match="front | body | back" mode="modal-figs">
        <xsl:apply-templates select=".//*[fig]" mode="modal-figs"/>
    </xsl:template>
    
    <xsl:template match="*[fig]" mode="modal-figs">
        <xsl:choose>
            <xsl:when test="fig[@xml:lang=$TEXT_LANG]">
                <!-- * == figgroup -->
                <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="modal"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- * == not figgroup -->
                <xsl:apply-templates select=".//fig" mode="modal"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="modal-all-items">
        <xsl:param name="body"/>

        <xsl:variable name="total_figs">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="body" select="$body"/>
                <xsl:with-param name="object" select="'fig'"/>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="total_tables">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="body" select="$body"/>
                <xsl:with-param name="object" select="'table'"/>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="total_formulas">
            <xsl:apply-templates select="." mode="get-total">
                <xsl:with-param name="body" select="$body"/>
                <xsl:with-param name="object" select="'formula'"/>
            </xsl:apply-templates>
        </xsl:variable>

         <xsl:if test="number($total_figs) + number($total_tables) + number($total_formulas) &gt; 0">
             <div class="modal fade ModalDefault" id="ModalTablesFigures" tabindex="-1" role="dialog" aria-hidden="true">
                 <div class="modal-dialog">
                     <div class="modal-content">
                         <div class="modal-header">
                             <button type="button" class="close" data-dismiss="modal">
                                 <span aria-hidden="true">&#xd7;</span>
                                 <span class="sr-only">
                                     <xsl:apply-templates select="." mode="interface">
                                         <xsl:with-param name="text">Close</xsl:with-param>
                                     </xsl:apply-templates>
                                 </span>
                             </button>
                             <h4 class="modal-title"><xsl:value-of select="$graphic_elements_title"/></h4>
                         </div>
                         <div class="modal-body">
                             <ul class="nav nav-tabs md-tabs" role="tablist">
                                <xsl:apply-templates select="." mode="modal-all-items-total-objects">
                                    <xsl:with-param name="body" select="$body"/>
                                    <xsl:with-param name="total_figs" select="$total_figs"/>
                                    <xsl:with-param name="total_tables" select="$total_tables"/>
                                    <xsl:with-param name="total_formulas" select="$total_formulas"/>
                                </xsl:apply-templates>
                             </ul>
                             <div class="clearfix"></div>
                             <div class="tab-content">
                                <xsl:apply-templates select="." mode="modal-all-items-display-objects">
                                    <xsl:with-param name="body" select="$body"/>
                                    <xsl:with-param name="total_figs" select="$total_figs"/>
                                    <xsl:with-param name="total_tables" select="$total_tables"/>
                                    <xsl:with-param name="total_formulas" select="$total_formulas"/>
                                </xsl:apply-templates>
                             </div>
                         </div>
                     </div>
                 </div>
             </div>
         </xsl:if>
    </xsl:template>
    
    <xsl:template match="article" mode="modal-all-items-total-objects">
        <xsl:parm name="total_figs" select="'0'"/>
        <xsl:parm name="total_tables" select="'0'"/>
        <xsl:parm name="total_formulas" select="'0'"/>

        <!-- 
        Apresenta todos os elementos do documento de um dado body selecionado
        divididos por abas: "Figures", "Tables", "Formulas".
        No entanto, as abas somente aparecem se existem os respectivos objetos.
        Apenas uma das abas aparece como "active", e a ordem de precedência é:
        "Figures", "Tables", "Formulas" e ficará como "active" a primeira que
        tiver objetos.
        -->
        <xsl:apply-templates select="." mode="modal-all-items-total-object-type">
            <xsl:with-param name="anchor">figures</xsl:with-param>
            <xsl:with-param name="label">Figures</xsl:with-param>
            <xsl:with-param name="total" select="$total_figs"/>
            <xsl:with-param name="active">active</xsl:with-param>
        </xsl:apply-templates>

        <xsl:apply-templates select="." mode="modal-all-items-total-object-type">
            <xsl:with-param name="anchor">tables</xsl:with-param>
            <xsl:with-param name="label">Tables</xsl:with-param>
            <xsl:with-param name="total" select="$total_tables"/>
            <xsl:with-param name="active">
                <xsl:if test="$total_figs='0'">active</xsl:if>
            </xsl:with-param>
        </xsl:apply-templates>

        <xsl:apply-templates select="." mode="modal-all-items-total-object-type">
            <xsl:with-param name="anchor">schemes</xsl:with-param>
            <xsl:with-param name="label">Formulas</xsl:with-param>
            <xsl:with-param name="total" select="$total_formulas"/>
            <xsl:with-param name="active">
                <xsl:if test="$total_figs='0' and $total_tables='0'">active</xsl:if>
            </xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="article" mode="modal-all-items-total-object-type">
        <xsl:param name="anchor"/>
        <xsl:param name="label"/>
        <xsl:param name="total"/>
        <xsl:param name="active"/>

        <xsl:if test="number($total) &gt; 0">
            <li role="presentation" class="col-md-4 col-sm-4 {$active}">
                <a href="#{$anchor}" aria-controls="{$anchor}" role="tab" data-toggle="tab">
                    <xsl:apply-templates select="." mode="interface">
                        <xsl:with-param name="text" select="$label"/>
                    </xsl:apply-templates>
                    (<xsl:value-of select="$total"/>)
                </a>
            </li>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="get-total">
        <xsl:param name="body"/>
        <xsl:param name="object"/>
        <xsl:choose>
            <xsl:when test="count(.//body) = 1">
                <xsl:apply-templates select="." mode="sum-objects">
                    <xsl:with-param name="object" select="$object"/>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="f"><xsl:apply-templates select="front" mode="sum-objects">
                    <xsl:with-param name="object" select="$object"/>
                </xsl:apply-templates></xsl:variable>
                <xsl:variable name="b"><xsl:apply-templates select="$body" mode="sum-objects">
                    <xsl:with-param name="object" select="$object"/>
                </xsl:apply-templates></xsl:variable>
                <xsl:variable name="bk"><xsl:apply-templates select="back" mode="sum-objects">
                    <xsl:with-param name="object" select="$object"/>
                </xsl:apply-templates></xsl:variable>
                <xsl:value-of select="number($f)+number($b)+number($bk)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="article | front | body | back" mode="sum-objects">
        <xsl:param name="object"/>
        <xsl:choose>
            <xsl:when test="$object='fig'">
                <xsl:value-of select="count(.//fig-group[@id]/fig[@xml:lang][1]) + count(.//fig[not(@xml:lang)])"/>
            </xsl:when>
            <xsl:when test="$object='table'">
                <xsl:value-of select="count(.//table-wrap-group)+count(.//*[table-wrap and name()!='table-wrap-group']//table-wrap)"/>
            </xsl:when>
            <xsl:when test="$object='formula'">
                <xsl:value-of select="count(.//disp-formula[@id])"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="article" mode="modal-all-items-display-objects">
        <xsl:param name="body"/>
        <xsl:parm name="total_figs" select="'0'"/>
        <xsl:parm name="total_tables" select="'0'"/>
        <xsl:parm name="total_formulas" select="'0'"/>

        <!-- 
        Apresenta todos os elementos do documento de um dado body selecionado
        divididos por abas: "Figures", "Tables", "Formulas".
        No entanto, as abas somente aparecem se existem os respectivos objetos.
        Apenas uma das abas aparece como "active", e a ordem de precedência é:
        "Figures", "Tables", "Formulas" e ficará como "active" a primeira que
        tiver objetos.
        -->
        <xsl:apply-templates select="." mode="modal-all-items-display-tabpannel">
            <xsl:with-param name="anchor">figures</xsl:with-param>
            <xsl:with-param name="body" select="$body"/>
            <xsl:with-param name="total" select="$total_figs"/>
            <xsl:with-param name="active">active</xsl:with-param>
        </xsl:apply-templates>

        <xsl:apply-templates select="." mode="modal-all-items-display-tabpannel">
            <xsl:with-param name="anchor">tables</xsl:with-param>
            <xsl:with-param name="body" select="$body"/>
            <xsl:with-param name="total" select="$total_tables"/>
            <xsl:with-param name="active">
                <xsl:if test="$total_figs='0'">active</xsl:if>
            </xsl:with-param>
        </xsl:apply-templates>

        <xsl:apply-templates select="." mode="modal-all-items-display-tabpannel">
            <xsl:with-param name="anchor">schemes</xsl:with-param>
            <xsl:with-param name="body" select="$body"/>
            <xsl:with-param name="total" select="$total_formulas"/>
            <xsl:with-param name="active">
                <xsl:if test="$total_figs='0' and $total_tables='0'">active</xsl:if>
            </xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="article" mode="modal-all-items-display-tabpannel">
        <xsl:param name="anchor"/>
        <xsl:param name="body"/>
        <xsl:param name="total"/>
        <xsl:param name="active"/>

        <xsl:if test="number($total) &gt; 0">
            <div role="tabpanel" class="tab-pane {$active}" id="{$anchor}">
                <xsl:choose>
                    <xsl:when test="$anchor='figures'">
                        <xsl:apply-templates select="front | $body | back" mode="modal-all-items-figs"/>
                    </xsl:when>
                    <xsl:when test="$anchor='tables'">
                        <xsl:apply-templates select="front | $body | back" mode="modal-all-items-tables"/>
                    </xsl:when>
                    <xsl:when test="$anchor='schemes'">
                        <xsl:apply-templates select="front | $body | back" mode="modal-all-items-formulas"/>
                    </xsl:when>
                </xsl:choose>
            </div>
        </xsl:if>
    </xsl:template>
 
    <xsl:template match="front | body | back" mode="modal-all-items-tables">
        <xsl:apply-templates select=".//table-wrap-group[table-wrap] | .//*[table-wrap and name()!='table-wrap-group']/table-wrap" mode="modal-all-item"/>
    </xsl:template>

    <xsl:template match="front | body | back" mode="modal-all-items-formulas">
        <xsl:apply-templates select=".//disp-formula[@id]" mode="modal-all-item"/>
    </xsl:template>

    <xsl:template match="front | body | back" mode="modal-all-items-figs">
        <xsl:apply-templates select=".//*[fig]" mode="modal-all-items-figs"/>
    </xsl:template>

    <xsl:template match="*[fig]" mode="modal-all-items-figs">
        <xsl:choose>
            <xsl:when test="fig[@xml:lang=$TEXT_LANG]">
                <!-- * == figgroup -->
                <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="modal-all-item"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- * == not figgroup -->
                <xsl:apply-templates select=".//fig" mode="modal-all-item"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="fig | disp-formula[@id]" mode="modal-all-item">
        <div class="row fig">
            <xsl:apply-templates select="." mode="modal-all-item-thumbnail"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="modal-all-item-label"></xsl:apply-templates>
        </div>        
    </xsl:template>
 
    <xsl:template match="table-wrap-group[table-wrap]" mode="modal-all-item">
        <div class="row table">
            <xsl:apply-templates select="." mode="modal-all-item-thumbnail"></xsl:apply-templates>
            <xsl:apply-templates select="table-wrap[@xml:lang=$TEXT_LANG]" mode="modal-all-item-label"></xsl:apply-templates>
        </div>        
    </xsl:template>
    
    <xsl:template match="table-wrap[not(@xml:lang)]" mode="modal-all-item">
        <div class="row table">
            <xsl:apply-templates select="." mode="modal-all-item-thumbnail"></xsl:apply-templates>
            <xsl:apply-templates select="." mode="modal-all-item-label"></xsl:apply-templates>
        </div>        
    </xsl:template>

    <xsl:template match="fig" mode="modal-all-item-thumbnail">
        <xsl:variable name="location">
            <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"></xsl:apply-templates>
        </xsl:variable>
        <xsl:variable name="figid">
            <xsl:choose>
                <xsl:when test="@id"><xsl:value-of select="@id"/></xsl:when>
                <xsl:when test="../../fig-group/@id"><xsl:value-of select="../../fig-group/@id"/></xsl:when>
                <xsl:otherwise>IDMISSING</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalFig{$figid}">
                <div class="thumb" style="background-image: url({$location});">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
                <div>
                    <xsl:choose>
                        <xsl:when test="$location">
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
    </xsl:template>
            
    <xsl:template match="table-wrap | table-wrap-group" mode="modal-all-item-thumbnail">
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalTable{@id}">
                <div class="thumbOff">
                    Thumbnail
                    <div class="zoom"><span class="sci-ico-zoom"></span></div>
                </div>
            </a>
        </div>
    </xsl:template>
             
    <xsl:template match="disp-formula[@id]" mode="modal-all-item-thumbnail">
        <xsl:variable name="location">
            <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"></xsl:apply-templates>
        </xsl:variable>
        <div class="col-md-4">
            <a data-toggle="modal" data-target="#ModalScheme{@id}">
                <div>
                    <xsl:choose>
                        <xsl:when test="graphic">
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
    </xsl:template>
    
    <xsl:template match="fig | table-wrap" mode="modal-all-item-label">
        <div class="col-md-8">
            <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
        </div>
    </xsl:template>

    <xsl:template match="disp-formula[@id]" mode="modal-all-item-label">
        <div class="col-md-8">
            <xsl:apply-templates select="label"></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>