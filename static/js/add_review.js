/*
function add_place_review(slug){
	fix_stars();
	
	/*
	var xhttp = new XMLHttpRequest();
	var params = "task=add_place_review&slug="+slug+"&review="+document.getElementById("pr_review").value+"&stars="+document.getElementById("pr_stars");
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById("review_section").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST", "/placeholdr/ajax", true);
	xhttp.send(params);
	
}
*/
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

function fix_tags() {

    var tag_pattern = /(#(\S*))/gi;

    var tag_text = '<a style="color:red; text-decoration:none;" href="/placeholdr/search?=$2">$1</a>';


    document.getElementById("tag_section").innerHTML = document.getElementById("tag_section").innerHTML.replace(tag_pattern, tag_text);
    document.getElementById("review_section").innerHTML = document.getElementById("review_section").innerHTML.replace(tag_pattern, tag_text);


}

$(document).ready(function () {

    reset_page();

});

function reset_page() {

    fix_tags();
    $('#rev_submit').click(function () {
        fix_stars();


        $.ajax({
            type: "POST",
            url: "/placeholdr/ajax/",
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': getCookie('csrftoken'),
                'task': document.getElementById("task").innerHTML + "_review",
                'slug': document.getElementById("slug").innerHTML,
                'review': document.getElementById("r_review").value + " ",
                'stars': document.getElementById("r_stars").value
            },
            success: function (data) {
                response = data;

                document.getElementById("review_sec").innerHTML = response.rev_sec;
                document.getElementById("star_rating").innerHTML = response.stars_string;
                document.getElementById("tag_section").innerHTML = response.tags_string;

                document.getElementById("r_review").value = ""
                reset_page();
                fix_tags();
            }
        });
    });
	
	do_rep(0);

}

function do_rep(value){
	
	$.ajax({
            type: "POST",
            url: "/placeholdr/ajax/",
            dataType: 'json',
            data: {
                'csrfmiddlewaretoken': getCookie('csrftoken'),
                'task': document.getElementById("task").innerHTML + "_rep",
                'slug': document.getElementById("slug").innerHTML,
                'rep': value
            },
            success: function (data) {
                response = data;

				rep_val = data.rep;
				
				if (rep_val == "1"){
					document.getElementById("repup").src = document.getElementById("repup").src.replace(".png", "_dark.png");
					document.getElementById("repdown").src = document.getElementById("repdown").src.replace("_dark", "");
					
					document.getElementById("repup").setAttribute("onClick","");
					document.getElementById("repdown").setAttribute("onClick","do_rep(-1)");
				}else if(rep_val == "-1"){
					document.getElementById("repdown").src = document.getElementById("repdown").src.replace(".png", "_dark.png");
					document.getElementById("repup").src = document.getElementById("repup").src.replace("_dark", "");
					
					document.getElementById("repup").setAttribute("onClick","do_rep(1)");
					document.getElementById("repdown").setAttribute("onClick","");
				}else{
					document.getElementById("repup").src = document.getElementById("repup").src.replace("_dark", "");
					document.getElementById("repdown").src = document.getElementById("repdown").src.replace("_dark", "");
					
					document.getElementById("repup").setAttribute("onClick","do_rep(1)");
					document.getElementById("repdown").setAttribute("onClick","do_rep(-1)");
				}

            },
			error: function (data) {
				if (value != 0){
					alert("Please login to rate a user");
				}
			}
        });
	
}


function fix_stars() {
    if (document.getElementById("r_stars") == null) {

        return;

    }

    if (document.getElementById("r_stars").value.length > 1) {

        document.getElementById('r_stars').value = document.getElementById('r_stars').value.substr(0, 1);
        alert("Please enter a number from 1-5");

    }

    if (document.getElementById('r_stars').value.search("[1-5]") == -1) {

        document.getElementById('r_stars').value = "";
        alert("Please enter a number from 1-5");

    }
}