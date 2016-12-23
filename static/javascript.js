
var map;

$(document).ready(function(){
	
    var x2js = new X2JS();
    
	map = new OpenLayers.Map("info");
   
    var mapnik = new OpenLayers.Layer.OSM();
    map.addLayer(mapnik);

    map.setCenter(
    	new OpenLayers.LonLat(-99.097,19.447).transform(
        	new OpenLayers.Projection("EPSG:4326"),
        	map.getProjectionObject()
        ), 4
    );
    //*****************************PARTE DEL MAPA **************************

          $.ajax({
            url: '/mongo',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                var obj = jsonQ(response);
            
                initMap();
               
            
                function initMap() {



                    map.addControl(new OpenLayers.Control.ScaleLine());
                    map.addControl(new OpenLayers.Control.OverviewMap());
                    map.addControl(new OpenLayers.Control.MousePosition());
                    map.addControl(new OpenLayers.Control.LayerSwitcher());

                    obj = obj.value()[0];//NOOOOOOBORRARRRRR


                    var your_context = {
                        getColor: function (featur) {
                            if (featur.attributes.sent == "negative"  || featur.attributes.sent =='Negative') {
                                return "blue";
                            } else if (featur.attributes.sent == "positive"  || featur.attributes.sent =='Positive') {
                                return "red";
                            } else if (featur.attributes.sent =='neutral' || featur.attributes.sent =='Neutral') {
                                return "green";
                            } else {
                                return "yellow";
                            }
                        }
                    };
                    /*var your_context = {
                        getColor: function (featur) {
                            if (featur.attributes.day == "Lunes") {
                                return "blue";
                            } else if (featur.attributes.day == "Martes") {
                                return "red";
                            } else if (featur.attributes.day =='Miercoles') {
                                return "green";
                            } else if (featur.attributes.day == "Jueves") {
                                return "yellow";
                            } else if (featur.attributes.day =='Viernes') {
                                return "pink";
                            } else if (featur.attributes.day == "Sabado") {
                                return "brown";
                            } else if (featur.attributes.day =='Domingo') {
                                return "black";
                            } else {
                                return "yellow";
                            }
                        }
                    };*/


                    var yourStyle = new OpenLayers.Style({
                        fillColor: "white",
                        strokeColor: "${getColor}",
                        strokeOpacity: "0.7",
                        strokeWidth: 2,
                        cursor: "pointer",
                            'pointRadius': 3
                    }, {
                        context: your_context
                    });



                  var selectStyle = new OpenLayers.Style({
                        'pointRadius':3 ,
                        strokeColor: "${getColor}",
                    });

                    var your_styleMap = new OpenLayers.StyleMap({
                        'default': yourStyle,
                        'select': selectStyle
                    });




                var geojson_layer = new OpenLayers.Layer.Vector("GeoJSON", {
                     styleMap: your_styleMap 
                  });

               
                var geojson_parser  = new OpenLayers.Format.GeoJSON({
                'internalProjection': new OpenLayers.Projection("EPSG:900913"),
                'externalProjection': new OpenLayers.Projection("EPSG:4326")
                });

                geojson_layer.addFeatures(geojson_parser.read(obj));
                
                map.addLayer(geojson_layer);
                

                //genera un geoJSON
                //var GEOJSON_PARSER = new OpenLayers.Format.GeoJSON();
                //var vectorLayerAsJson = GEOJSON_PARSER.write(geojson_layer.features);
                
                //alert(vectorLayerAsJson);
                
			    //se genera el control y se agrega la capa
			    selectControl = new OpenLayers.Control.SelectFeature(
			        [geojson_layer]
			    );
			    //Se agrega el control al map y se activa
			     map.addControl(selectControl);
    			 selectControl.activate();
    			
                	//geojson_layer.addFeatures(createFeatures());
    				//agregar a la capa de los puntos que muestre la info de cada punto
                geojson_layer.events.on({"featureselected": function(e) {
            			//alert();
            			//validar xml con xmlschema 
            				var xml_str = x2js.json2xml_str({"root":e.feature.attributes});
                            var Module = {
        					 	xml: xml_str,//"<root><text>La fiesta TID UAM-X :) (@ Av. del Taller Y Galindo y Villa w/ @itzelsnchezcru3) https://t.co/t25gZ4tdiu</text><day>Domingo</day><sent>positive</sent></root>",
    							schema: '<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root"><xs:complexType><xs:sequence><xs:element  name="text"><xs:simpleType><xs:restriction base="xs:string"><xs:minLength value="12"/><xs:maxLength value="140"/></xs:restriction></xs:simpleType></xs:element><xs:element type="xs:string" name="day"/><xs:element type="xs:string" name="sent"/></xs:sequence></xs:complexType></xs:element></xs:schema>'
							};
                            
							var xm = xmllint.validateXML(Module);
							if (xm.errors == null){
								var xmlDoc = $.parseXML(xml_str);
								if(xmlDoc){

									$('#tuit').html(xmlDoc.getElementsByTagName('text')[0].childNodes[0].nodeValue);
                                    $('#sent').html(xmlDoc.getElementsByTagName('sent')[0].childNodes[0].nodeValue);
                                    $('#day').html(xmlDoc.getElementsByTagName('day')[0].childNodes[0].nodeValue);
									
								}
							}else
								alert(xm.errors);
                            /*var Module = {
                                xml: xml_str,//"<root><text>La fiesta TID UAM-X :) (@ Av. del Taller Y Galindo y Villa w/ @itzelsnchezcru3) https://t.co/t25gZ4tdiu</text><day>Domingo</day><sent>positive</sent></root>",
                                schema: '<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:element name="root"><xs:complexType><xs:sequence><xs:element type="xs:string" name="hora"/><xs:element type="xs:string" name="city"/><xs:element type="xs:string" name="fecha"/><xs:element type="xs:string" name="subtype"/><xs:element type="xs:string" name="street"/><xs:element type="xs:string" name="day"/></xs:sequence></xs:complexType></xs:element></xs:schema>'
                            };
                            var xm = xmllint.validateXML(Module);
                            if (xm.errors == null){
                                var xmlDoc = $.parseXML(xml_str);
                                if(xmlDoc){

                                    $('#hora').html(xmlDoc.getElementsByTagName('hora')[0].childNodes[0].nodeValue);
                                    $('#city').html(xmlDoc.getElementsByTagName('city')[0].childNodes[0].nodeValue);
                                    $('#fecha').html(xmlDoc.getElementsByTagName('fecha')[0].childNodes[0].nodeValue);
                                    $('#subtype').html(xmlDoc.getElementsByTagName('subtype')[0].childNodes[0].nodeValue);
                                    $('#street').html(xmlDoc.getElementsByTagName('street')[0].childNodes[0].nodeValue);
                                    $('#day').html(xmlDoc.getElementsByTagName('day')[0].childNodes[0].nodeValue);
                                    
                                }
                            }else
                                alert(xm.errors);*/

        				}
    			});

            }
            },//FIN SUCESS
            error: function(error) {
                alert(error);
            }
        });//FIN AJAX*/
    //});
  //*************************************************FIN DEL MAPA **************************
   //*************************************************INICIO GRÁFICA ******************************* 
    var obj_inter;

    $('#btn_chart').click(function() {
        
        setInterval(function() {
           ajax_call();                       
        }, 5000);
        
        ajax_call(); 

        function ajax_call(){
            $.ajax({
                    url: '/grafica',
                    data: $('form').serialize(),
                    type: 'POST',
                   

                    success: function(response) {
                         //alert(response);
                         obj_inter = jsonQ(response);
                         cant = obj_inter.find('cantidad');
                         label = obj_inter.find('label');
                         
                        var barChartData = {
                            labels: label.value()[0],
                            datasets: [{
                                fillColor: "rgba(0,60,100,1)",
                                strokeColor: "black",
                                data: cant.value()[0]
                             }]
                             
                        }
                        var ctx = document.getElementById("canvas").getContext("2d");
                        var barChartDemo = new Chart(ctx).Bar(barChartData, {
                            responsive: true,
                            barValueSpacing: 2
                        });

                    },//FIN SUCCESS BOTTON

                    error: function(error) {
                        alert(error);
                    },
                     
            });
        }//fin functionajax_call()
        
    });//fin btn_chart
//*************************************** FIN GRÁFICA *******************************


//************************************* INICIO REPORTE ******************************
    var xmlDoc;
     $('#btn_report').click(function() {

        setInterval(function() {
           report();                       
        }, 7000);
       
        

        function report(){  
            var sentimiento =  document.getElementById('sent').value;
            var xml = new XMLWriter();
            
            var oj =obj_inter.find('lista');

            var personObj = oj.find('sent', function () {
                return this == sentimiento;
            }).parent();
            //crea XML ----------------------------------------------------
            xml.writeStartDocument(true);
            xml.writeStartElement('tuits');
            
            personObj.each(function (index, path, value) {
                 xml.writeStartElement('tuit');
                    xml.writeElementString('text',value.text);
                    xml.writeElementString('sent',value.sent);
                    xml.writeElementString('day',value.day);
                 xml.writeEndElement();
                //alert(value.sent);
            });
            xml.writeEndElement();
            xml.writeEndDocument();
            xml_str= xml.flush();
            xml_str = xml_str.replace("true", "no"); 
            //------------------------------------------------------

            //----------------VALIDA XML----------------------
            var Module = {
                    xml: xml_str,
                    schema: '<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:simpleType name="text_tuit"><xs:restriction base="xs:string"><xs:maxLength value="140"/></xs:restriction></xs:simpleType><xs:simpleType name="sent_tuit"><xs:restriction base="xs:string"><xs:enumeration value="NEUTRA"/><xs:enumeration value="POSITIVA"/><xs:enumeration value="NEGATIVA"/></xs:restriction></xs:simpleType><xs:element name="tuits"><xs:complexType><xs:sequence><xs:element name="tuit" maxOccurs="unbounded" minOccurs="0"><xs:complexType><xs:sequence><xs:element type="text_tuit" name="text"/><xs:element type="sent_tuit" name="sent"/><xs:element type="xs:string" name="day"/></xs:sequence></xs:complexType></xs:element></xs:sequence></xs:complexType></xs:element></xs:schema>'
            };
                                
            var xm = xmllint.validateXML(Module);
                if (xm.errors == null){
                     xmlDoc= $.parseXML(xml_str);
                    if(xmlDoc){
                        
                        //--------------------------construye la tabla------------------------------- 
                        if (sentimiento == 'POSITIVA'){
                            displayResult(xmlDoc,'#f90312');    
                        }else if (sentimiento == 'NEGATIVA'){
                            displayResult(xmlDoc,' #0315ac'); 
                        }else {
                             displayResult(xmlDoc,'#28e815'); 
                        }
                        
                    }     
                      
                }else
                    alert(xm.errors);
            //----------------VALIDA XML----------------------
        }//fin function report

       function displayResult(xml_doc,color){
            aux= '<?xml version="1.0" encoding="UTF-8"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"><xsl:template match="/"><h2>Tuits Sobre Interjet</h2><table border="3"><tr bgcolor="'+color+'"><th style="text-align:center">Text</th><th style="text-align:center">Sentimiento</th><th style="text-align:center">Día</th></tr><xsl:for-each select="tuits/tuit"><tr><td><xsl:value-of select="text" /></td><td><xsl:value-of select="sent" /></td><td><xsl:value-of select="day" /></td></tr></xsl:for-each></table></xsl:template></xsl:stylesheet>';
            xslDoc= $.parseXML(aux);
            xml = xml_doc;
            xsl = xslDoc;
            
            if (document.implementation && document.implementation.createDocument){
              xsltProcessor = new XSLTProcessor();
              xsltProcessor.importStylesheet(xsl);
              resultDocument = xsltProcessor.transformToFragment(xml, document);
              document.getElementById("example").innerHTML="";//limpia antes de colocar la tabla
              document.getElementById("example").appendChild(resultDocument);
            }
              
        }

        
    });//FIN BUTTON REPORT
// ********************************************************** FIN REPORTE ************************************
});
