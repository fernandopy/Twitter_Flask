
var map;

$(document).ready(function(){
	var x2js = new X2JS();
    
	//$('#info').html("<br><b>Loading grafica...</b>");
    map = new OpenLayers.Map("info");
   
    var mapnik = new OpenLayers.Layer.OSM();
    map.addLayer(mapnik);

    map.setCenter(
    	new OpenLayers.LonLat(-99.097,19.447).transform(
        	new OpenLayers.Projection("EPSG:4326"),
        	map.getProjectionObject()
        ), 4
    );
    ///$('button').click(function() {

    	//var user = $('#txtUsername').val();
        //var pass = $('input[name="password"]').val();
        $.ajax({
            url: '/mongo',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                //alert(response);
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
                            if (featur.attributes.sent == "negative") {
                                return "blue";
                            } else if (featur.attributes.sent == "positive") {
                                return "red";
                            } else if (featur.attributes.sent =='neutral') {
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
        });//*/
    //});
});
