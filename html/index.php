<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="EXPIRES" CONTENT="0">
    <title>NER English Demo</title>
    <link rel="stylesheet" type="text/css" href="./html/css/w3.css">
    <link rel="stylesheet" type="text/css" href="./html/css/multilang.css">
	<script src="./html/js/jquery-3.5.1.min.js"></script>
	<script src="./html/js/multilang.js"></script>

	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
    </style>
</head>
<body>
<div class="main">
	<form id="demoForm" name="demoForm" onSubmit="return false;">
		<div class="w3-container">
			<div class="w3-left">
				<label> <b>Annotators</b> </label>
				<br>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="conll">
				<label>neural_conll</label>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="onto_ner">
				<label>neural_onto</label>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="cogcomp_conll">
				<label>cogcomp_conll</label>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="cogcomp_onto">
				<label>cogcomp_onto</label>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="kairos_ner">
				<label>neural_kairos</label>
				
				 
			</div>
			<div class="w3-right">
			<!--
				<div class="w3-left">
					<label> <b>Languages:</b> </label>
					<br>
					<select class="w3-select w3-border" id="lang" name="lang" value="eng" onChange="javascript:newLanguageSelect();" style="width:128px;">
					</select>
				</div>
			-->
				<div class="w3-left">
					<label> <b>Examples:</b> </label>
					<br>
					<select class="w3-select w3-border" id="example" name="example" value="" onChange="javascript:newExampleSelect();" style="width:512px;">
						<!--<option value="">Select a language... -->
					</select>
				</div>
			</div>
		</div>
		<div class="w3-container">
			<label> <b>Text:</b> </label>
			<br>
			<textarea class="w3-input w3-border" id="text" name="text" rows="8" cols="50" style="resize: vertical;"></textarea>
		</div>
		<div class="w3-container">
			<button class="w3-button w3-blue" onClick="return formSubmit();"> Run > </button>
		</div>
	</form>

	<!--<div class="w3-container">-->
		&nbsp;
		<br>
		<div id="result" class="w3-container">
		</div>
	<!--</div>-->

</div>

<script>main();</script>
</body>
</html>
