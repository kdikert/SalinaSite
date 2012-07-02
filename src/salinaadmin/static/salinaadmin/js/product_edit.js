
function update_product(product_json) {
	var items = [];
	$.each(product_json.materials, function(key, val) {
		items.push('<li>' + key + ": " + val.name + " " + val.pk + '</li>');
	});
	
	$('<ul/>', {
		'class': 'my-new-list',
		html: items.join('')
	}).appendTo('body');
	
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
			$(partHtml).find('.material_amount').each(function() {
				$element = $(this);
				$element.attr('id', $element.attr('id').replace(columnAmountRegex, '-amount-' + index));
				$element.attr('name', $element.attr('name').replace(columnAmountRegex, '-amount-' + index));
			});
			$(partHtml).find('.material_text').each(function() {
				$element = $(this);
				$element.attr('id', $element.attr('id').replace(columnTextRegex, '-text-' + index));
				$element.attr('name', $element.attr('name').replace(columnTextRegex, '-text-' + index));
			});
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
		$newMaterialColumn.insertAfter($lastMaterialColumn);
	});
	
	updateMaterialIndexes();
	$('.material_form_remove').show();
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

function removePart(part) {
	var numberOfParts = parseInt($('#id_parts-TOTAL_FORMS').val());
	if (numberOfParts > 1) {
		part.remove();
		updatePartIndexes();
	}
	if (numberOfParts == 2) {
		$('.part_form_remove').hide();
	}
}

$(document).ready(function() {
	
	
	
//	$('.formset_material').formset({
//        prefix: 'materials',
//        formCssClass: 'dynamic_materials_formset'
//    });
//    $('.formset_part').formset({
//        prefix: 'parts',
//        formCssClass: 'dynamic_parts_formset'
//    });
	
	$('.material_form_add').click(function() { appendMaterial(); });

	$('.part_form_add').click(function() { appendPart(); });
	$('.part_form_remove').click(function() { removePart($(this).parent().parent()); });
	
	$.getJSON('json', update_product);
});