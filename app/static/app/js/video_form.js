var video_form = (function(){

	function loadingToast(e){
		if (e.keyCode == 13) {
			setInterval(function(){console.log('hi')}, 1000)
			setTimeout(function(){
				setInterval(function(){
					Materialize.toast('Loading the results in a moment :)',4000,'rounded')
				},3000)
			},2000)
		}
	}

	function checkYouTubeLink(e){
		link_input = document.getElementById('icon_prefix2')
		var Url = link_input.value;
		console.log(Url)
		var matches = Url.match(/watch\?v=([a-zA-Z0-9\-_]+)/);
		if (matches){
			console.log("Good")
			$.ajax({
				url : window.location.origin + "/video/download/link",
				method : 'GET',
				data : {
					'url' : Url,
				},
				datatype : 'json',
				success : function(response){
					console.log("gadadasdadasdasd")
					download_url = response.download_link
					window.open(download_url)
				},
			})
		}
	}

	function init(){
		enter_input = document.getElementById('icon_prefix1')
		enter_input.addEventListener('keypress', loadingToast)
		link_input = document.getElementById('icon_prefix2')
		link_input.addEventListener('keypress', checkYouTubeLink)
	}
	return {
		init: init
	};
})();