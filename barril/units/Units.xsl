<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:n1="http://www.posc.org/schemas" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

<xsl:key name="uomkey" match="n1:UnitOfMeasure/n1:CatalogSymbol" use="."/>

    <xsl:template match="/">
        <html>
            <head/>
            <body>
                <xsl:for-each select="n1:UnitOfMeasureDictionary">
                    <xsl:for-each select="n1:DocumentInformation">
                        <xsl:for-each select="n1:DocumentName">
                            <span style="font-size:14 pt; ">Document: </span>
                            <span style="font-size:14 pt; ">
                                <xsl:apply-templates/>
                            </span>
                        </xsl:for-each>
                        <br/>Issue date: <xsl:for-each select="n1:DocumentDate">
                            <xsl:apply-templates/>
                        </xsl:for-each>
                        <br/>Disclaimer: <xsl:for-each select="n1:Disclaimer">
                            <xsl:apply-templates/>
                        </xsl:for-each>
                        <p><i>Note:</i> The latest version of the dictionary is version 2.2, and is found at <a href="http://www.posc.org/refs/poscUnits22.xml">http://www.posc.org/refs/poscUnits22.xml</a></p>
                    </xsl:for-each>
                </xsl:for-each>
                <br/>
                <span style="font-size:12 pt; ">Units of Measure Information:</span>
                <xsl:for-each select="n1:UnitOfMeasureDictionary">
                    <xsl:for-each select="n1:UnitsDefinition">
                        <br/>
                        <xsl:if test="count(  n1:UnitOfMeasure/n1:BaseUnit  ) &gt;0">
                            <p><B>Table of Base Units</B></p>
                            <br/>
                            <p>
                                <table border="1">
                                    <thead>
                                        <tr>
                                            <td align="center">
                                                <span style="font-weight:bold; ">Name</span>
                                            </td>
                                            <td>Quantity Type</td>
                                            <td>Catalog Name</td>
                                            <td>Catalog Symbol</td>
                                            <td align="center">RP66 symbol
                                            </td>
                                            <td>Base Unit Description</td>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <xsl:for-each select="n1:UnitOfMeasure">
<xsl:if test="n1:BaseUnit">
                                            <tr>
                                                <td>
                                                    <xsl:for-each select="n1:Name">
                                                        <xsl:apply-templates/>
                                                    </xsl:for-each>
                                                </td>
                                                <td>
                                                    <xsl:for-each select="n1:QuantityType">
                                                        <xsl:apply-templates/><BR/>
                                                    </xsl:for-each>
                                                </td>
                                                <td>
                                                    <xsl:for-each select="n1:CatalogName">
                                                        <xsl:apply-templates/>
                                                    </xsl:for-each>
                                                </td>
                                                <td>
                                                    <xsl:for-each select="n1:CatalogSymbol">
                                                        <xsl:apply-templates/>
                                                    </xsl:for-each>
                                                </td>
                                                <td>
                      <xsl:for-each select="n1:SameUnit">
                        <xsl:if test="@namingSystem='RP66'">
                          <xsl:value-of select="./@uom"/><BR/>
                        </xsl:if>
                      </xsl:for-each>
                                                </td>
                                                <td>
                                                    <xsl:for-each select="n1:BaseUnit">
                                                        <xsl:for-each select="n1:Description">
                                                            <xsl:apply-templates/>
                                                        </xsl:for-each>
                                                    </xsl:for-each>
                                                </td>
                                            </tr>
</xsl:if>
                                        </xsl:for-each>
                                    </tbody>
                                </table>
                            </p>
                        </xsl:if>
                    </xsl:for-each>
                </xsl:for-each>
                <br/>
                <p>
                    <p>
                        <p>
                            <br/>
                        </p>
                    </p>
                </p>
                <xsl:for-each select="n1:UnitOfMeasureDictionary">
                    <xsl:for-each select="n1:UnitsDefinition">
                        <p>
                            <p>
                                <p><B>Table of Customary Units</B><table border="1">
                                        <thead>
                                            <tr>
                                                <td rowspan="2">Name</td>
                                                <td rowspan="2">Quantity Type</td>
                                                <td rowspan="2">Catalog Name</td>
                                                <td rowspan="2">Catalog Symbol</td>
                                                <td rowspan="2">RP66 symbol</td>
                                                <td align="center" rowspan="2">Base<br/>Unit</td>
                                                <td align="center" colspan="4">Conversion To Base Unit:<br/>(A + BX) / (C + DX)<br/>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td align="center">A</td>
                                                <td align="center">B</td>
                                                <td align="center">C</td>
                                                <td align="center">D</td>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <xsl:for-each select="n1:UnitOfMeasure">
<xsl:if test="n1:ConversionToBaseUnit">
                                                <tr>
                                                    <td>
                                                        <xsl:for-each select="n1:Name">
                                                            <xsl:apply-templates/>
                                                        </xsl:for-each>
                                                    </td>
                                                    <td>
                                                        <xsl:for-each select="n1:QuantityType">
                                                            <xsl:apply-templates/><BR/>
                                                        </xsl:for-each>
                                                    </td>
                                                    <td>
                                                        <xsl:for-each select="n1:CatalogName">
                                                            <xsl:apply-templates/>
                                                        </xsl:for-each>
                                                    </td>
                                                    <td>
                                                        <xsl:for-each select="n1:CatalogSymbol">
                                                            <xsl:apply-templates/>
<xsl:if test="../n1:Deprecated">
  <BR/>(Deprecated)
</xsl:if>
                                                        </xsl:for-each>
                                                    </td>
                                                    <td>
                      <xsl:for-each select="n1:SameUnit">
                        <xsl:if test="@namingSystem='RP66'">
                          <xsl:value-of select="./@uom"/><BR/>
                        </xsl:if>
                      </xsl:for-each>
                                                    </td>
                                                    <td align="center">
    <xsl:choose>
      <xsl:when test="contains(n1:ConversionToBaseUnit/@baseUnit,'#')">
        <xsl:choose>
          <xsl:when test="key('uomkey',substring-after(n1:ConversionToBaseUnit/@baseUnit,'#'))">
		<xsl:value-of select="key('uomkey',substring-after(n1:ConversionToBaseUnit/@baseUnit,'#'))"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="substring-after(n1:ConversionToBaseUnit/@baseUnit,'#')"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:when test="key('uomkey',n1:ConversionToBaseUnit/@baseUnit)">
        <xsl:value-of select="key('uomkey',n1:ConversionToBaseUnit/@baseUnit)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="n1:ConversionToBaseUnit/@baseUnit"/>
      </xsl:otherwise>
    </xsl:choose>

</td>
                                                    <td align="center">
                                                        <xsl:choose>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Formula/n1:A  and  n1:ConversionToBaseUnit/n1:Formula/n1:A  != &quot;&quot;">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Formula">
                                                                        <xsl:for-each select="n1:A">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:otherwise>0</xsl:otherwise>
                                                        </xsl:choose>
                                                    </td>
                                                    <td align="center">
                                                        <xsl:choose>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Factor">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Factor">
                                                                        <xsl:apply-templates/>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Fraction">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Fraction">
                                                                        <xsl:for-each select="n1:Numerator">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:otherwise>
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Formula">
                                                                        <xsl:for-each select="n1:B">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:otherwise>
                                                        </xsl:choose>
                                                    </td>
                                                    <td align="center">
                                                        <xsl:choose>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Formula/n1:C  and  n1:ConversionToBaseUnit/n1:Formula/n1:C  != &quot;&quot;">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Formula">
                                                                        <xsl:for-each select="n1:C">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Fraction">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Fraction">
                                                                        <xsl:for-each select="n1:Denominator">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:otherwise>1</xsl:otherwise>
                                                        </xsl:choose>
                                                    </td>
                                                    <td align="center">
                                                        <xsl:choose>
                                                            <xsl:when test="n1:ConversionToBaseUnit/n1:Formula/n1:D">
                                                                <xsl:for-each select="n1:ConversionToBaseUnit">
                                                                    <xsl:for-each select="n1:Formula">
                                                                        <xsl:for-each select="n1:D">
                                                                            <xsl:apply-templates/>
                                                                        </xsl:for-each>
                                                                    </xsl:for-each>
                                                                </xsl:for-each>
                                                            </xsl:when>
                                                            <xsl:otherwise>0</xsl:otherwise>
                                                        </xsl:choose>
                                                    </td>
                                                </tr>
</xsl:if>
                                            </xsl:for-each>
                                        </tbody>
                                    </table>
                                </p>
                            </p>
                        </p>
                        <br/>
                    </xsl:for-each>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

<xsl:template match="n1:UnitOfMeasure">
  <xsl:value-of select="n1:Name"/>
</xsl:template>

</xsl:stylesheet>