

// DROPDOWN SET MENU
$('.dropdown-menu a').click(function(){
	$('#selected').text($(this).text());
});



// SEND CLASSIFICATION INFORMATION TO BE SAVED
//  This function retreives the number the user pressed
//  function getKeyEvent(event) {
$(document).keypress(function(e) {
	var pnum = (e.which - 48)
	if(pnum <= 8 && pnum >= 0) {
		var request_data = pnum;
		alert("TODO: Send classification number with active picture ID.");
		// $.ajax({
		// 	url:"/classifier/post_category/",
		// 	// dataType: "json",
		// 	// data: {
		// 	// 		'category': pnum,
		// 	// 		'imgid' : 'http://www.test.url'
		// 	// 		},
		// 	success: function(data) { 
		// 		console.log(data);

		// 	},
		// 	error: function() {
		// 		alert("Fail");
		// 	}
		// });
	}
});




// MODAL SCRIPT
var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById('myImg');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img.onclick = function(){
	modal.style.display = "block";
	modalImg.src = this.src;
	captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
	modal.style.display = "none";
}





// ADD NEW CLASS 
var catbutton = document.getElementById('myCatButton');
catbutton.onclick = function(){
	var catname = prompt('Please enter the name of the new category');
	if (catname != '') {
		alert("TODO: Send the name/ID of the category to be added!");
		// $.ajax
		// ({
		// 	//the url where you want to sent the userName and password to
		// 	type: "GET",
		// 	url: 'add_new_category/',
		// 	//json object to sent to the authentication url
		// 	data: { "catname": catname},
		// 	success : function(data) {
		// 		alert(data);				
		// 		// get_image();
		// 	},

		// 	// handle a non-successful response
		// 	error : function(xhr,errmsg,err) {
		// 		console.log(errmsg); // provide a bit more info about the error to the console
		// 	}
		// })
	}
}
// END BUTTON ADD CATEGORY				

