var categoriesContainer = "div#categories-container";
var selectedSet = "span#selected-set";
var catButton = "a#cat-button";
var photosContainer = "div#images-container";
var dropdownChoices = ".dropdown-menu a";
var selectedImage = "img#myImg";


$(function () {
    // display categories
    refreshCategories();

    // display photos
    refreshPhotos();

    $(dropdownChoices).click(function (e) {
        e.preventDefault();
        var $selectedSet = $(selectedSet);
        $selectedSet.text($(this).text());
        $selectedSet.data("id", $(this).data("id"));
        refreshPhotos();
    });

     $(categoriesContainer).on("click", "button", function () {
        associatePhoto($(this).data('id'));
     });

    $(categoriesContainer).on("click", catButton, function () {
        var catname = prompt('Please enter the name of the new category');
        var url = $(categoriesContainer).data('url');
        if (catname !== '') {
            // alert("TODO: Send the name/ID of the category to be added!");
            $.ajax
            ({
                type: "POST",
                url: url,
                data: {"title": catname},
                success: function (data) {
                    refreshCategories()
                },
                // handle a non-successful response
                error: function (xhr, errmsg, err) {
                    console.log(errmsg); // provide a bit more info about the error to the console
                }
            })
        }
    });
});


// SEND CLASSIFICATION INFORMATION TO BE SAVED
//  This function retreives the number the user pressed
//  function getKeyEvent(event) {
// $(document).keypress(function (e) {
//     var pnum = (e.which - 48)
//     if (pnum <= 8 && pnum >= 0) {
//         var request_data = pnum;
//         alert("TODO: Send classification number with active picture ID.");
//         // $.ajax({
//         // 	url:"/classifier/post_category/",
//         // 	// dataType: "json",
//         // 	// data: {
//         // 	// 		'category': pnum,
//         // 	// 		'imgid' : 'http://www.test.url'
//         // 	// 		},
//         // 	success: function(data) {
//         // 		console.log(data);
//
//         // 	},
//         // 	error: function() {
//         // 		alert("Fail");
//         // 	}
//         // });
//     }
// });


// MODAL SCRIPT
// var modal = document.getElementById('myModal');
//
// // Get the image and insert it inside the modal - use its "alt" text as a caption
// var img = document.getElementById('myImg');
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
// img.onclick = function () {
//     modal.style.display = "block";
//     modalImg.src = this.src;
//     captionText.innerHTML = this.alt;
// };
//
// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];
//
// // When the user clicks on <span> (x), close the modal
// span.onclick = function () {
//     modal.style.display = "none";
// };


function refreshCategories() {
    var $categoriesContainer = $(categoriesContainer);
    var url = $categoriesContainer.data('url');
    $.ajax({
        url: url,
        success: function (data) {
            $categoriesContainer.html(data);
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    })
}


function refreshPhotos() {
    // change for photos
    var $photosContainer = $(photosContainer);
    var url = $photosContainer.data('url').replace("0", $(selectedSet).data('id'));
    $.ajax({
        url: url,
        success: function (data) {
            $photosContainer.html(data);
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
        }
    })
}

function associatePhoto(categoryId) {
    var photoId = $(selectedImage).data('id');
    var photoSetId = $(selectedSet).data('id');
    var url = $(categoriesContainer).data('associate-url');
    $.ajax({
        type: "POST",
        url: url,
        data: {
            "photo": photoId,
            "photo_set": photoSetId,
            "category": categoryId
        },
        success: function (data) {
            refreshCategories();
            refreshPhotos();
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            console.log(errmsg); // provide a bit more info about the error to the console
        }
    })
}

// CSRF TOKEN SETUP

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
