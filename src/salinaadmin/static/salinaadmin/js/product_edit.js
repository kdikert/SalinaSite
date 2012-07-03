
function updateProduct(productJSON) {
	
	var materialFormsCount = 1; //parseInt($('#id_materials-TOTAL_FORMS').val());
	var partFormsCount = 1; //parseInt($('#id_parts-TOTAL_FORMS').val());
	
	var materials = productJSON['materials'];
	var parts = productJSON['parts'];
	
	for (var i = 0; i < materials.length - materialFormsCount; i++) {
		appendMaterial();
	}
	updateMaterialIndexes();
	
	$('.material_form option').each(function() {
		$(this).removeAttr('selected');
	});
	for (var i = 0; i < materials.length; i++) {
		$('#id_materials-' + i + '-material option[value="' + materials[i]['pk'] + '"]').attr('selected', 'selected');
	}
	
	for (var i = 0; i < parts.length - partFormsCount; i++) {
		appendPart();
	}
	updatePartIndexes();
	
	var part;
	for (var i = 0; i < parts.length; i++) {
		part = parts[i];
		$('#id_parts-' + i + '-name').val(part['name']);
		$('#id_parts-' + i + '-time_min').val(part['time']);
		$('#id_parts-' + i + '-price').val(part['price']);
		for (var materialIndex = 0; materialIndex < part.materials.length; materialIndex++) {
			$('#id_parts-' + i + '-amount-' + materialIndex).val(part.materials[materialIndex].amount);
			$('#id_parts-' + i + '-text-' + materialIndex).val(part.materials[materialIndex].text);
		}
	}
}

function updateMaterialIndexes() {
	var $element, count;
	var formNameRegex = /^materials-[0-9]+-/;
	var formIdRegex = /^id_materials-[0-9]+-/;
	
	$('.material_form').each(function(index, partHtml) {
		$(partHtml).find('select').each(function() {
			$element = $(this);
			$element.attr('id', $element.attr('id').replace(formIdRegex, 'id_materials-' + index + '-'));
			$element.attr('name', $element.attr('name').replace(formNameRegex, 'materials-' + index + '-'));
		});
		count = index + 1;
	});
	
	var columnAmountRegex = /-amount-[0-9]+$/;
	var columnTextRegex = /-text-[0-9]+$/;
	
	$('.part_form').each(function() {
		$(this).find('.material_column').each(function(index, partHtml) {
			$element = $(partHtml).find('.material_amount').first();
			$element.attr('id', $element.attr('id').replace(columnAmountRegex, '-amount-' + index));
			$element.attr('name', $element.attr('name').replace(columnAmountRegex, '-amount-' + index));
			
			$element = $(partHtml).find('.material_text').first();
			$element.attr('id', $element.attr('id').replace(columnTextRegex, '-text-' + index));
			$element.attr('name', $element.attr('name').replace(columnTextRegex, '-text-' + index));
		});
	});
	
	$('#id_materials-TOTAL_FORMS').val(count);
}

function appendMaterial() {
	var $lastMaterial = $('.material_form:last');
	var $newMaterial = $lastMaterial.clone(true);
	$newMaterial.insertAfter($lastMaterial);

	$('.part_form').each(function(index, partHtml) {
		var $lastMaterialColumn = $(partHtml).find('.material_column:last');
		var $newMaterialColumn = $lastMaterialColumn.clone(true);

		$newMaterialColumn.find('input').each(function() {
	    	$(this).val('');
	    });
	    
		$newMaterialColumn.insertAfter($lastMaterialColumn);
	});
	
	updateMaterialIndexes();
	$('.material_form_remove').show();
}

function removeMaterial($materialTD) {
	var numberOfMaterials = parseInt($('#id_materials-TOTAL_FORMS').val());
	var $materialElement = $materialTD.find('select').first();
	
	var materialNameRegex = /^materials-([0-9]+)-/;
	var materialIndex = materialNameRegex.exec($materialElement.attr('name'))[1];
	
	if (numberOfMaterials > 1) {
		$materialTD.remove();
		
		$('.part_form').each(function() {
			$(this).find('.material_column').each(function(index, partHtml) {
				if (index == materialIndex) {
					$(partHtml).remove();
				}
			});
		});
		
		updateMaterialIndexes();
	}
	
	if (numberOfMaterials == 2) {
		$('.material_form_remove').hide();
	}
}

function updatePartIndexes() {
	var $element, count;
	var formNameRegex = /^parts-[0-9]+-/;
	var formIdRegex = /^id_parts-[0-9]+-/;
	
	$('.part_form').each(function(index, partHtml) {
		$(partHtml).find('input').each(function() {
			$element = $(this);
			$element.attr('id', $element.attr('id').replace(formIdRegex, 'id_parts-' + index + '-'));
			$element.attr('name', $element.attr('name').replace(formNameRegex, 'parts-' + index + '-'));
		});
		count = index + 1;
	});
	
	$('#id_parts-TOTAL_FORMS').val(count);
}

function appendPart() {
	var $lastPart = $('.part_form:last');
    var $newPart = $lastPart.clone(true);
    
    $newPart.find('input').each(function() {
    	$(this).val('');
    });
    
    $newPart.insertAfter($lastPart);
    updatePartIndexes();
    $('.part_form_remove').show();
}

function removePart($partRow) {
	var numberOfParts = parseInt($('#id_parts-TOTAL_FORMS').val());
	if (numberOfParts > 1) {
		$partRow.remove();
		updatePartIndexes();
	}
	if (numberOfParts == 2) {
		$('.part_form_remove').hide();
	}
}

$(document).ready(function() {
	
	$('.material_form_add').click(function() { appendMaterial(); });
	$('.material_form_remove').click(function() { removeMaterial($(this).parent()); });

	$('.part_form_add').click(function() { appendPart(); });
	$('.part_form_remove').click(function() { removePart($(this).parent().parent()); });
	
	$.getJSON('json', updateProduct);
});
