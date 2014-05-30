// profile.js goes with Profile.html

function processRelatives(relativeJSON, status){

	//alert("Data: " + data + "\nStatus: " + status);
	//making the next three variables global, total relatives and count for the status
	stats = {};                 //initialize a global object to hold the stats
	stats['totalRelatives'] = relativeJSON.relatives.length;
	stats['introsSent'] = 0;    //count of how many successful introductions sent
	stats['genomes'] = 0;    //count of how many are sharing genomes
	stats['publicProfile'] = 0;    // count of how many sharing profiles but not genomes     
	stats['tryToSend'] = 0;
	stats['introDeclined'] = 0;
	stats['cancelled'] = 0;
	replyFromServer = 0;           // if there are no errors, replyFromServer should equal tryToSend when done

	//var $send = $("input[type='radio'][name='send']:checked");
	
	//alert("selectedRelatives:"+selectedRelatives);
	// send intros to people with 'null' intro status and not already sharing genomes; should be first timers.
	
	for (var index=0;index<relativeJSON.relatives.length; index++){
		if (relativeJSON.relatives[index].share_status != 'Sharing Genomes' && relativeJSON.relatives[index].intro_status != 'Introduction Declined' && typeof(relativeJSON.relatives[index].match_id) == 'string'){
			//send to everyone except those sharing genomes or declined. Server will send or cancel and resend depending on intro status.
			postIntro(relativeJSON.relatives[index].match_id);
			stats['tryToSend'] += 1;
			if (relativeJSON.relatives[index].share_status == "Public Match") stats['publicProfile'] +=1;
			if (relativeJSON.relatives[index].intro_status == 'Introduction Cancelled') stats['cancelled'] +=1;
		}
		else{
			
			if (relativeJSON.relatives[index].share_status == 'Sharing Genomes') stats['genomes'] += 1;
			if (relativeJSON.relatives[index].intro_status == 'Introduction Declined') stats['introDeclined'] +=1;
		}
	}
	
}
function postIntroResult(data,status){
	replyFromServer += 1;
	if (data.send == true){
		stats['introsSent'] += 1;
	}
	updateProgress()
	//$("#getProgress").html("sent " + successCount + " introductions out of a total of " + totalRelatives);
	$("#getProgress").html("The selected profile has " + stats['totalRelatives'] + " relatives. <br>" + 
			"Sharing genomes with " + stats['genomes'] + ". <br>" + 
			"Public profiles not sharing genomes " + stats['publicProfile'] + ". <br>" + 
			"Declined introductions " + stats['introDeclined'] + ". <br>" +
			"Cancelled introductions " + stats['cancelled'] + ". <br>" +
			"Sending " + stats['introsSent'] + " introductions.");
	$("#explanation").html("Not all introductions were sent because either; the introduction was already accepted, a previous introduction was rejected, " +
			"an introduction was already sent and it is too soon to resend another.");
}

function updateProgress(){
	var percentDone = Math.round(((replyFromServer)/stats['tryToSend']) * 100);
	$("#percent").html(percentDone + "%");
	$("#bar").css('width', percentDone + '%');
}

function postIntro(match_id){
	$.post(
		"send_intro/",
		{profile_id:$("input[type='radio'][name='profile_id']:checked").val(),
		 match_id:match_id,
		 csrfmiddlewaretoken:$("input[name='csrfmiddlewaretoken']").val()
		 },
		 function(data,status){
			 postIntroResult(data,status);
		 })
		.fail(function(xhr) {
			replyFromServer += 1;   //still need to count this. Maybe should resend?
			updateProgress()
		    console.log("Error: " + xhr.statusText);
		 });
}
function handleSubmit(event){
	//alert( "#2" );
    var $profile_id = $("input[type='radio'][name='profile_id']:checked");
    //if ($profile_id.length == 0){
    //    alert("need to select a profile");
    //    return false;  //is this status used?
    //}
    //loopLi();
	$("#getProgress").html("getting results...");
	// make progress bar visible
	$("#progress").css('visibility', 'visible');
	$("#percent").html(0 + "%");
	$("#bar").css('width', 0 + '%');
    var $send = $("input[type='radio'][name='send']:checked");
	$.post("relatives/",
		{profile_id:$profile_id.val(),
        introductionText: $(".textBox").text(),
	    csrfmiddlewaretoken:$("input[name='csrfmiddlewaretoken']").val()
	    },
	    function(data,status){
	    	//alert('ready to process relatives');
	    	processRelatives(data, status);
	    })
	.fail(function(xhr) {
	        console.log("Error: " + xhr.statusText);
	        alert("Error: " + xhr.statusText);
	    });
	//return false;
}

$(document).ready(function () {
	if($("input[type='radio'][name='profile_id']:checked").length == 0){
			$("input[type='radio'][name='profile_id']:first").prop('checked',true);
	}
    //on clicking the submit button, do this
    $( "#relatives" ).submit(function( event ) {
	  event.preventDefault();   // do I need to prevent default action?
	  handleSubmit(event);
	});
});


